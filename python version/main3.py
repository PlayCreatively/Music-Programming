from __future__ import annotations
import math, random, sys
from collections import OrderedDict
from typing import Dict, Set, Tuple

from PySide6 import QtCore, QtGui, QtWidgets

# -----------------------
# Tiny N-D data store
# -----------------------
Color = Tuple[int, int, int]

class NDStore(QtCore.QObject):
	changed = QtCore.Signal()

	def __init__(self):
		super().__init__()
		self.dims: OrderedDict[str, Dict[str, float]] = OrderedDict()  # name -> {'min':, 'max':}
		self.vectors: Dict[str, Dict] = {}  # name -> {'vals':{dim:float}, 'color':(r,g,b), 'cu':float, 'cv':float}
		self.selection: Set[str] = set()
		self.u: OrderedDict[str, float] = OrderedDict()  # x-basis weights over dims
		self.v: OrderedDict[str, float] = OrderedDict()  # y-basis weights over dims

	# ---- dimensions
	def add_dim(self, name: str, vmin=0.0, vmax=1.0):
		if name in self.dims: return
		self.dims[name] = {'min': float(vmin), 'max': float(vmax)}
		self.u.setdefault(name, 0.0)
		self.v.setdefault(name, 0.0)
		for vec in self.vectors.values():
			vec['vals'].setdefault(name, (vmin+vmax)/2)
		self._reproject_all()
		self.changed.emit()

	def set_dim_min(self, name: str, v: float):
		self.dims[name]['min'] = float(v); self._reproject_all(); self.changed.emit()

	def set_dim_max(self, name: str, v: float):
		self.dims[name]['max'] = float(v); self._reproject_all(); self.changed.emit()

	# ---- basis (dynamic plane)
	def set_basis_by_dims(self, xdim: str, ydim: str):
		for d in self.dims:
			self.u[d] = 1.0 if d == xdim else 0.0
			self.v[d] = 1.0 if d == ydim else 0.0
		self._normalize_basis()
		self._reproject_all()
		self.changed.emit()

	def set_basis(self, u_weights: Dict[str, float], v_weights: Dict[str, float]):
		for d in self.dims:
			self.u[d] = float(u_weights.get(d, 0.0))
			self.v[d] = float(v_weights.get(d, 0.0))
		self._normalize_basis()
		self._reproject_all()
		self.changed.emit()

	def _normalize_basis(self):
		def norm(vec): return math.sqrt(sum(vec[d]*vec[d] for d in self.dims))
		def dot(a,b):  return sum(a[d]*b[d] for d in self.dims)
		n = norm(self.u) or 1.0
		for d in self.dims: self.u[d] /= n
		proj = dot(self.v, self.u)
		for d in self.dims: self.v[d] -= proj * self.u[d]
		n2 = norm(self.v) or 1.0
		for d in self.dims: self.v[d] /= n2

	# ---- vectors
	def add_vector(self, name: str|None=None, color: Color|None=None):
		if not self.dims: return
		name = name or f"vec{len(self.vectors)+1}"
		if name in self.vectors:
			i = 1
			while f"{name}_{i}" in self.vectors: i += 1
			name = f"{name}_{i}"
		color = color or random.choice([
			(255,77,77),(92,242,214),(138,255,59),(255,202,40),(187,134,252),(255,102,204),(100,181,246)
		])
		vals = {d:(mm['min']+mm['max'])/2 for d,mm in self.dims.items()}
		self.vectors[name] = {'vals': vals, 'color': color, 'cu': 0.5, 'cv': 0.5}
		self._update_coeffs_from_vals(name)
		self.changed.emit()

	def duplicate_vector(self, name: str):
		if name not in self.vectors: return
		base = name + "_copy"
		i = 1
		while f"{base}{i}" in self.vectors: i += 1
		new = f"{base}{i}"
		self.vectors[new] = {
			'vals': dict(self.vectors[name]['vals']),
			'color': self.vectors[name]['color'],
			'cu': self.vectors[name]['cu'],
			'cv': self.vectors[name]['cv'],
		}
		self.changed.emit()

	def delete_selected(self):
		for n in list(self.selection):
			self.vectors.pop(n, None)
		self.selection.clear()
		self.changed.emit()

	# ---- math helpers
	def _norm(self, dim: str, x: float) -> float:
		mm = self.dims[dim]
		if mm['max'] == mm['min']: return 0.5
		return (x - mm['min']) / (mm['max'] - mm['min'])

	def _denorm(self, dim: str, t: float) -> float:
		mm = self.dims[dim]
		return mm['min'] + t * (mm['max'] - mm['min'])

	def _proj(self, name: str) -> Tuple[float,float]:
		vec = self.vectors[name]['vals']
		x = sum(self._norm(d, vec[d]) * self.u[d] for d in self.dims)
		y = sum(self._norm(d, vec[d]) * self.v[d] for d in self.dims)
		return max(0.0,min(1.0,x)), max(0.0,min(1.0,y))

	def _update_coeffs_from_vals(self, name: str):
		x,y = self._proj(name)
		self.vectors[name]['cu'] = x
		self.vectors[name]['cv'] = y

	def _apply_coeffs_to_vals(self, name: str):
		cu = self.vectors[name]['cu']; cv = self.vectors[name]['cv']
		normed = {d: cu*self.u[d] + cv*self.v[d] for d in self.dims}
		for d in self.dims:
			t = max(0.0, min(1.0, normed[d]))
			self.vectors[name]['vals'][d] = self._denorm(d, t)

	def _reproject_all(self):
		for n in self.vectors.keys(): self._update_coeffs_from_vals(n)

