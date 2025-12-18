import platform
import ctypes

# --- DPI awareness (same as your original) ---
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception as e:
        print(f"[Warning] Could not set DPI awareness: {e}")

# --- ImGui + GLFW stack ---
import glfw
import OpenGL.GL as gl
import imgui
import numpy as np
from imgui.integrations.glfw import GlfwRenderer

import state as S
import globals as G
import style
import dx7_bridge

# Simple helper for colors: 0–255 -> ImGui RGBA (0–1)
def rgba_f(r, g, b, a=255):
    return r / 255.0, g / 255.0, b / 255.0, a / 255.0


def rgba_u32(r, g, b, a=255):
    """Convert 0–255 RGBA to ImGui packed color (for draw_list)."""
    return imgui.get_color_u32_rgba(*rgba_f(r, g, b, a))

# Drag state for pad circles
PAD_DRAG = {
    "active": False,     # whether a drag is in progress
    "idx": None,         # index of the preset being dragged
    "start_mouse": (0.0, 0.0),
    "start_tx_ty": (0.0, 0.0),  # normalized plane coords at drag start
}

def init_state():
    S.init_space(["freq1", "freq2", "freq3"], n_vectors=0)
    S.add_preset("Piano", (255, 205, 50))
    S.add_preset("Fiddle", (255, 105, 150))
    S.add_preset("Film", (255, 15, 250))

