# pip install dearpygui
import dearpygui.dearpygui as dpg
from collections import OrderedDict
import random, math

# -----------------------
# Core model (tiny store)
# -----------------------
class NDStore:
	def __init__(self):
		self.dims = OrderedDict()		  # name -> {'min':float, 'max':float}
		self.vectors = {}				  # name -> {'vals':{dim:float}, 'color':(r,g,b), 'cu':float, 'cv':float}
		self.selection = set()			 # selected vector names
		# 2D basis in N-D (dynamic projection plane): dict dim->weight
		self.u = OrderedDict()			 # x-axis in N-D
		self.v = OrderedDict()			 # y-axis in N-D

	# ---- dimension helpers
	def add_dim(self, name, vmin=0.0, vmax=1.0):
		self.dims[name] = {'min': float(vmin), 'max': float(vmax)}
		# ensure basis carries this dim (default 0 weight)
		self.u.setdefault(name, 0.0)
		self.v.setdefault(name, 0.0)
		for vec in self.vectors.values():
			vec['vals'].setdefault(name, (vmin+vmax)/2)

	def set_dim_minmax(self, name, vmin=None, vmax=None):
		mm = self.dims[name]
		if vmin is not None: mm['min'] = float(vmin)
		if vmax is not None: mm['max'] = float(vmax)

	# ---- basis helpers
	def set_basis_by_dims(self, xdim, ydim):
		# zero all weights, then set unit weights on chosen dims (simple orthonormal)
		for k in self.dims.keys():
			self.u[k] = 1.0 if k == xdim else 0.0
			self.v[k] = 1.0 if k == ydim else 0.0
		self._reproject_all()

	def set_basis(self, u_weights: dict, v_weights: dict):
		# Accept arbitrary plane (you'll plug your "3 points -> plane" math here later)
		for k in self.dims.keys():
			self.u[k] = float(u_weights.get(k, 0.0))
			self.v[k] = float(v_weights.get(k, 0.0))
		self._normalize_basis()
		self._reproject_all()

	def _normalize_basis(self):
		# make u, v roughly orthonormal in L2 over dims
		def norm(vec): return math.sqrt(sum(w*w for w in vec.values()))
		def dot(a,b):  return sum(a[k]*b[k] for k in self.dims.keys())
		nu = norm(self.u) or 1.0
		for k in self.dims: self.u[k] /= nu
		# Gram–Schmidt for v
		proj = dot(self.v, self.u)
		for k in self.dims: self.v[k] -= proj * self.u[k]
		nv = norm(self.v) or 1.0
		for k in self.dims: self.v[k] /= nv

	# ---- vectors
	def add_vector(self, name=None, color=None):
		name = name or f"vec{len(self.vectors)+1}"
		if color is None:
			color = random.choice([
				(255, 77, 77), (92, 242, 214), (138, 255, 59),
				(255, 202, 40), (187, 134, 252), (255, 102, 204),
				(100, 181, 246)
			])
		vals = {k: (mm['min']+mm['max'])/2 for k, mm in self.dims.items()}
		self.vectors[name] = {'vals': vals, 'color': color, 'cu': 0.5, 'cv': 0.5}
		# compute initial (cu, cv) from projection of normalized vals
		self._update_coeffs_from_vals(name)

	def duplicate_vector(self, name):
		i = 1
		while f"{name}_copy{i}" in self.vectors: i += 1
		new = f"{name}_copy{i}"
		self.vectors[new] = {
			'vals': dict(self.vectors[name]['vals']),
			'color': self.vectors[name]['color'],
			'cu': self.vectors[name]['cu'],
			'cv': self.vectors[name]['cv']
		}
		return new

	def delete_vectors(self, names):
		for n in names:
			self.vectors.pop(n, None)
			self.selection.discard(n)

	# ---- N-D <-> 2-D projection math
	def _norm_val(self, dim, x):
		mm = self.dims[dim]
		if mm['max'] == mm['min']: return 0.5
		return (x - mm['min']) / (mm['max'] - mm['min'])

	def _denorm_val(self, dim, t):
		mm = self.dims[dim]
		return mm['min'] + t * (mm['max'] - mm['min'])

	def _proj(self, name):
		"""Return (x,y) in 0..1 from current vals using basis (u,v)."""
		vec = self.vectors[name]['vals']
		x = sum(self._norm_val(d, vec[d]) * self.u[d] for d in self.dims)
		y = sum(self._norm_val(d, vec[d]) * self.v[d] for d in self.dims)
		# clamp to 0..1 display space
		return max(0.0,min(1.0,x)), max(0.0,min(1.0,y))

	def _update_coeffs_from_vals(self, name):
		x,y = self._proj(name)
		self.vectors[name]['cu'] = x
		self.vectors[name]['cv'] = y

	def _apply_coeffs_to_vals(self, name):
		"""Reconstruct normalized vector from (cu,cv) along basis only (simple plane embedding)."""
		cu = self.vectors[name]['cu']; cv = self.vectors[name]['cv']
		# Build normalized values as linear combo in the plane (no orthogonal component)
		normed = {d: cu*self.u[d] + cv*self.v[d] for d in self.dims}
		# Clamp and denormalize
		for d in self.dims:
			t = max(0.0, min(1.0, normed[d]))
			self.vectors[name]['vals'][d] = self._denorm_val(d, t)

	def _reproject_all(self):
		for n in self.vectors.keys(): self._update_coeffs_from_vals(n)

