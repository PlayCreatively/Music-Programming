# state.py
# Global state for high-D slice explorer
# dimensions -> Parameter (D)
# vectors    -> preset    (V)

import numpy as np
from random import randint
import imgui
import helper as H

# ---------- core high-D data ---------- #

# Parameter names: ["freq1", "freq2", ...]
param_names: list[str] = [] # len D

# Per-parameter bounds
mins: np.ndarray # shape (D,)
maxs: np.ndarray # shape (D,)

# High-D vectors (presets)
presets: np.ndarray # shape (V, D) | [Preset Index] -> Preset vector

# 2D basis for the current slice
basis: np.ndarray # shape (2, D) | [basis Vector Index "U,V"] -> basis vector
slice_origin: np.ndarray | None = None # shape (D,) | Origin point of the slice in unit space

# Names + colors per vector
preset_names: list[str] = [] # len V
preset_colors: list[tuple[int,int,int]] = []  # len V, RGB tuples

# ---------- app / interaction state ----------

# Which vectors are selected (indices into presets/preset_names)
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
    global param_names, mins, maxs, basis, slice_origin, presets, preset_names, preset_colors
    param_names = list(dims)
    D = len(param_names)

    mins = np.zeros(D, dtype=float)
    maxs = np.ones(D, dtype=float)
    presets = np.zeros((0, D), dtype=float)

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
        basis = np.zeros((2, D), dtype=float)
        basis[0, 0] = 1.0  # x axis = dim 0
        basis[1, 1] = 1.0  # y axis = dim 1
        slice_origin = np.zeros(D, dtype=float)
    else:
        basis = np.zeros((2, D), dtype=float)
        slice_origin = np.zeros(D, dtype=float)

def add_preset(name: str, color: tuple[int,int,int] = None, value: np.ndarray = None) -> int:
    """Append a new vector at the midpoint of each dimension. Returns its index."""
    global presets, selection, active_preset_value
    assert mins is not None and maxs is not None and presets is not None

    if value is None:
        D = presets.shape[1]
        value = np.random.uniform(low=mins, high=maxs, size=(1, D))
        
    if color is None:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))

    presets = np.vstack([presets, value])
    idx = presets.shape[0] - 1

    preset_names.append(name or f"vec{idx}")
    preset_colors.append(color or (255, 255, 255))
    selection = {idx}
    active_preset_value = presets[idx, :]
    return idx


def add_parameter(name: str, vmin: float = 0.0, vmax: float = 1.0):
    """Append a new dimension to all vectors and update mins/maxs/basis."""
    global param_names, mins, maxs, presets, basis, slice_origin, active_preset_value
    param_names.append(name)
    D_new = len(param_names)

    if mins is None or maxs is None:
        mins = np.array([vmin], dtype=float)
        maxs = np.array([vmax], dtype=float)
    else:
        mins = np.concatenate([mins, np.array([vmin], dtype=float)])
        maxs = np.concatenate([maxs, np.array([vmax], dtype=float)])

    if presets is None:
        presets = np.zeros((0, D_new), dtype=float)
    else:
        N = presets.shape[0]
        mid = (vmin + vmax) / 2.0
        new_col = np.full((N, 1), mid, dtype=float)
        presets = np.hstack([presets, new_col])

    # grow basis with a 0 in new dim
    if basis is None:
        basis = np.zeros((2, D_new), dtype=float)
    else:
        extra_col = np.zeros((2, 1), dtype=float)
        basis = np.hstack([basis, extra_col])
        
    if slice_origin is None:
        slice_origin = np.zeros(D_new, dtype=float)
    else:
        slice_origin = np.concatenate([slice_origin, [0.0]])
        
    if active_preset_value is not None:
        # extend active_preset_value by one dimension with the midpoint
        mid = (vmin + vmax) / 2.0
        active_preset_value = np.hstack([active_preset_value, np.array([mid], dtype=float)])
    