# ---------- PAD DRAWING (ImGui draw list) ----------
def draw_pad():
    
    # Top-left of the pad in screen coordinates
    pad_x, pad_y = imgui.get_cursor_screen_pos()
    pad_x2 = pad_x + G.PAD_W
    pad_y2 = pad_y + G.PAD_H

    draw_list = imgui.get_window_draw_list()

    # Background rounded rectangle
    bg_col = rgba_u32(36, 36, 36)
    border_col = rgba_u32(42, 42, 42)
    draw_list.add_rect_filled(pad_x, pad_y, pad_x2, pad_y2, bg_col, rounding=18)
    
    mouse_over_pad = imgui.is_mouse_hovering_rect(pad_x, pad_y, pad_x2, pad_y2)
    
    draw_list.add_rect(pad_x, pad_y, pad_x2, pad_y2, border_col, rounding=18, thickness=1.0)

    # --- Coordinate Transforms ---
    pad_inner_w = G.PAD_W - 2 * G.PAD_MARGIN
    pad_inner_h = G.PAD_H - 2 * G.PAD_MARGIN
    
    def unit_to_screen(u, v):
        su = (u + S.pad_offset[0]) * S.pad_zoom
        sv = ((1.0 - v) + S.pad_offset[1]) * S.pad_zoom
        sx = pad_x + G.PAD_MARGIN + su * pad_inner_w
        sy = pad_y + G.PAD_MARGIN + sv * pad_inner_h
        return sx, sy

    def screen_to_unit(sx, sy):
        su = (sx - (pad_x + G.PAD_MARGIN)) / pad_inner_w
        sv = (sy - (pad_y + G.PAD_MARGIN)) / pad_inner_h
        u = su / S.pad_zoom - S.pad_offset[0]
        v = 1.0 - (sv / S.pad_zoom - S.pad_offset[1])
        return u, v

    # --- Pan & Zoom Interaction ---
    io = imgui.get_io()
    if mouse_over_pad:
        # Zoom
        if io.mouse_wheel != 0:
            zoom_factor = 1.1 if io.mouse_wheel > 0 else 0.9
            mx, my = G.mouse_pos
            u_mouse, v_mouse = screen_to_unit(mx, my)
            
            S.pad_zoom *= zoom_factor
            
            # Adjust offset to keep mouse point stable
            su = (mx - (pad_x + G.PAD_MARGIN)) / pad_inner_w
            sv = (my - (pad_y + G.PAD_MARGIN)) / pad_inner_h
            
            new_off_x = su / S.pad_zoom - u_mouse
            new_off_y = sv / S.pad_zoom - (1.0 - v_mouse)
            S.pad_offset = (new_off_x, new_off_y)

        # Pan (Right Mouse or Middle Mouse)
        if imgui.is_mouse_down(1) or imgui.is_mouse_down(2):
            dx, dy = io.mouse_delta
            S.pad_offset = (
                S.pad_offset[0] + dx / (pad_inner_w * S.pad_zoom),
                S.pad_offset[1] + dy / (pad_inner_h * S.pad_zoom)
            )

    # Clip drawing to pad area
    draw_list.push_clip_rect(pad_x, pad_y, pad_x2, pad_y2, True)

    # --- 1. Draw Valid Slice Region ---
    poly_verts = S.get_slice_polygon_vertices()
    if len(poly_verts) > 2:
        screen_poly = []
        for u, v in poly_verts:
            sx, sy = unit_to_screen(u, v)
            screen_poly.append((sx, sy))
            
        # Draw filled polygon
        poly_col = rgba_u32(60, 60, 70, 100) 
        
        # Use path API for filled convex polygon
        draw_list.path_clear()
        for sx, sy in screen_poly:
            draw_list.path_line_to(sx, sy)
        draw_list.path_fill_convex(poly_col)
        
        # Draw outline
        outline_col = rgba_u32(100, 100, 120, 200)
        # add_polyline(points, color, closed=False, thickness=1.0) -> flags in older versions?
        # Checking docs/source, some versions use 'closed' as a positional or flags.
        # But to be safe, let's use path API for stroke too, or just pass positional args if we knew the signature.
        # Let's use path API for stroke as well, it's safer.
        draw_list.path_clear()
        for sx, sy in screen_poly:
            draw_list.path_line_to(sx, sy)
        draw_list.path_stroke(outline_col, flags=imgui.DRAW_CLOSED, thickness=1.5)

    # --- 2. Grid dots ---
    dot_col = rgba_u32(54, 54, 54)
    
    # Calculate visible range in unit space
    vis_u_min, vis_v_min = screen_to_unit(pad_x, pad_y2) # Bottom-left screen
    vis_u_max, vis_v_max = screen_to_unit(pad_x2, pad_y) # Top-right screen
    
    # Ensure min < max
    if vis_u_min > vis_u_max: vis_u_min, vis_u_max = vis_u_max, vis_u_min
    if vis_v_min > vis_v_max: vis_v_min, vis_v_max = vis_v_max, vis_v_min

    # Round to nearest grid step
    grid_step = 1.0 / 8.0 
    
    start_i = int(np.floor(vis_u_min / grid_step))
    end_i = int(np.ceil(vis_u_max / grid_step))
    start_j = int(np.floor(vis_v_min / grid_step))
    end_j = int(np.ceil(vis_v_max / grid_step))

    # Limit grid drawing to avoid freezing if zoomed out too much
    if (end_i - start_i) * (end_j - start_j) < 10000:
        for i in range(start_i, end_i + 1):
            for j in range(start_j, end_j + 1):
                u = i * grid_step
                v = j * grid_step
                
                if S.is_point_valid(u, v):
                    sx, sy = unit_to_screen(u, v)
                    draw_list.add_circle_filled(sx, sy, 2.0, dot_col)

    # --- Sample points (your projection) ---
    presets_2d, dists = S.get_presets_on_plane()  # shape (V, 2)
    if presets_2d is None:
        draw_list.pop_clip_rect()
        return
    white = rgba_u32(255, 255, 255)
    any_hovered = False

    for idx, ((tx, ty), dist, col) in enumerate(zip(presets_2d, dists, S.preset_colors)):
        x, y = unit_to_screen(tx, ty)
        
        selected: bool = idx in S.selection
        is_on_plane: bool = dist < 1e-5
        
        r = 8
        is_hovered = S.is_cursor_within_circle((x, y), r)
        if is_hovered:
            r += 2  # slightly larger on hover
            any_hovered = True
        
        if G.mouse_clicked and is_hovered:
            S.record_selection(idx)
        
        # Drag start: click on a hovered circle
        if is_hovered and G.mouse_down and not PAD_DRAG["active"]:          
            if not imgui.get_io().key_ctrl:  # hold Ctrl to multi-select
                PAD_DRAG["active"] = True
                PAD_DRAG["dragging"] = False
                PAD_DRAG["idx"] = idx
                PAD_DRAG["start_mouse"] = G.mouse_pos
                PAD_DRAG["start_tx_ty"] = (tx, ty)
                PAD_DRAG["start_value"] = S.Presets[idx, :].copy()

        # If this preset is the one being dragged, compute new position
        if PAD_DRAG["active"] and PAD_DRAG["idx"] == idx:
            if G.mouse_down:
                mx, my = G.mouse_pos
                sx, sy = PAD_DRAG["start_mouse"]
                dx = mx - sx
                dy = my - sy
                
                # Convert pixel delta into normalized pad delta (taking zoom into account)
                norm_dx = dx / (pad_inner_w * S.pad_zoom)
                norm_dy = -dy / (pad_inner_h * S.pad_zoom)  # Y is inverted
                
                new_tx = PAD_DRAG["start_tx_ty"][0] + norm_dx
                new_ty = PAD_DRAG["start_tx_ty"][1] + norm_dy
                # clamp 0..1
                new_tx = min(max(new_tx, 0.0), 1.0)
                new_ty = min(max(new_ty, 0.0), 1.0)
                
                if not PAD_DRAG["dragging"]:
                    dist_from_start = ((mx - sx) ** 2 + (my - sy) ** 2)
                    if dist_from_start > 1:
                        PAD_DRAG["dragging"] = True
                else:
                    # A. Get the Starting Real Value
                    start_real = PAD_DRAG["start_value"]
                    
                    # B. Convert Start Value to Normalized Space (0.0 to 1.0)
                    start_norm = S.to_unit(start_real, S.mins, S.maxs)
                    

                    # C. Calculate the Delta Vector in High-D Normalized Space
                    # This maps the 2D pad movement onto the high-D hypercube
                    # Basis vectors are usually unit-length in normalized space
                    delta_tx = norm_dx 
                    delta_ty = norm_dy 
                    
                    # Movement vector in N-dimensions
                    movement_nd = (S.Basis[0, :] * delta_tx) + (S.Basis[1, :] * delta_ty)

                    # D. Apply movement
                    target_norm = start_norm + movement_nd

                    # E. Clamp values to valid 0.0-1.0 range using ray casting to stop at edges
                    new_norm = S.clamp_movement(start_norm, target_norm)

                    # F. Convert back to Real Units
                    S.Presets[idx, :] = S.from_unit(new_norm, S.mins, S.maxs)
                    
            else:
                # mouse released -> end drag
                PAD_DRAG["active"] = False
                PAD_DRAG["dragging"] = False
                PAD_DRAG["idx"] = None

        if selected:
            # draw a line across the pad at the slider's value
            if S.hovered_parameter_slider != -1:
                slope_u, slope_v = S.get_slope_of_parameter_in_plane(S.hovered_parameter_slider)
                
                if not (slope_u == 0 and slope_v == 0):
                    line_col = rgba_u32(255, 130, 0)

                    # Draw line passing through (tx, ty) with slope m
                    # v - ty = m * (u - tx)
                    # We pick two points far away to ensure they cover the view
                    u1, u2 = -100.0, 100.0
                    
                    if abs(slope_u) < 1e-8:
                        # Vertical line at u = tx
                        sx1, sy1 = unit_to_screen(tx, -100.0)
                        sx2, sy2 = unit_to_screen(tx, 100.0)
                    else:
                        m = -slope_v / slope_u
                        v1 = ty + m * (u1 - tx)
                        v2 = ty + m * (u2 - tx)
                        sx1, sy1 = unit_to_screen(u1, v1)
                        sx2, sy2 = unit_to_screen(u2, v2)
                        
                    draw_list.add_line(sx1, sy1, sx2, sy2, line_col, thickness=2.0)
            
            dist_inv = 1.0 - dist
            dist_inv = round(dist_inv ** 5, 5)  # emphasize closeness
            
            draw_list.add_circle_filled(x, y, (r + 3) * dist_inv, white)

        dist_inv = 1.0 - dist
        dist_inv = round(dist_inv ** 5, 5) # emphasize closeness
        
        cr, cg, cb = col[:3]
        draw_list.add_circle_filled(x, y, r * dist_inv, rgba_u32(cr, cg, cb))
        
        if is_on_plane:
            draw_list.add_circle_filled(x, y, 2 * dist_inv, rgba_u32(255,255,255))

    # Mouse interaction for creating/selecting
    mouse_pad_x, mouse_pad_y = screen_to_unit(G.mouse_pos[0], G.mouse_pos[1])
    
    # Mouse is over pad
    if mouse_over_pad and not any_hovered:
        if G.mouse_clicked:
            S.active_preset_value = None
            S.selection = set()
        if G.mouse_down:
            S.active_preset_value = S.get_preset_from_coordinates(mouse_pad_x, mouse_pad_y)
            
            
    if S.selection == set() and S.active_preset_value is not None:
        (x, y), dist = S.project_point_on_plane(S.active_preset_value)
        px, py = unit_to_screen(x, y)
        r = 8
        is_on_plane: bool = dist < 1e-5
        
        draw_list.add_circle_filled(px, py, r + 3, white)
        draw_list.add_circle_filled(px, py, r, rgba_u32(155, 155, 155, 255))
        if is_on_plane:
            draw_list.add_circle_filled(x, y, 2 * dist_inv, rgba_u32(255,255,255))
        
    draw_list.pop_clip_rect()

