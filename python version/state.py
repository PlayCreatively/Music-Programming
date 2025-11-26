# state.py
# Global state for high-D slice explorer
# dimensions -> Parameter (D)
# vectors    -> preset    (V)

import numpy as np
from random import randint

# ---------- core high-D data ---------- #

# Parameter names: ["freq1", "freq2", ...]
param_names: list[str] = [] # len D

# Per-parameter bounds
mins: np.ndarray # shape (D,)
maxs: np.ndarray # shape (D,)

# High-D vectors (presets)
Presets: np.ndarray # shape (V, D) | [Preset Index] -> Preset vector

# 2D basis for the current slice
Basis: np.ndarray # shape (2, D) | [Basis Vector Index "U,V"] -> Basis vector

# Names + colors per vector
preset_names: list[str] = [] # len V
preset_colors: list[tuple[int,int,int]] = []  # len V, RGB tuples

# ---------- app / interaction state ----------

# Which vectors are selected (indices into Presets/preset_names)
selection: set[int] = set()

drag_anchor_pad: tuple[float,float]  # (x,y) in pad 0..1 space
drag_initial_Y: np.ndarray           # (k,2) projected coords of selected at drag start

# View transforms (for future pan/zoom)
pad_zoom: float = 1.0
pad_offset: tuple[float,float] = (0.0, 0.0)

hovered_parameter_slider: int = -1  # 
"""index of parameter being edited in slider panel, or -1 if none."""

active_preset_value: np.ndarray | None = None
"""active preset vector. Can be a non-saved one if exploring. Is a non-saved one if selection is empty."""

# ---------- simple helpers ----------
def init_space(dims: list[str], n_vectors: int = 0):
    """Initialize global space with given dimensions and optional empty vectors."""
    global param_names, mins, maxs, Basis, Presets, preset_names, preset_colors
    param_names = list(dims)
    param_names = list(dims)
    D = len(param_names)

    mins = np.zeros(D, dtype=float)
    maxs = np.ones(D, dtype=float)
    Presets = np.zeros((0, D), dtype=float)

    if n_vectors > 0:
        X = np.zeros((n_vectors, D), dtype=float)
        preset_names = [f"vec{i}" for i in range(n_vectors)]
        preset_colors = [(255,255,255)] * n_vectors
    else:
        X = np.zeros((0, D), dtype=float)
        preset_names = []
        preset_colors = []

    # default slice: first 2 dims if available
    if D >= 2:
        Basis = np.zeros((2, D), dtype=float)
        Basis[0, 0] = 1.0  # x axis = dim 0
        Basis[1, 1] = 1.0  # y axis = dim 1
    else:
        Basis = np.zeros((2, D), dtype=float)

def add_preset(name: str, color: tuple[int,int,int] = None, value: np.ndarray = None) -> int:
    """Append a new vector at the midpoint of each dimension. Returns its index."""
    global Presets, selection, active_preset_value
    assert mins is not None and maxs is not None and Presets is not None

    if value is None:
        D = Presets.shape[1]
        value = np.random.uniform(low=mins, high=maxs, size=(1, D))
        
    if color is None:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))

    Presets = np.vstack([Presets, value])
    idx = Presets.shape[0] - 1

    preset_names.append(name or f"vec{idx}")
    preset_colors.append(color or (255, 255, 255))
    selection = {idx}
    active_preset_value = Presets[idx, :]
    return idx


def add_parameter(name: str, vmin: float = 0.0, vmax: float = 1.0):
    """Append a new dimension to all vectors and update mins/maxs/B."""
    global param_names, mins, maxs, Presets, Basis, active_preset_value
    param_names.append(name)
    D_new = len(param_names)

    if mins is None or maxs is None:
        mins = np.array([vmin], dtype=float)
        maxs = np.array([vmax], dtype=float)
    else:
        mins = np.concatenate([mins, np.array([vmin], dtype=float)])
        maxs = np.concatenate([maxs, np.array([vmax], dtype=float)])

    if Presets is None:
        Presets = np.zeros((0, D_new), dtype=float)
    else:
        N = Presets.shape[0]
        mid = (vmin + vmax) / 2.0
        new_col = np.full((N, 1), mid, dtype=float)
        Presets = np.hstack([Presets, new_col])

    # grow basis with a 0 in new dim
    if Basis is None:
        Basis = np.zeros((2, D_new), dtype=float)
    else:
        extra_col = np.zeros((2, 1), dtype=float)
        Basis = np.hstack([Basis, extra_col])
        
        
    if active_preset_value is not None:
        # extend active_preset_value by one dimension with the midpoint
        mid = (vmin + vmax) / 2.0
        active_preset_value = np.hstack([active_preset_value, np.array([mid], dtype=float)])
    

def get_preset(i: int) -> np.ndarray: # shape (D,)
    """Return the high-D vector at given index."""
    assert Presets is not None
    return Presets[i, :]