# -----------------------
# App state + helpers
# -----------------------
S = NDStore()
for nm in ("freq1","freq2","freq3"):
	S.add_dim(nm, 0.0, 1.0)
S.set_basis_by_dims("freq1","freq2")
for _ in range(6):
	S.add_vector()

PAD_SIZE = (720, 540)
PAD_MARGIN = 24
POINT_RADIUS = 8
HIT_RADIUS = 12

pad_drawlist = None
vectors_list_id = None
selected_panel_id = None
min_labels = {}   # dim -> text item id (min)
max_labels = {}   # dim -> text item id (max)
slider_ids = {}   # dim -> slider id

def _to_pad_px(x01, y01):
	x0, y0 = PAD_MARGIN, PAD_MARGIN
	w, h = PAD_SIZE
	# flip y to match UI "up"
	x = x0 + x01 * (w - 2*PAD_MARGIN)
	y = y0 + (1.0 - y01) * (h - 2*PAD_MARGIN)
	return x, y

def _from_pad_px(x, y):
	x0, y0 = PAD_MARGIN, PAD_MARGIN
	w, h = PAD_SIZE
	tx = (x - x0) / (w - 2*PAD_MARGIN)
	ty = 1.0 - (y - y0) / (h - 2*PAD_MARGIN)
	return max(0,min(1,tx)), max(0,min(1,ty))

def _hit_test(mx, my):
	"""Return nearest vector name within HIT_RADIUS (in px) or None."""
	for name in reversed(list(S.vectors.keys())):
		x01, y01 = S.vectors[name]['cu'], S.vectors[name]['cv']
		px, py = _to_pad_px(x01, y01)
		if (mx-px)**2 + (my-py)**2 <= HIT_RADIUS**2:
			return name
	return None

# -----------------------
# UI: drawing + refresh
# -----------------------
def draw_pad():
	dpg.delete_item(pad_drawlist, children_only=True)

	# background & grid
	w,h = PAD_SIZE
	dpg.draw_rectangle((0,0), (w,h), color=(40,40,40), fill=(32,32,32), thickness=1, parent=pad_drawlist, rounding=10)
	# grid dots  (7x5 roughly)
	cols, rows = 12, 8
	for i in range(cols):
		for j in range(rows):
			gx = PAD_MARGIN + i*(w-2*PAD_MARGIN)/(cols-1)
			gy = PAD_MARGIN + j*(h-2*PAD_MARGIN)/(rows-1)
			dpg.draw_circle((gx,gy), 2, color=(60,60,60), fill=(60,60,60), parent=pad_drawlist)

	# points
	for name, data in S.vectors.items():
		px, py = _to_pad_px(data['cu'], data['cv'])
		col = data['color']
		sel = name in S.selection
		# selection ring (white) + core color
		if sel:
			dpg.draw_circle((px,py), POINT_RADIUS+3, color=(255,255,255), fill=(255,255,255), parent=pad_drawlist)
		dpg.draw_circle((px,py), POINT_RADIUS, color=col, fill=col, parent=pad_drawlist)