# -----------------------
# Pad widget (2D view)
# -----------------------
class PadWidget(QtWidgets.QWidget):
	pointRadius = 7
	hitRadius   = 11
	margin	  = 22

	def __init__(self, store: NDStore, parent=None):
		super().__init__(parent)
		self.setMinimumSize(720, 540)
		self.setMouseTracking(True)
		self.store = store
		self.dragging = False
		self.lastMouse = QtCore.QPointF()
		self.store.changed.connect(self.update)

	# coords
	def _to_px(self, tx: float, ty: float) -> QtCore.QPointF:
		w,h = self.width(), self.height()
		x0,y0 = self.margin, self.margin
		x = x0 + tx * (w-2*self.margin)
		y = y0 + (1.0-ty) * (h-2*self.margin)
		return QtCore.QPointF(x,y)

	def _from_px(self, p: QtCore.QPointF) -> Tuple[float,float]:
		w,h = self.width(), self.height()
		x0,y0 = self.margin, self.margin
		tx = (p.x()-x0)/(w-2*self.margin)
		ty = 1.0 - (p.y()-y0)/(h-2*self.margin)
		return max(0.0,min(1.0,tx)), max(0.0,min(1.0,ty))

	def _hit(self, p: QtCore.QPointF) -> str|None:
		r2 = self.hitRadius*self.hitRadius
		for name in reversed(list(self.store.vectors.keys())):
			v = self.store.vectors[name]
			pp = self._to_px(v['cu'], v['cv'])
			if (pp-p).manhattanLength()**2 <= r2:  # cheap-ish test
				# refine with Euclidean
				if QtGui.QVector2D(pp-p).length() <= self.hitRadius: return name
		return None

	# painting
	def paintEvent(self, e):
		qp = QtGui.QPainter(self)
		qp.setRenderHint(QtGui.QPainter.Antialiasing, True)

		# bg
		qp.fillRect(self.rect(), QtGui.QColor(32,32,32))
		rect = self.rect().adjusted(0,0,-1,-1)
		pen = QtGui.QPen(QtGui.QColor(40,40,40), 1)
		qp.setPen(pen)
		qp.drawRoundedRect(rect, 10, 10)

		# grid dots
		cols, rows = 12, 8
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(60,60,60))
		for i in range(cols):
			for j in range(rows):
				gx = self.margin + i*(self.width()-2*self.margin)/(cols-1)
				gy = self.margin + j*(self.height()-2*self.margin)/(rows-1)
				qp.drawEllipse(QtCore.QPointF(gx,gy), 2,2)

		# points
		for name, data in self.store.vectors.items():
			px = self._to_px(data['cu'], data['cv'])
			col = QtGui.QColor(*data['color'])
			if name in self.store.selection:
				qp.setBrush(QtGui.QColor(255,255,255))
				qp.setPen(QtCore.Qt.NoPen)
				qp.drawEllipse(px, self.pointRadius+3, self.pointRadius+3)
			qp.setBrush(col)
			qp.setPen(QtCore.Qt.NoPen)
			qp.drawEllipse(px, self.pointRadius, self.pointRadius)

	# interaction
	def mousePressEvent(self, ev: QtGui.QMouseEvent):
		if ev.button() == QtCore.Qt.LeftButton:
			hit = self._hit(ev.position())
			ctrl = ev.modifiers() & QtCore.Qt.ControlModifier
			if hit:
				if ctrl:
					if hit in self.store.selection: self.store.selection.remove(hit)
					else: self.store.selection.add(hit)
				else:
					self.store.selection = {hit}
				self.dragging = True
				self.lastMouse = ev.position()
				self.store.changed.emit()
			else:
				if not ctrl:
					self.store.selection.clear()
					self.store.changed.emit()
		elif ev.button() == QtCore.Qt.RightButton:
			self._open_context(ev.position())

	def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
		if self.dragging and self.store.selection:
			tx, ty = self._from_px(ev.position())
			for n in list(self.store.selection):
				vec = self.store.vectors[n]
				vec['cu'] = tx; vec['cv'] = ty
				self.store._apply_coeffs_to_vals(n)
			self.store.changed.emit()

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
		if ev.button() == QtCore.Qt.LeftButton:
			self.dragging = False

	def keyPressEvent(self, ev: QtGui.QKeyEvent):
		# In case pad has focus; main window also handles keys globally
		self.parent().keyPressEvent(ev)

	# context menu
	def _open_context(self, posLocal: QtCore.QPointF):
		name = self._hit(posLocal)
		menu = QtWidgets.QMenu(self)
		if name:
			actRename = menu.addAction("Rename…")
			actDup	= menu.addAction("Duplicate")
			actDel	= menu.addAction("Delete")
			chosen = menu.exec(self.mapToGlobal(QtCore.QPoint(int(posLocal.x()), int(posLocal.y()))))
			if chosen == actRename:
				new, ok = QtWidgets.QInputDialog.getText(self, "Rename", "New name:", text=name)
				if ok and new and new not in self.store.vectors:
					self.store.vectors[new] = self.store.vectors.pop(name)
					if name in self.store.selection:
						self.store.selection.remove(name); self.store.selection.add(new)
					self.store.changed.emit()
			elif chosen == actDup:
				self.store.duplicate_vector(name)
			elif chosen == actDel:
				if name in self.store.selection: self.store.selection.remove(name)
				self.store.vectors.pop(name, None); self.store.changed.emit()
		else:
			actAdd = menu.addAction("Add vector")
			menu.addSeparator()
			sub = menu.addMenu("Align axes to dims…")
			dims = list(self.store.dims.keys())
			acts = []
			for i, xd in enumerate(dims):
				for yd in dims[i+1:]:
					acts.append(sub.addAction(f"X:{xd}  Y:{yd}"))
			chosen = menu.exec(self.mapToGlobal(QtCore.QPoint(int(posLocal.x()), int(posLocal.y()))))
			if chosen == actAdd:
				self.store.add_vector()
			elif chosen and chosen.parentWidget() == sub:
				text = chosen.text()
				xdim = text.split()[0].split(':')[1]
				ydim = text.split()[1].split(':')[1]
				self.store.set_basis_by_dims(xdim, ydim)