def get_preset(i: int) -> np.ndarray: # shape (D,)
    """Return the high-D vector at given index."""
    assert presets is not None
    return presets[i, :]

def get_preset_from_coordinates(u: float, v: float) -> np.ndarray:
    """Return the high-D vector at given (u,v) coordinates on the current 2D plane."""
    assert basis is not None
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    unit_point = origin + u * basis[0, :] + v * basis[1, :]
    point = H.from_unit(unit_point, mins, maxs)
    return point

def get_unit_from_coordinates(u: float, v: float) -> np.ndarray:
    """Return the high-D unit vector at given (u,v) coordinates."""
    assert basis is not None
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    return origin + u * basis[0, :] + v * basis[1, :]

def is_point_valid(u: float, v: float) -> bool:
    """Check if a point on the plane is within the unit hypercube."""
    p = get_unit_from_coordinates(u, v)
    # Allow a tiny epsilon for floating point noise
    return np.all((p >= -1e-9) & (p <= 1.0 + 1e-9))

def get_slice_polygon_vertices() -> list[tuple[float, float]]:
    """
    Calculate the polygon vertices (u, v) representing the intersection 
    of the current plane with the unit hypercube [0, 1]^D.
    """
    if basis is None: return []
    
    # Start with a large box in (u, v) space
    limit = np.sqrt(len(param_names)) * 2.0
    poly = [(-limit, -limit), (limit, -limit), (limit, limit), (-limit, limit)]
    
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    
    # Helper to clip polygon by line ax + by + c <= 0
    def clip(poly_in, a, b, c):
        new_poly = []
        if not poly_in: return []
        
        for i in range(len(poly_in)):
            curr = poly_in[i]
            prev = poly_in[(i - 1) % len(poly_in)]
            
            curr_in = (a * curr[0] + b * curr[1] + c) <= 1e-9
            prev_in = (a * prev[0] + b * prev[1] + c) <= 1e-9
            
            if curr_in:
                if not prev_in:
                    denom = (a * (prev[0] - curr[0]) + b * (prev[1] - curr[1]))
                    if abs(denom) > 1e-12:
                        t = (a * prev[0] + b * prev[1] + c) / denom
                        inter_x = prev[0] + t * (curr[0] - prev[0])
                        inter_y = prev[1] + t * (curr[1] - prev[1])
                        new_poly.append((inter_x, inter_y))
                new_poly.append(curr)
            elif prev_in:
                denom = (a * (prev[0] - curr[0]) + b * (prev[1] - curr[1]))
                if abs(denom) > 1e-12:
                    t = (a * prev[0] + b * prev[1] + c) / denom
                    inter_x = prev[0] + t * (curr[0] - prev[0])
                    inter_y = prev[1] + t * (curr[1] - prev[1])
                    new_poly.append((inter_x, inter_y))
                
        return new_poly

    # For each dimension k, clip against 0 <= x_k <= 1
    # x_k = origin[k] + u * basis[0, k] + v * basis[1, k]
    for k in range(len(param_names)):
        b0 = basis[0, k]
        b1 = basis[1, k]
        o = origin[k]
        
        # Lower bound: x_k >= 0  =>  -x_k <= 0
        # -o - u*b0 - v*b1 <= 0
        poly = clip(poly, -b0, -b1, -o)
        if not poly: return []
        
        # Upper bound: x_k <= 1  =>  x_k - 1 <= 0
        # o + u*b0 + v*b1 - 1 <= 0
        poly = clip(poly, b0, b1, o - 1.0)
        if not poly: return []
        
    return poly

def update_preset_parameter_index(preset: int, param: int, value: float):
    """Update a single parameter of a preset vector by numeric indices."""
    assert presets is not None
    presets[preset, param] = value

