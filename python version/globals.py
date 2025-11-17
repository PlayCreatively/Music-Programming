
PAD_W, PAD_H = 860, 600
PAD_MARGIN = 26

COLORS = [(176, 240, 71, 255),   # lime
(255, 205, 50, 255),   # yellow
(255, 102, 204, 255),  # pink
(187, 134, 252, 255),  # purple
(92, 242, 214, 255),   # aqua
(255, 77, 77, 255),	# red
(100, 181, 246, 255)]   # blue

import imgui
mouse_pos: tuple[float, float]
mouse_down: bool
mouse_clicked: bool


def update_globals():
	"""Update any globals that depend on mouse position."""
	global mouse_pos, mouse_down, mouse_clicked
	mouse_pos = imgui.get_mouse_pos()
	mouse_down = imgui.is_mouse_down(0)
	mouse_clicked = imgui.is_mouse_clicked(0)