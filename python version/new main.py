# pip install dearpygui
from tkinter import font
import dearpygui.dearpygui as dpg

PAD_W, PAD_H = 860, 600
PAD_MARGIN = 26

COLORS = [(176, 240, 71, 255),   # lime
(255, 205, 50, 255),   # yellow
(255, 102, 204, 255),  # pink
(187, 134, 252, 255),  # purple
(92, 242, 214, 255),   # aqua
(255, 77, 77, 255),	# red
(100, 181, 246, 255)]   # blue


# --------- THEME ----------
def build_theme():
	with dpg.theme(tag="app_theme"):
		with dpg.theme_component(dpg.mvAll):
			# Global style
			dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
			dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
			dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
			dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 8)
			dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
			dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10)
			dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
			dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)

			# Dark palette
			BG = (24,24,24,255)
			Panel = (30,30,30,255)
			Frame = (44,44,44,255)
			Hover = (56,56,56,255)
			Active= (72,72,72,255)
			Text = (230,230,230,255)
			Muted= (160,160,160,255)
			Accent= (255,180,40,255)  # for selected halo, buttons

			# windows / panels
			dpg.add_theme_color(dpg.mvThemeCol_WindowBg, BG)
			dpg.add_theme_color(dpg.mvThemeCol_ChildBg, Panel)
			dpg.add_theme_color(dpg.mvThemeCol_PopupBg, Panel)

			# text
			dpg.add_theme_color(dpg.mvThemeCol_Text, Text)
			dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, Muted)

			# frames & widgets
			dpg.add_theme_color(dpg.mvThemeCol_FrameBg, Frame)
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, Hover)
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, Active)
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (180,180,180,255))
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (220,220,220,255))
			dpg.add_theme_color(dpg.mvThemeCol_Button, (60,60,60,255))
			dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90,90,90,255))
			dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, Active)
			dpg.add_theme_color(dpg.mvThemeCol_Header, (58,58,58,255))
			dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (82,82,82,255))
			dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, Active)
			dpg.add_theme_color(dpg.mvThemeCol_Separator, (70,70,70,255))
   
		with dpg.font_registry():
			font = dpg.add_font("C:/Windows/Fonts/SegoeUI.ttf", 18)  # or Inter/Roboto
   
	dpg.bind_theme("app_theme")
	dpg.bind_font(font)

# --------- PAD DRAWING ----------
def draw_pad(drawlist, dots=True):
	dpg.delete_item(drawlist, children_only=True)
	# rounded container
	dpg.draw_rectangle((0,0), (PAD_W,PAD_H), fill=(36,36,36,255),
					   color=(42,42,42,255), rounding=18, thickness=1.0, parent=drawlist)
	# subtle grid dots
	if dots:
		cols, rows = 12, 8
		for i in range(cols):
			for j in range(rows):
				gx = PAD_MARGIN + i*(PAD_W-2*PAD_MARGIN)/(cols-1)
				gy = PAD_MARGIN + j*(PAD_H-2*PAD_MARGIN)/(rows-1)
				dpg.draw_circle((gx,gy), 2, color=(54,54,54,255),
								fill=(54,54,54,255), parent=drawlist)

	# --- SAMPLE POINTS (replace with your projection) ---
	points = [
		((0.70, 0.62), (176, 240, 71, 255)),   # lime
		((0.56, 0.44), (255, 205, 50, 255)),   # yellow (selected)
		((0.40, 0.40), (255, 102, 204, 255)),  # pink
		((0.31, 0.34), (187, 134, 252, 255)),  # purple
		((0.20, 0.28), (92, 242, 214, 255)),   # aqua
		((0.18, 0.16), (255, 77, 77, 255)),	# red
		((0.28, 0.74), (100, 181, 246, 255)),  # blue
	]
	r = 8
	sel_index = 1  # pretend the yellow one is selected
	for idx, ((tx,ty), col) in enumerate(points):
		x = PAD_MARGIN + tx*(PAD_W-2*PAD_MARGIN)
		y = PAD_MARGIN + (1-ty)*(PAD_H-2*PAD_MARGIN)
		if idx == sel_index:
			dpg.draw_circle((x,y), r+3, color=(255,255,255,255),
							fill=(255,255,255,255), parent=drawlist)
		dpg.draw_circle((x,y), r, color=col, fill=col, parent=drawlist)

# --------- RIGHT PANEL WIDGETS ----------
def header(text):
	# bold header like “Piano” / “Presets”
	dpg.add_text(text, bullet=False)
	last = dpg.last_item()
	dpg.bind_item_theme(last, "h_theme")
	dpg.add_separator()

def pill_button(label="+"):
	dpg.add_button(label=label, width=26, height=26)
	dpg.bind_item_theme(dpg.last_item(), "pill_theme")

def build_header_theme():
	with dpg.theme(tag="h_theme"):
		with dpg.theme_component(dpg.mvText):
			dpg.add_theme_color(dpg.mvThemeCol_Text, (245,245,245,255))
	with dpg.theme(tag="pill_theme"):
		with dpg.theme_component(dpg.mvButton):
			dpg.add_theme_color(dpg.mvThemeCol_Button, (255,128,40,255))
			dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255,160,80,255))
			dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255,180,108,255))
			dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)

# --------- PRESET ROW ----------
def preset_row(name, rgba):
	with dpg.group(horizontal=True):
		dpg.add_text("●", color=rgba)   # colored bullet
		dpg.add_text(name)

# --------- APP SKELETON ----------
dpg.create_context()
dpg.create_viewport(title="Slice Explorer UI", width=1280, height=760)

build_theme()
build_header_theme()

with dpg.window(no_title_bar=True, no_move=True, no_resize=True, pos=(12,12), width=1260, height=736):
	with dpg.group(horizontal=True):
		# LEFT: PAD
		with dpg.group():
			with dpg.drawlist(width=PAD_W, height=PAD_H, tag="pad_dl"):
				pass
			draw_pad("pad_dl")

		# RIGHT: PANEL
		with dpg.child_window(width=340, height=PAD_H):
			# Top section: current preset name + sliders
			header("Piano")
			# Three sliders with editable min/max labels (stub visuals)
			for dim in ["freq1","freq2","freq3"]:
				with dpg.group(horizontal=True):
					dpg.add_text("0")		  # min label (you'll hook double-click edit)
					dpg.add_slider_float(label=dim, width=210, min_value=0.0, max_value=1.0, format="")  # hide numeric text
					dpg.add_text("1")		  # max label
			dpg.add_separator()
			pill_button("+")  # add dimension

			dpg.add_spacer(height=16)
			# Bottom section: presets list
			header("Presets")
			preset_row("808",		 (255, 77, 77, 255))
			preset_row("String",	  (176, 240, 71, 255))
			preset_row("Piano",	   (255, 205, 50, 255))
			preset_row("Terminator",  (187, 134, 252, 255))
			preset_row("Home",		(255, 102, 204, 255))
			preset_row("Speak Out",   (92, 242, 214, 255))
			preset_row("Jam",		 (100, 181, 246, 255))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