# ---------- RIGHT PANEL HELPERS ----------
def header(text: str):
    imgui.text(text)
    imgui.separator()


def draw_preset_row(idx):
    """Simple horizontal row with a colored bullet and label."""
    name = S.preset_names[idx]
    color = S.preset_colors[idx]
    cr, cg, cb = color[:3]
    is_selected = idx in S.selection

    imgui.text_colored("o", *(c / 255.0 for c in (cr, cg, cb)), 1.0)
    imgui.same_line()
    # Invisible ID: '##' prefix makes the label hidden, but keeps IDs unique.
    clicked, _ = imgui.selectable(f"{name}##preset_{idx}", is_selected)
    if clicked:
        S.record_selection(idx)

def draw_inspector():
    # Top: current preset + sliders
    header(S.get_selection_name())
    
    if(S.selection is None or len(S.selection) == 0):
        if S.active_preset_value is None:
            imgui.text("No preset selected.")
            return
        else:
            selected_preset = S.active_preset_value
    elif(len(S.selection) == 3):
        # Button to create a new plane projection from three selected presets
        if imgui.button("Define plane from these 3 presets"):
            S.assign_basis_from_three_presets(list(S.selection))
        
        return
    elif(len(S.selection) > 1):
        imgui.text("Multiple presets selected.")
        return
    
    else:
        selected_idx = next(iter(S.selection))
        selected_preset = S.Presets[selected_idx, :]

    any_hovered = False
    
    for i in range(len(S.param_names)):
        param = S.param_names[i]
        min = S.mins[i]
        max = S.maxs[i] 
        
        
        imgui.text(param.capitalize())
        imgui.same_line()

        imgui.text(str(min))
        imgui.same_line()
        
        inspecting_unsaved_point: bool = (S.selection == set() and S.active_preset_value is not None)

        # Keep the slider compact and ID separate from label with '##'
        changed, new_val = imgui.slider_float(
            f"##{param}_slider",  # ImGui ID (label part hidden by '##')
            selected_preset[i] if not inspecting_unsaved_point else S.active_preset_value[i],
            min,
            max,
            ""  # empty format string -> no numeric text displayed
        )

        # Check if the last item (this slider) is hovered

        if imgui.is_item_hovered() | imgui.is_item_active():
            any_hovered = True
            S.hovered_parameter_slider = i
        if changed:
            if inspecting_unsaved_point: # unsaved active preset
                S.active_preset_value[i] = new_val
            else:
                S.Presets[selected_idx, i] = new_val

        imgui.same_line()
        imgui.text(str(max))

    if not any_hovered:
        S.hovered_parameter_slider = -1
    
    # "Add dimension" pill button
    if imgui.button("+##add_parameter", width=26, height=26):
        S.add_parameter(f"param{len(S.param_names)+1}")