def refresh_vectors_list():
	dpg.delete_item(vectors_list_id, children_only=True)
	for name, data in S.vectors.items():
		with dpg.group(parent=vectors_list_id, horizontal=True):
			dpg.add_text("●", color=data['color'])
			sel = dpg.add_selectable(label=name, default_value=(name in S.selection),
									 user_data=name, callback=on_list_select)

def refresh_selected_panel():
	dpg.delete_item(selected_panel_id, children_only=True)
	# Sliders for a small subset (here: show all dims for simplicity)
	for dim, mm in S.dims.items():
		with dpg.group(parent=selected_panel_id, horizontal=True):
			# min label (editable on double click)
			min_lbl = dpg.add_text(f"{_fmt(mm['min'])}")
			min_labels[dim] = min_lbl
			_install_doubleclick(min_lbl, lambda s=dim: edit_minmax(s, True))

			# slider
			def slider_cb(sender, app_data, user_data):
				dim = user_data
				# write-through to all selected vectors
				for n in S.selection or []:
					S.vectors[n]['vals'][dim] = app_data
					S._update_coeffs_from_vals(n)
				draw_pad()
			# Mixed selection? We still show a slider; user motion overwrites all selected
			slider = dpg.add_slider_float(label=dim, width=180, min_value=mm['min'], max_value=mm['max'],
										  default_value=_common_value(dim), callback=slider_cb, user_data=dim)
			slider_ids[dim] = slider

			# max label (editable on double click)
			max_lbl = dpg.add_text(f"{_fmt(mm['max'])}")
			max_labels[dim] = max_lbl
			_install_doubleclick(max_lbl, lambda s=dim: edit_minmax(s, False))

	# tiny add button (for adding a new dimension)
	dpg.add_spacer(height=4, parent=selected_panel_id)
	dpg.add_button(label="+", width=26, height=26, callback=popup_add_dimension, parent=selected_panel_id)

def _common_value(dim):
	"""Return a representative value for slider display (first selected)."""
	if not S.selection:
		# no selection -> midpoint
		mm = S.dims[dim]
		return (mm['min']+mm['max'])/2
	first = next(iter(S.selection))
	return S.vectors[first]['vals'][dim]

def _fmt(x):
	# short pretty printing for min/max labels
	if abs(x) >= 1000 or (abs(x) < 0.01 and x != 0):
		return f"{x:.2e}"
	return f"{x:.3f}".rstrip('0').rstrip('.')

# -----------------------
# UI: interactions
# -----------------------
dragging = False
drag_origin = (0,0)
drag_target = None

def pad_mouse_down(sender, app_data):
	global dragging, drag_target, drag_origin
	if app_data[0] != 0:  # left button only for drag/select
		return
	mx, my = dpg.get_mouse_pos(local=True, viewport=False)
	# Transform to drawlist-local
	rx, ry = dpg.get_item_rect_min(pad_drawlist)
	mx -= rx; my -= ry
	hit = _hit_test(mx, my)
	ctrl = dpg.is_key_down(dpg.mvKey_Control)
	if hit:
		if ctrl:
			if hit in S.selection: S.selection.remove(hit)
			else: S.selection.add(hit)
		else:
			S.selection = {hit}
		dragging = True
		drag_target = hit
		drag_origin = (mx, my)
		refresh_vectors_list()
		refresh_selected_panel()
		draw_pad()
	else:
		# empty click: clear selection
		if not ctrl:
			S.selection.clear()
			refresh_vectors_list()
			refresh_selected_panel()
			draw_pad()

def pad_mouse_release(sender, app_data):
	global dragging, drag_target
	dragging = False
	drag_target = None

def pad_mouse_move(sender, app_data):
	if not dragging or not S.selection:
		return
	mx, my = dpg.get_mouse_pos(local=True, viewport=False)
	rx, ry = dpg.get_item_rect_min(pad_drawlist)
	mx -= rx; my -= ry
	tx, ty = _from_pad_px(mx, my)
	# Move ALL selected along the plane by setting (cu,cv)
	for name in list(S.selection):
		S.vectors[name]['cu'] = tx
		S.vectors[name]['cv'] = ty
		S._apply_coeffs_to_vals(name)
	# keep sliders in sync
	for dim, sid in slider_ids.items():
		dpg.configure_item(sid, default_value=_common_value(dim))
	draw_pad()