def update_preset_parameter(preset: str, param: str, value: float):
    """Update a single parameter of a preset vector by names."""
    assert preset_names is not None and param_names is not None
    update_preset_parameter_index(preset_names.index(preset), param_names.index(param), value)



def update_preset_on_plane(preset: int, u: float, v: float):
    """Update the preset vector to lie on the current 2D plane at (u,v) coords."""
    assert basis is not None and presets is not None
    
    current_unit = H.to_unit(presets[preset], mins, maxs)
    
    # Calculate movement vector in the plane to reach (u,v)
    # We preserve the off-plane components of the vector.
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    
    # Current projection u,v
    cur_u = np.dot(current_unit - origin, basis[0])
    cur_v = np.dot(current_unit - origin, basis[1])
    
    diff_u = u - cur_u
    diff_v = v - cur_v
    
    movement = diff_u * basis[0] + diff_v * basis[1]
    target_unit = current_unit + movement
    
    # Restrict movement to bounds
    final_unit = H.clamp_movement(current_unit, target_unit)
    
    updated_point = H.from_unit(final_unit, mins, maxs)
    presets[preset, :] = updated_point
    
def get_presets_on_plane() -> tuple[np.ndarray, np.ndarray]: # shape (V,2), (V,)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert basis is not None and presets is not None
    unit_presets = H.to_unit(presets, mins, maxs)
    
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    
    # Project relative to slice origin
    # P_proj = (P - Origin) . basis^T
    presets_2D = (unit_presets - origin) @ basis.T
    
    # Calculate distance to plane in unit space
    # P_on_plane = Origin + P_proj . basis
    projected_back = origin + presets_2D @ basis 
    diff = unit_presets - projected_back
    dists = np.linalg.norm(diff, axis=1)
    MAX_DIST = np.sqrt(len(param_names))  # max possible distance in unit space
    dists = np.clip(dists / MAX_DIST, 0.0, 1.0)  # normalize to 0..1
    
    return presets_2D, dists

def project_point_on_plane(point: np.ndarray) -> tuple[np.ndarray, np.ndarray]: # shape (V,D)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert basis is not None and presets is not None
    unit_presets = H.to_unit(point, mins, maxs)
    
    origin = slice_origin if slice_origin is not None else np.zeros(len(param_names))
    
    presets_2D = (unit_presets - origin) @ basis.T
    
    # Calculate distance to plane in unit space
    projected_back = origin + presets_2D @ basis 
    diff = unit_presets - projected_back
    
    if diff.ndim == 1:
        dists = np.linalg.norm(diff)
    else:
        dists = np.linalg.norm(diff, axis=1)
    return presets_2D, dists
        
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
    
    

def get_slope_of_parameter_in_plane(param_idx: int) -> tuple[float,float]:
    """Return the (u,v) slope of the given parameter in the current 2D plane."""
    assert basis is not None
    x,y = basis[:, param_idx]  # (2,)
    return x,y

# Build basis

def assign_parameters_to_basis(x_param: int, y_param: int):
    global basis, slice_origin
    D = len(param_names)
    basis = np.zeros((2, D), float)
    basis[0, x_param] = 1.0
    basis[1, y_param] = 1.0
    slice_origin = np.zeros(D, float) # Axis views usually start at origin

# QR decomposition version
def assign_basis_from_three_points(p1, p2, p3):
    global basis, slice_origin
    A = np.stack([p2 - p1, p3 - p1], axis=1)  # (D,2)
    Q, R = np.linalg.qr(A)
    basis = Q.T  # (2,D), columns are orthonormal
    slice_origin = (p1 + p2 + p3) / 3.0  # Center the slice at the centroid of the three points
    
def assign_basis_from_three_presets(presets: list[int]):
    global basis
    unit_presets = H.to_unit(presets, mins, maxs)
    assign_basis_from_three_points(unit_presets[presets[0]], unit_presets[presets[1]], unit_presets[presets[2]])
    


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
        active_preset_value = presets[idx, :]