# -----------------------
# Inspector (right side)
# -----------------------
class ClickLabel(QtWidgets.QLabel):
	doubleClicked = QtCore.Signal()

	def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent):
		if e.button() == QtCore.Qt.LeftButton:
			self.doubleClicked.emit()

def fmt_num(x: float) -> str:
	if abs(x) >= 1000 or (abs(x) < 0.01 and x != 0):
		return f"{x:.2e}"
	s = f"{x:.3f}".rstrip('0').rstrip('.')
	return s or "0"

class Inspector(QtWidgets.QWidget):
	def __init__(self, store: NDStore, parent=None):
		super().__init__(parent)
		self.store = store
		self._is_refreshing = False
		self.setFixedWidth(260)

		self.vlayout = QtWidgets.QVBoxLayout(self)
		self.vlayout.setContentsMargins(0,0,0,0)
		self.vlayout.setSpacing(8)

		# Selected
		self.vlayout.addWidget(self._label("Selected"))
		self.vlayout.addWidget(self._hr())

		self.selectedPanel = QtWidgets.QWidget()
		self.selLayout = QtWidgets.QVBoxLayout(self.selectedPanel); self.selLayout.setSpacing(6); self.selLayout.setContentsMargins(6,0,6,0)
		self.vlayout.addWidget(self.selectedPanel)

		self.vlayout.addSpacing(8)
		self.vlayout.addWidget(self._hr())
		self.vlayout.addWidget(self._label("Vectors"))
		self.vlayout.addWidget(self._hr())

		# Vectors list
		self.list = QtWidgets.QListWidget()
		self.list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.list.itemSelectionChanged.connect(self._list_changed)
		self.vlayout.addWidget(self.list, 1)

		# + button under Selected
		self.addBtn = QtWidgets.QPushButton("+")
		self.addBtn.setFixedSize(26,26)
		self.addBtn.clicked.connect(self._add_dim_popup)
		self.selLayout.addWidget(self.addBtn, 0, QtCore.Qt.AlignLeft)

		self._sliderWidgets: Dict[str, Tuple[ClickLabel, QtWidgets.QSlider, ClickLabel]] = {}
		self.store.changed.connect(self.refresh)
		self.refresh()

	def _label(self, text: str) -> QtWidgets.QLabel:
		lab = QtWidgets.QLabel(text)
		f = lab.font(); f.setPointSize(f.pointSize()+1); f.setBold(True); lab.setFont(f)
		return lab

	def _hr(self):
		line = QtWidgets.QFrame(); line.setFrameShape(QtWidgets.QFrame.HLine); line.setFrameShadow(QtWidgets.QFrame.Sunken)
		return line

	def refresh(self):
		if self._is_refreshing:
			return
		self._is_refreshing = True
		try:
			# Selected panel sliders for all dims (matches your mock)
			# Clear panel
			for i in reversed(range(self.selLayout.count()-1)):  # keep last (+) button
				item = self.selLayout.itemAt(i).widget()
				if item is not None:
					item.setParent(None)
			self._sliderWidgets.clear()

			for dim, mm in self.store.dims.items():
				row = QtWidgets.QWidget()
				h = QtWidgets.QHBoxLayout(row)
				h.setContentsMargins(0,0,0,0)
				h.setSpacing(6)

				minLab = ClickLabel(fmt_num(mm['min']))
				maxLab = ClickLabel(fmt_num(mm['max']))
				minLab.setToolTip("Double-click to edit min")
				maxLab.setToolTip("Double-click to edit max")

				slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
				slider.setMinimum(0)
				slider.setMaximum(1000)
				slider.setFixedWidth(180)
				slider.valueChanged.connect(lambda v, d=dim: self._slider_changed(d, v))

				# initial value: first selected or mid
				if self.store.selection:
					first = next(iter(self.store.selection))
					val = self.store.vectors[first]['vals'][dim]
				else:
					val = (mm['min']+mm['max'])/2
				slider.blockSignals(True)
				slider.setValue(self._val_to_slider(dim, val))
				slider.blockSignals(False)

				minLab.doubleClicked.connect(lambda d=dim: self._edit_min(d))
				maxLab.doubleClicked.connect(lambda d=dim: self._edit_max(d))

				h.addWidget(minLab)
				h.addWidget(slider)
				h.addWidget(maxLab)
				self.selLayout.insertWidget(self.selLayout.count()-1, row)
				self._sliderWidgets[dim] = (minLab, slider, maxLab)

			with QtCore.QSignalBlocker(self.list):
				self.list.clear()
				for name, data in self.store.vectors.items():
					item = QtWidgets.QListWidgetItem(f"?-? {name}")
					qcol = QtGui.QColor.fromRgb(*data['color'])
					item.setForeground(qcol)
					item.setSelected(name in self.store.selection)
					self.list.addItem(item)
		finally:
			self._is_refreshing = False
	# slider mapping
	def _val_to_slider(self, dim: str, val: float) -> int:
		mm = self.store.dims[dim]
		t = 0.0 if mm['max']==mm['min'] else (val-mm['min'])/(mm['max']-mm['min'])
		return int(round(1000*max(0.0,min(1.0,t))))

	def _slider_to_val(self, dim: str, sv: int) -> float:
		mm = self.store.dims[dim]
		t = sv/1000.0
		return mm['min'] + t*(mm['max']-mm['min'])

	def _slider_changed(self, dim: str, sval: int):
		if self._is_refreshing:
			return
		val = self._slider_to_val(dim, sval)
		for n in list(self.store.selection):
			self.store.vectors[n]['vals'][dim] = val
			self.store._update_coeffs_from_vals(n)
		self.store.changed.emit()

	# min/max editing (double-click)
	def _edit_min(self, dim: str):
		cur = self.store.dims[dim]['min']
		v, ok = QtWidgets.QInputDialog.getDouble(self, "Edit min", f"{dim} min:", cur, decimals=6)
		if ok:
			self.store.set_dim_min(dim, v)
			self._sliderWidgets[dim][0].setText(fmt_num(self.store.dims[dim]['min']))
			# keep slider bounds visually by remapping values (handled via changed signal)

	def _edit_max(self, dim: str):
		cur = self.store.dims[dim]['max']
		v, ok = QtWidgets.QInputDialog.getDouble(self, "Edit max", f"{dim} max:", cur, decimals=6)
		if ok:
			self.store.set_dim_max(dim, v)
			self._sliderWidgets[dim][2].setText(fmt_num(self.store.dims[dim]['max']))

	# vectors list
	def _list_changed(self):
		if self._is_refreshing:
			return
		self.store.selection = set(self._selected_names())
		self.store.changed.emit()

	def _selected_names(self):
		out = []
		for item in self.list.selectedItems():
			text = item.text()
			out.append(text[2:])  # strip "● "
		return out

	# add dimension popup
	def _add_dim_popup(self):
		name, ok = QtWidgets.QInputDialog.getText(self, "Add dimension", "Name:")
		if not ok or not name: return
		vmin, ok2 = QtWidgets.QInputDialog.getDouble(self, "Add dimension", "Min:", 0.0, decimals=6)
		if not ok2: return
		vmax, ok3 = QtWidgets.QInputDialog.getDouble(self, "Add dimension", "Max:", 1.0, decimals=6)
		if not ok3: return
		self.store.add_dim(name, vmin, vmax)