def pad_right_click(sender, app_data):
	mx, my = dpg.get_mouse_pos(local=True, viewport=False)
	rx, ry = dpg.get_item_rect_min(pad_drawlist)
	mx -= rx; my -= ry
	hit = _hit_test(mx, my)
	if hit:
		open_vector_menu(hit)
	else:
		open_canvas_menu()

def on_list_select(sender, app_data, user_data):
	name = user_data
	if app_data: S.selection.add(name)
	else: S.selection.discard(name)
	draw_pad()
	refresh_selected_panel()

def key_handler(sender, app_data):
	key = app_data
	if key in (dpg.mvKey_Delete, dpg.mvKey_Back):
		if S.selection:
			S.delete_vectors(list(S.selection))
			S.selection.clear()
			refresh_vectors_list()
			refresh_selected_panel()
			draw_pad()
	elif key == dpg.mvKey_A and dpg.is_key_down(dpg.mvKey_Control):
		S.selection = set(S.vectors.keys())
		refresh_vectors_list(); refresh_selected_panel(); draw_pad()
	elif key == dpg.mvKey_Escape:
		S.selection.clear()
		refresh_vectors_list(); refresh_selected_panel(); draw_pad()
	elif key in (dpg.mvKey_Left, dpg.mvKey_Right, dpg.mvKey_Up, dpg.mvKey_Down):
		if not S.selection: return
		step = 0.005 * (5 if dpg.is_key_down(dpg.mvKey_Shift) else 1)
		dx = (key == dpg.mvKey_Right) - (key == dpg.mvKey_Left)
		dy = (key == dpg.mvKey_Up) - (key == dpg.mvKey_Down)
		for n in S.selection:
			S.vectors[n]['cu'] = min(1,max(0,S.vectors[n]['cu'] + dx*step))
			S.vectors[n]['cv'] = min(1,max(0,S.vectors[n]['cv'] + dy*step))
			S._apply_coeffs_to_vals(n)
		# sync sliders
		for dim, sid in slider_ids.items():
			dpg.configure_item(sid, default_value=_common_value(dim))
		draw_pad()

# -----------------------
# Context menus & popups
# -----------------------
def open_canvas_menu():
	with dpg.window(label="Canvas", modal=False, popup=True, no_title_bar=True, no_move=True, autosize=True) as w:
		dpg.add_button(label="Add vector", callback=lambda: (S.add_vector(), close_popup(w)))
		dpg.add_separator()
		dpg.add_text("Basis (align X/Y to dim)")
		dims = list(S.dims.keys())
		if len(dims)>=2:
			xdim = dpg.add_combo(dims, default_value=dims[0])
			ydim = dpg.add_combo(dims, default_value=dims[1])
			def apply_basis():
				S.set_basis_by_dims(dpg.get_value(xdim), dpg.get_value(ydim))
				draw_pad(); close_popup(w)
			dpg.add_button(label="Apply", callback=apply_basis)
	# position under mouse
	dpg.set_item_pos(w, dpg.get_mouse_pos())

def open_vector_menu(name):
	with dpg.window(label=name, modal=False, popup=True, no_title_bar=True, no_move=True, autosize=True) as w:
		dpg.add_text(f"{name}")
		dpg.add_separator()
		dpg.add_button(label="Rename…", callback=lambda: (popup_rename(name), close_popup(w)))
		dpg.add_button(label="Duplicate", callback=lambda: (S.duplicate_vector(name), refresh_vectors_list(), draw_pad(), close_popup(w)))
		dpg.add_button(label="Delete", callback=lambda: (S.delete_vectors([name]), refresh_vectors_list(), draw_pad(), close_popup(w)))
	dpg.set_item_pos(w, dpg.get_mouse_pos())

def close_popup(w):
	if dpg.does_item_exist(w):
		dpg.delete_item(w)

def popup_rename(old):
	with dpg.window(label="Rename", modal=True, no_close=True, autosize=True) as w:
		inp = dpg.add_input_text(label="New name", default_value=old)
		def apply():
			new = dpg.get_value(inp).strip()
			if new and new not in S.vectors:
				S.vectors[new] = S.vectors.pop(old)
				if old in S.selection:
					S.selection.remove(old); S.selection.add(new)
				refresh_vectors_list(); draw_pad()
			close_popup(w)
		dpg.add_button(label="OK", callback=apply)
		dpg.add_same_line(); dpg.add_button(label="Cancel", callback=lambda: close_popup(w))