def get_preset_from_coordinates(u: float, v: float) -> np.ndarray:
    """Return the high-D vector at given (u,v) coordinates on the current 2D plane."""
    assert Basis is not None
    unit_point = u * Basis[0, :] + v * Basis[1, :]
    point = from_unit(unit_point, mins, maxs)
    return point
def update_preset_parameter_index(preset: int, param: int, value: float):
    """Update a single parameter of a preset vector by numeric indices."""
    assert Presets is not None
    Presets[preset, param] = value

def update_preset_parameter(preset: str, param: str, value: float):
    """Update a single parameter of a preset vector by names."""
    assert preset_names is not None and param_names is not None
    update_preset_parameter_index(preset_names.index(preset), param_names.index(param), value)

def update_preset_on_plane(preset: int, u: float, v: float):
    """Update the preset vector to lie on the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    updated_unit_point = u * Basis[0, :] + v * Basis[1, :]
    updated_point = from_unit(updated_unit_point, mins, maxs)
    Presets[preset, :] = updated_point
    
def get_presets_on_plane() -> np.ndarray: # shape (V,D)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    unit_presets = to_unit(Presets, mins, maxs)
    Presets_2D = unit_presets @ Basis.T
    return Presets_2D

def project_point_on_plane(point: np.ndarray) -> np.ndarray: # shape (V,D)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    unit_presets = to_unit(point, mins, maxs)
    Presets_2D = unit_presets @ Basis.T
    return Presets_2D
    
def get_selection_name() -> str:
    """Return the names of all currently selected presets."""
    assert preset_names is not None
    if selection is None or len(selection) == 0:
        return "no selection"
    elif len(selection) == 1:
        idx = next(iter(selection))
        return preset_names[idx]
    else :
        return f"{len(selection)} presets selected"
    
    
def to_unit(preset:np.ndarray, mins, maxs):
    span = np.where((maxs - mins) != 0, (maxs - mins), 1.0)
    return (preset - mins) / span

def from_unit(unit_preset:np.ndarray, mins, maxs):
    return mins + unit_preset * (maxs - mins)

# Project to 2-D and back
def project(unit_preset:np.ndarray, mins, maxs, basis:np.ndarray):
    """(N,D) -> (N,2) in 0..1"""
    T = to_unit(unit_preset, mins, maxs)          # (N,D)
    Y = T @ basis                            # (N,2)
    return np.clip(Y, 0.0, 1.0)

def lift(selected_unit_presets, mins, maxs, basis):
    """(k,2) -> (k,D) projected back onto the plane spanned by basis."""
    T_plane = np.clip(selected_unit_presets @ basis.T, 0.0, 1.0)
    return from_unit(T_plane, mins, maxs)

def get_slope_of_parameter_in_plane(param_idx: int) -> tuple[float,float]:
    """Return the (u,v) slope of the given parameter in the current 2D plane."""
    assert Basis is not None
    x,y = Basis[:, param_idx]  # (2,)
    return x,y

# Build basis

def assign_parameters_to_basis(x_param: int, y_param: int):
    global Basis
    D = len(param_names)
    Basis = np.zeros((2, D), float)
    Basis[0, x_param] = 1.0
    Basis[1, y_param] = 1.0

# Gram–Schmidt version
def assign_basis_from_three_points(p1, p2, p3):
    global Basis
    # All are (D,) in unit space.
    u = p2 - p1
    u /= np.linalg.norm(u) + 1e-12
    w = p3 - p1
    # Gram–Schmidt: v = w - (u·w)u
    v = w - np.dot(u, w) * u
    v /= np.linalg.norm(v) + 1e-12
    # Pack as columns
    Basis = np.stack([u, v]) # (2,D)
    
# QR decomposition version
def assign_basis_from_three_points(p1, p2, p3):
    global Basis
    A = np.stack([p2 - p1, p3 - p1], axis=1)  # (D,2)
    Q, R = np.linalg.qr(A)
    Basis = Q.T  # (2,D), columns are orthonormal
    
def assign_basis_from_three_presets(presets: list[int]):
    global Basis
    unit_presets = to_unit(Presets, mins, maxs)
    assign_basis_from_three_points(unit_presets[presets[0]], unit_presets[presets[1]], unit_presets[presets[2]])
    
import imgui
def is_cursor_within_circle(circle_center, radius) -> bool:
    """Check if the cursor is within a circle defined by center and radius."""
    import globals as G
    dx = G.mouse_pos[0] - circle_center[0]
    dy = G.mouse_pos[1] - circle_center[1]
    
    distance_squared = dx * dx + dy * dy
    return distance_squared <= radius * radius

def record_selection(idx: int):
    """Record the given preset index as selected."""
    global selection, active_preset_value
    
    is_selected = idx in selection
    if imgui.get_io().key_ctrl:
        # multi-select
        if is_selected:
            selection.remove(idx)
        else:
            selection.add(idx)
    else:
        selection = {idx}
        active_preset_value = Presets[idx, :]