import imgui

def setup_style():
    """Dark theme for ImGui."""
    style = imgui.get_style()

    # Style numbers are just floats; tuples/lists are 2D vectors.
    style.window_rounding = 10
    style.frame_rounding = 6
    style.child_rounding = 12
    style.grab_rounding = 6
    style.window_padding = (10, 10)
    style.item_spacing = (8, 6)
    style.frame_padding = (8, 6)

    colors = style.colors
    colors[imgui.COLOR_WINDOW_BACKGROUND] = rgba_f(24, 24, 24)
    colors[imgui.COLOR_CHILD_BACKGROUND] = rgba_f(30, 30, 30)
    colors[imgui.COLOR_POPUP_BACKGROUND] = rgba_f(30, 30, 30)

    colors[imgui.COLOR_TEXT] = rgba_f(230, 230, 230)
    colors[imgui.COLOR_TEXT_DISABLED] = rgba_f(160, 160, 160)

    colors[imgui.COLOR_FRAME_BACKGROUND] = rgba_f(44, 44, 44)
    colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = rgba_f(56, 56, 56)
    colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = rgba_f(72, 72, 72)

    colors[imgui.COLOR_BUTTON] = rgba_f(60, 60, 60)
    colors[imgui.COLOR_BUTTON_HOVERED] = rgba_f(90, 90, 90)
    colors[imgui.COLOR_BUTTON_ACTIVE] = rgba_f(72, 72, 72)

    colors[imgui.COLOR_HEADER] = rgba_f(58, 58, 58)
    colors[imgui.COLOR_HEADER_HOVERED] = rgba_f(82, 82, 82)
    colors[imgui.COLOR_HEADER_ACTIVE] = rgba_f(72, 72, 72)

    colors[imgui.COLOR_SEPARATOR] = rgba_f(70, 70, 70)
    colors[imgui.COLOR_SLIDER_GRAB] = rgba_f(180, 180, 180)
    colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = rgba_f(220, 220, 220)
    
# Simple helper for colors: 0–255 -> ImGui RGBA (0–1)
def rgba_f(r, g, b, a=255):
    return r / 255.0, g / 255.0, b / 255.0, a / 255.0


def rgba_u32(r, g, b, a=255):
    """Convert 0–255 RGBA to ImGui packed color (for draw_list)."""
    return imgui.get_color_u32_rgba(*rgba_f(r, g, b, a))