def popup_add_dimension():
	with dpg.window(label="Add Dimension", modal=True, autosize=True) as w:
		name = dpg.add_input_text(label="Name")
		vmin = dpg.add_input_float(label="Min", default_value=0.0)
		vmax = dpg.add_input_float(label="Max", default_value=1.0)
		def apply():
			nm = dpg.get_value(name).strip()
			if nm and nm not in S.dims:
				S.add_dim(nm, dpg.get_value(vmin), dpg.get_value(vmax))
				refresh_selected_panel(); draw_pad()
			close_popup(w)
		dpg.add_button(label="Add", callback=apply)
		dpg.add_same_line(); dpg.add_button(label="Cancel", callback=lambda: close_popup(w))

def _install_doubleclick(item_id, cb):
	with dpg.item_handler_registry() as h:
		dpg.add_item_double_clicked_handler(callback=lambda s,a,u: cb())
	dpg.bind_item_handler_registry(item_id, h)

def edit_minmax(dim, edit_min: bool):
	label = "Edit min" if edit_min else "Edit max"
	with dpg.window(label=label, modal=True, autosize=True) as w:
		cur = S.dims[dim]['min' if edit_min else 'max']
		f = dpg.add_input_float(label=f"{dim} {'min' if edit_min else 'max'}", default_value=cur, step=0.0)
		def apply():
			val = dpg.get_value(f)
			if edit_min:
				S.set_dim_minmax(dim, vmin=val)
			else:
				S.set_dim_minmax(dim, vmax=val)
			# Update slider bounds and labels
			mm = S.dims[dim]
			dpg.configure_item(slider_ids[dim], min_value=mm['min'], max_value=mm['max'])
			dpg.configure_item(min_labels[dim], default_value=_fmt(mm['min']))
			dpg.configure_item(max_labels[dim], default_value=_fmt(mm['max']))
			# Reproject to keep cu/cv coherent
			S._reproject_all()
			draw_pad()
			close_popup(w)
		dpg.add_button(label="OK", callback=apply)
		dpg.add_same_line(); dpg.add_button(label="Cancel", callback=lambda: close_popup(w))

# -----------------------
# Build UI
# -----------------------
dpg.create_context()
dpg.create_viewport(title="N-D Explorer (2D slice)", width=1100, height=700)

with dpg.handler_registry():
	dpg.add_key_press_handler(callback=key_handler)
    # call pad_mouse_release whenever *any* button is released
	dpg.add_mouse_release_handler(button=0, callback=pad_mouse_release)  # left up
	dpg.add_mouse_release_handler(button=1, callback=pad_mouse_release)  # right up (optional)
	dpg.add_mouse_release_handler(button=2, callback=pad_mouse_release)  # middle up (optional)


# Window 1: PAD
with dpg.window(label="", pos=(20,20), width=800, height=660, no_title_bar=True, no_resize=True, no_move=True):
	dpg.add_text("")  # spacer
	with dpg.drawlist(width=PAD_SIZE[0], height=PAD_SIZE[1]) as pad_drawlist:
		pass
	# mouse handlers
	with dpg.item_handler_registry() as pad_handlers:
		dpg.add_item_clicked_handler(button=0, callback=pad_mouse_down)   # left click on pad
		dpg.add_item_clicked_handler(button=1, callback=pad_right_click)  # right click on pad
		dpg.add_item_hover_handler(callback=pad_mouse_move)			   # drag while hovering
	dpg.bind_item_handler_registry(pad_drawlist, pad_handlers)


# Window 2: Inspector (right column)
with dpg.window(label="", pos=(840,20), width=240, height=660, no_title_bar=True, no_resize=True, no_move=True):
	dpg.add_text("Selected"); dpg.add_separator()
	selected_panel_id = dpg.add_group()
	dpg.add_spacer(height=10)
	dpg.add_separator()
	dpg.add_text("Vectors"); dpg.add_separator()
	vectors_list_id = dpg.add_group()

# First paint
refresh_vectors_list()
refresh_selected_panel()
draw_pad()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(dpg.last_container(), True)
dpg.start_dearpygui()
dpg.destroy_context()