# -----------------------
# Main Window
# -----------------------
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("N-D Explorer (2D slice)")
		self.resize(1120, 700)
		self.store = NDStore()

		# seed a few dims and vectors
		for nm in ("freq1","freq2","freq3"): self.store.add_dim(nm, 0.0, 1.0)
		self.store.set_basis_by_dims("freq1","freq2")
		for _ in range(6): self.store.add_vector()

		# central layout: pad + inspector
		central = QtWidgets.QWidget(); self.setCentralWidget(central)
		h = QtWidgets.QHBoxLayout(central); h.setContentsMargins(16,16,16,16); h.setSpacing(16)
		self.pad = PadWidget(self.store)
		self.inspector = Inspector(self.store)
		h.addWidget(self.pad, 1); h.addWidget(self.inspector, 0)

		# shortcuts
		delSc = QtGui.QShortcut(QtGui.QKeySequence.Delete, self, activated=self.store.delete_selected)
		escSc = QtGui.QShortcut(QtGui.QKeySequence("Esc"), self, activated=self._clear_sel)
		selAll = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+A"), self, activated=self._select_all)
		# arrow keys
		self._arrowTimer = QtCore.QTimer(self); self._arrowTimer.setSingleShot(True)

		self.store.changed.connect(self._sync_sliders)

	def _clear_sel(self):
		self.store.selection.clear(); self.store.changed.emit()

	def _select_all(self):
		self.store.selection = set(self.store.vectors.keys()); self.store.changed.emit()

	def _sync_sliders(self):
		# keep inspector sliders showing first selected values
		if self.inspector._is_refreshing:
			return
		if not self.store.selection:
			return
		first = next(iter(self.store.selection))
		for dim, widgets in self.inspector._sliderWidgets.items():
			_, slider, _ = widgets
			val = self.store.vectors[first]['vals'][dim]
			slider.blockSignals(True)
			slider.setValue(self.inspector._val_to_slider(dim, val))
			slider.blockSignals(False)

	# Keyboard nudging (global)
	def keyPressEvent(self, ev: QtGui.QKeyEvent):
		key = ev.key()
		if key in (QtCore.Qt.Key_Left, QtCore.Qt.Key_Right, QtCore.Qt.Key_Up, QtCore.Qt.Key_Down):
			if not self.store.selection: return
			step = 0.005 * (5 if (ev.modifiers() & QtCore.Qt.ShiftModifier) else 1)
			dx = (key == QtCore.Qt.Key_Right) - (key == QtCore.Qt.Key_Left)
			dy = (key == QtCore.Qt.Key_Up) - (key == QtCore.Qt.Key_Down)
			for n in list(self.store.selection):
				vec = self.store.vectors[n]
				vec['cu'] = min(1.0, max(0.0, vec['cu'] + dx*step))
				vec['cv'] = min(1.0, max(0.0, vec['cv'] + dy*step))
				self.store._apply_coeffs_to_vals(n)
			self.store.changed.emit()
		else:
			super().keyPressEvent(ev)

# -----------------------
# Entrypoint
# -----------------------
def main():
	app = QtWidgets.QApplication(sys.argv)
	w = MainWindow(); w.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()
