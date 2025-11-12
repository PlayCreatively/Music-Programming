import dearpygui.dearpygui as dpg


class CustomSlider:
	def __init__(
		self,
		label: str,
		min_value: float = 0.0,
		max_value: float = 1.0,
		default_value: float = 0.5,
		width: int = 250,
		height: int = 40,
		callback=None,
		user_data=None,
		parent=None,
	):
		self.min = min_value
		self.max = max_value
		self.value = float(default_value)
		self.callback = callback
		self.user_data = user_data
		self.width = width
		self.height = height
		self.margin = 15  # horizontal padding inside drawlist

		with dpg.group(parent=parent):
			dpg.add_text(label)
			self.drawlist = dpg.add_drawlist(width=width, height=height)

		# Draw static bar
		mid_y = height * 0.5
		self.bar_tag = dpg.draw_rectangle(
			(self.margin, mid_y - 3),
			(width - self.margin, mid_y + 3),
			parent=self.drawlist,
			fill=(80, 80, 80, 255),
			color=(40, 40, 40, 255),
			thickness=1,
		)

		# Draw knob (we'll move this when value changes)
		self.knob_tag = dpg.draw_circle(
			(0, mid_y),
			radius=8,
			parent=self.drawlist,
			fill=(200, 200, 200, 255),
			color=(30, 30, 30, 255),
			thickness=1,
		)

		# Handlers: click and drag on the drawlist
		with dpg.item_handler_registry() as self.handlers:
			dpg.add_item_clicked_handler(callback=self._on_click_or_drag)
			dpg.add_item_active_handler(callback=self._on_click_or_drag)

		dpg.bind_item_handler_registry(self.drawlist, self.handlers)

		# Initial position
		self._update_knob_from_value()

	# --- public API -------------------------------------------------
	def get_value(self) -> float:
		return self.value

	def set_value(self, v: float):
		self.value = max(self.min, min(self.max, float(v)))
		self._update_knob_from_value()
		self._fire_callback()

	# --- internal helpers -------------------------------------------
	def _value_to_pos(self) -> float:
		"""Map current value to x position in drawlist coords."""
		t = (self.value - self.min) / (self.max - self.min) if self.max != self.min else 0.0
		t = max(0.0, min(1.0, t))
		x0 = self.margin
		x1 = self.width - self.margin
		return x0 + t * (x1 - x0)

	def _pos_to_value(self, x: float) -> float:
		"""Map mouse x position (in drawlist coords) to value."""
		x0 = self.margin
		x1 = self.width - self.margin
		# Clamp
		x_clamped = max(x0, min(x1, x))
		t = (x_clamped - x0) / (x1 - x0)
		return self.min + t * (self.max - self.min)

	def _update_knob_from_value(self):
		mid_y = self.height * 0.5
		x = self._value_to_pos()
		dpg.configure_item(self.knob_tag, center=(x, mid_y))

	def _on_click_or_drag(self, sender, app_data, user_data):
		# Mouse pos in this drawlist's coordinate space
		mx, my = dpg.get_drawing_mouse_pos()
		self.value = self._pos_to_value(mx)
		self._update_knob_from_value()
		self._fire_callback()

	def _fire_callback(self):
		if self.callback is not None:
			# Match Dear PyGui style: sender, app_data, user_data
			self.callback(self, self.value, self.user_data)
			
			
			
def build_custom_slider_theme():
	"""
	Creates a theme to make sliders look different.
	We can apply this to all sliders or just one.
	"""
	with dpg.theme(tag="custom_slider_theme"):
		with dpg.theme_component(dpg.mvSliderFloat):
			# --- Colors ---
			# The background of the slider track
			dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40))
			# The track color *when active* (being dragged)
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (45, 45, 45))
			# The track color *when hovered*
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (45, 45, 45))
			
			# The color of the "grab" (the handle)
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (255, 130, 0))
			# The color of the grab when active (being dragged)
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (255, 160, 60))

			# --- Styles ---
			# How round the grab is (a high value makes it a circle)
			dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 12)
			# How round the track is
			dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
			# The *minimum* size of the grab
			dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 10)
			
			# You can also adjust padding, border, etc.
			dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)

