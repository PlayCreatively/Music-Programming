# pip install PySide6 pyqtgraph
from PySide6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import random, itertools

class NDModel(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.dims = {}  # name -> (min,max)
        self.vectors = {}  # name -> {dim: value}
        self.palette = itertools.cycle(['#ff4d4d','#5cf2d6','#8aff3b','#ffca28','#bb86fc','#ff66cc','#64b5f6'])

    def add_dim(self, name, dmin=0.0, dmax=1.0):
        self.dims[name] = (float(dmin), float(dmax))
        # backfill missing values in vectors
        for v in self.vectors.values():
            v.setdefault(name, (dmin + dmax)/2)
        self.changed.emit()

    def add_vector(self, name=None):
        if not self.dims: return
        name = name or f"vec{len(self.vectors)+1}"
        color = next(self.palette)
        self.vectors[name] = {dim: random.uniform(*rng) for dim, rng in self.dims.items()}
        self.vectors[name]['__color'] = color
        self.changed.emit()

    def delete_vectors(self, names):
        for n in names:
            self.vectors.pop(n, None)
        self.changed.emit()

class ScatterPad(pg.PlotWidget):
    pointRightClicked = QtCore.Signal(str)       # vector name
    pointCtrlClicked = QtCore.Signal(str, bool)  # (vector name, additive)
    emptyRightClicked = QtCore.Signal(QtCore.QPoint)

    def __init__(self, model: NDModel):
        super().__init__(background=(30,30,30))
        self.model = model
        self.setAspectLocked(True)
        self.showGrid(x=True, y=True, alpha=0.2)
        self.getPlotItem().hideButtons()
        self.scatter = pg.ScatterPlotItem(size=12, pxMode=True, pen=pg.mkPen(width=0))
        self.addItem(self.scatter)
        self.scatter.sigClicked.connect(self._on_click)
        self.scene().sigMouseClicked.connect(self._scene_click)
        self.x_dim, self.y_dim = None, None
        self.selected = set()
        self.model.changed.connect(self.refresh)

    def set_axes(self, xdim, ydim):
        self.x_dim, self.y_dim = xdim, ydim
        self.refresh()

    def refresh(self):
        if not (self.x_dim and self.y_dim and self.model.dims):
            self.scatter.setData([])
            return
        xs, ys, brushes, data = [], [], [], []
        xmin,xmax = self.model.dims[self.x_dim]
        ymin,ymax = self.model.dims[self.y_dim]
        for name, vec in self.model.vectors.items():
            if name.startswith('_'): continue
            x = vec.get(self.x_dim, (xmin+xmax)/2)
            y = vec.get(self.y_dim, (ymin+ymax)/2)
            xs.append(x); ys.append(y)
            c = vec.get('__color', '#ffffff')
            sel = name in self.selected
            brushes.append(pg.mkBrush(QtGui.QColor(c) if not sel else QtGui.QColor('white')))
            data.append({'name': name})
        self.scatter.setData(xs, ys, brush=brushes, data=data)
        self.setXRange(*self.model.dims[self.x_dim], padding=0.05)
        self.setYRange(*self.model.dims[self.y_dim], padding=0.05)

    def _on_click(self, scatter, points):
        name = points[0].data()['name']
        mods = QtWidgets.QApplication.keyboardModifiers()
        additive = bool(mods & QtCore.Qt.ControlModifier)
        self.pointCtrlClicked.emit(name, additive)

    def _scene_click(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            items = self.itemsAt(ev.scenePos())
            if self.scatter in items:
                # right-click on a point
                mousePoint = self.getPlotItem().vb.mapSceneToView(ev.scenePos())
                pts = self.scatter.pointsAt(mousePoint)
                if pts:
                    self.pointRightClicked.emit(pts[0].data()['name'])
                    return
            self.emptyRightClicked.emit(ev.screenPos().toPoint())

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("N-D Explorer (2D slice)")
        self.resize(1100, 700)
        self.model = NDModel()

        # Center: 2D pad
        self.pad = ScatterPad(self.model)
        self.setCentralWidget(self.pad)

        # Right dock: vectors list
        self.vecList = QtWidgets.QListWidget()
        self.vecList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        vecDock = QtWidgets.QDockWidget("Vectors"); vecDock.setWidget(self.vecList)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, vecDock)

        # Middle dock: selected panel (sliders later)
        self.selectedPanel = QtWidgets.QListWidget()
        selDock = QtWidgets.QDockWidget("Selected"); selDock.setWidget(self.selectedPanel)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, selDock)

        # Left dock: dims + controls
        left = QtWidgets.QWidget(); form = QtWidgets.QFormLayout(left)
        self.xCombo = QtWidgets.QComboBox(); self.yCombo = QtWidgets.QComboBox()
        form.addRow("X axis", self.xCombo); form.addRow("Y axis", self.yCombo)
        self.dimName = QtWidgets.QLineEdit(); self.dmin = QtWidgets.QDoubleSpinBox(); self.dmax = QtWidgets.QDoubleSpinBox()
        self.dmin.setRange(-1e6,1e6); self.dmax.setRange(-1e6,1e6); self.dmin.setValue(0); self.dmax.setValue(1)
        addDimBtn = QtWidgets.QPushButton("Add dimension")
        addVecBtn = QtWidgets.QPushButton("Add vector")
        form.addRow("Dim name", self.dimName); form.addRow("Min", self.dmin); form.addRow("Max", self.dmax)
        form.addRow(addDimBtn); form.addRow(addVecBtn)
        dimDock = QtWidgets.QDockWidget("Axes & Dimensions"); dimDock.setWidget(left)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dimDock)

        # Signals
        addDimBtn.clicked.connect(self.add_dim)
        addVecBtn.clicked.connect(self.add_vec)
        self.xCombo.currentTextChanged.connect(self._axes_changed)
        self.yCombo.currentTextChanged.connect(self._axes_changed)
        self.model.changed.connect(self._rebuild_ui)
        self.pad.pointCtrlClicked.connect(self._toggle_selection)
        self.pad.pointRightClicked.connect(self._point_context)
        self.pad.emptyRightClicked.connect(self._empty_context)
        self.vecList.itemSelectionChanged.connect(self._sync_from_list)

        # Keyboard delete
        self.shortDel = QtGui.QShortcut(QtGui.QKeySequence.Delete, self, activated=self._delete_selected)

        # Seed a couple of dims + vectors to see something
        for nm, lo, hi in [("freq1",0,1),("freq2",0,1),("freq3",0,1)]:
            self.model.add_dim(nm, lo, hi)
        for _ in range(6): self.model.add_vector()
        self._rebuild_ui()
        self.xCombo.setCurrentText("freq1"); self.yCombo.setCurrentText("freq2")

    # UI actions
    def add_dim(self):
        name = self.dimName.text().strip()
        if not name or name in self.model.dims: return
        self.model.add_dim(name, self.dmin.value(), self.dmax.value())
        self.dimName.clear()

    def add_vec(self):
        self.model.add_vector()

    def _axes_changed(self):
        self.pad.set_axes(self.xCombo.currentText(), self.yCombo.currentText())

    def _rebuild_ui(self):
        # combos
        dims = list(self.model.dims.keys())
        with QtCore.QSignalBlocker(self.xCombo):
            self.xCombo.clear(); self.xCombo.addItems(dims)
        with QtCore.QSignalBlocker(self.yCombo):
            self.yCombo.clear(); self.yCombo.addItems(dims)
        # vectors list
        with QtCore.QSignalBlocker(self.vecList):
            self.vecList.clear()
            for name in self.model.vectors.keys():
                if name.startswith('_'): continue
                item = QtWidgets.QListWidgetItem(name)
                self.vecList.addItem(item)
                item.setSelected(name in self.pad.selected)
        # selected panel
        self.selectedPanel.clear()
        for n in sorted(self.pad.selected):
            self.selectedPanel.addItem(n)
        self.pad.refresh()

    def _toggle_selection(self, name, additive):
        if not additive:
            self.pad.selected = {name}
        else:
            if name in self.pad.selected: self.pad.selected.remove(name)
            else: self.pad.selected.add(name)
        self._rebuild_ui()

    def _sync_from_list(self):
        self.pad.selected = {i.text() for i in self.vecList.selectedItems()}
        self._rebuild_ui()

    # Context menus
    def _point_context(self, name):
        menu = QtWidgets.QMenu(self)
        actRename = menu.addAction("Rename…")
        actDup = menu.addAction("Duplicate")
        actDel = menu.addAction("Delete")
        chosen = menu.exec(QtGui.QCursor.pos())
        if chosen == actRename:
            new, ok = QtWidgets.QInputDialog.getText(self, "Rename", "New name:", text=name)
            if ok and new and new not in self.model.vectors:
                self.model.vectors[new] = self.model.vectors.pop(name)
                self.pad.selected = {new if s==name else s for s in self.pad.selected}
                self.model.changed.emit()
        elif chosen == actDup:
            base = name + "_copy"
            i=1
            while f"{base}{i}" in self.model.vectors: i+=1
            self.model.vectors[f"{base}{i}"] = dict(self.model.vectors[name])
            self.model.changed.emit()
        elif chosen == actDel:
            self.model.delete_vectors([name])

    def _empty_context(self, screenPos):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Add vector", self.add_vec)
        menu.exec(screenPos)

    def _delete_selected(self):
        if self.pad.selected:
            self.model.delete_vectors(list(self.pad.selected))
            self.pad.selected.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    pg.setConfigOptions(antialias=True)
    w = Main(); w.show()
    app.exec()