def draw_presets():
        # Bottom: presets list
    header("Presets")
    for idx in range(len(S.preset_names)):
        draw_preset_row(idx)
    
    if S.selection == set() and S.active_preset_value is not None:
        # "Add preset" pill button
        if imgui.button("+##add_preset", width=26, height=26):
            print("Added new preset from unsaved active preset.")
            S.add_preset(f"preset {len(S.preset_names)+1}", value=S.active_preset_value)

# ---------- MAIN WINDOW BUILD ----------
def draw_main_window():
    # Fix position & size so it roughly matches your original layout
    imgui.set_next_window_position(12, 12)
    imgui.set_next_window_size(1260, 736)

    flags = (
        imgui.WINDOW_NO_TITLE_BAR
        | imgui.WINDOW_NO_MOVE
        | imgui.WINDOW_NO_RESIZE
    )

    imgui.begin("Slice Explorer UI", flags=flags)

    # LEFT: pad
    imgui.begin_child("pad_child", width=G.PAD_W, height=G.PAD_H, border=False)
    draw_pad()
    imgui.end_child()

    imgui.same_line()

    # RIGHT: panel
    imgui.begin_child("right_panel", width=340, height=G.PAD_H, border=False)
    draw_inspector()
    imgui.spacing()
    imgui.spacing()
    draw_presets()
    imgui.end_child()

    imgui.end()


# ---------- GLFW + ImGui loop ----------
def create_window():
    if not glfw.init():
        raise SystemExit("Could not initialize GLFW")

    # Basic OpenGL setup (pyimgui docs pattern)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(1280, 760, "Slice Explorer UI", None, None)
    if not window:
        glfw.terminate()
        raise SystemExit("Could not create window")

    glfw.make_context_current(window)
    return window


def main():
    
    
    # init_state()
    dx7_bridge.load_dx7_json("output.json")

    window = create_window()

    imgui.create_context()
    style.setup_style()
    impl = GlfwRenderer(window)

    gl.glClearColor(0.1, 0.1, 0.1, 1.0)
    
    sender = dx7_bridge.DX7OSCClient(ip="127.0.0.1", port=57120)

    # Main frame loop: everything is rebuilt every iteration.
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()
        G.update_globals()

        draw_main_window()

        # Render
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)
        
        # send OSC updates
        if S.active_preset_value is not None:
            sender.send_active_preset(S.active_preset_value)
            sender.send_gate(G.mouse_down)
        else: 
            sender.send_gate(False)
        
            

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()
