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
Slice_origin: np.ndarray | None = None # shape (D,) | Origin point of the slice in unit space

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
    global param_names, mins, maxs, Basis, Slice_origin, Presets, preset_names, preset_colors
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
        Slice_origin = np.zeros(D, dtype=float)
    else:
        Basis = np.zeros((2, D), dtype=float)
        Slice_origin = np.zeros(D, dtype=float)

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
    global param_names, mins, maxs, Presets, Basis, Slice_origin, active_preset_value
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
        
    if Slice_origin is None:
        Slice_origin = np.zeros(D_new, dtype=float)
    else:
        Slice_origin = np.concatenate([Slice_origin, [0.0]])
        
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
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    unit_point = origin + u * Basis[0, :] + v * Basis[1, :]
    point = from_unit(unit_point, mins, maxs)
    return point

def get_unit_from_coordinates(u: float, v: float) -> np.ndarray:
    """Return the high-D unit vector at given (u,v) coordinates."""
    assert Basis is not None
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    return origin + u * Basis[0, :] + v * Basis[1, :]

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
    if Basis is None: return []
    
    # Start with a large box in (u, v) space
    limit = np.sqrt(len(param_names)) * 2.0
    poly = [(-limit, -limit), (limit, -limit), (limit, limit), (-limit, limit)]
    
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    
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
    # x_k = origin[k] + u * Basis[0, k] + v * Basis[1, k]
    for k in range(len(param_names)):
        b0 = Basis[0, k]
        b1 = Basis[1, k]
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
    assert Presets is not None
    Presets[preset, param] = value

def update_preset_parameter(preset: str, param: str, value: float):
    """Update a single parameter of a preset vector by names."""
    assert preset_names is not None and param_names is not None
    update_preset_parameter_index(preset_names.index(preset), param_names.index(param), value)

def clamp_movement(start: np.ndarray, end: np.ndarray) -> np.ndarray:
    """
    Return the point on the segment [start, end] that is closest to end
    while remaining within the unit hypercube [0, 1]^D.
    """
    direction = end - start
    t_max = 1.0
    epsilon = 1e-9
    
    for i in range(len(start)):
        d = direction[i]
        s = start[i]
        
        if abs(d) < epsilon:
            continue
            
        if d > 0:
            # Moving towards 1
            t = (1.0 - s) / d
        else:
            # Moving towards 0
            t = (0.0 - s) / d
            
        if t < t_max:
            # We only care about t >= 0, but if we are slightly out of bounds
            # and moving in, t might be negative? 
            # If s=1.1, d=-0.1 (moving in), t=(0-1.1)/-0.1 = 11.
            # If s=1.1, d=0.1 (moving out), t=(1-1.1)/0.1 = -1.
            # We want to restrict movement that goes OUT of bounds.
            # If we are already out, and moving further out, t < 0.
            # If we are out and moving in, t > 1 (for the far wall) or t large.
            
            # Simple logic: we want the smallest positive t that hits a boundary.
            # But we also want to handle the case where we are already out?
            # Assuming start is valid [0,1].
            if t >= 0:
                t_max = t
            
    t_max = max(0.0, min(t_max, 1.0))
    return start + t_max * direction

def update_preset_on_plane(preset: int, u: float, v: float):
    """Update the preset vector to lie on the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    
    current_unit = to_unit(Presets[preset], mins, maxs)
    
    # Calculate movement vector in the plane to reach (u,v)
    # We preserve the off-plane components of the vector.
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    
    # Current projection u,v
    cur_u = np.dot(current_unit - origin, Basis[0])
    cur_v = np.dot(current_unit - origin, Basis[1])
    
    diff_u = u - cur_u
    diff_v = v - cur_v
    
    movement = diff_u * Basis[0] + diff_v * Basis[1]
    target_unit = current_unit + movement
    
    # Restrict movement to bounds
    final_unit = clamp_movement(current_unit, target_unit)
    
    updated_point = from_unit(final_unit, mins, maxs)
    Presets[preset, :] = updated_point
    
def get_presets_on_plane() -> tuple[np.ndarray, np.ndarray]: # shape (V,2), (V,)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    unit_presets = to_unit(Presets, mins, maxs)
    
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    
    # Project relative to slice origin
    # P_proj = (P - Origin) . Basis^T
    Presets_2D = (unit_presets - origin) @ Basis.T
    
    # Calculate distance to plane in unit space
    # P_on_plane = Origin + P_proj . Basis
    projected_back = origin + Presets_2D @ Basis 
    diff = unit_presets - projected_back
    dists = np.linalg.norm(diff, axis=1)
    MAX_DIST = np.sqrt(len(param_names))  # max possible distance in unit space
    dists = np.clip(dists / MAX_DIST, 0.0, 1.0)  # normalize to 0..1
    
    return Presets_2D, dists

def project_point_on_plane(point: np.ndarray) -> tuple[np.ndarray, np.ndarray]: # shape (V,D)
    """Return all preset vectors projected onto the current 2D plane at (u,v) coords."""
    assert Basis is not None and Presets is not None
    unit_presets = to_unit(point, mins, maxs)
    
    origin = Slice_origin if Slice_origin is not None else np.zeros(len(param_names))
    
    Presets_2D = (unit_presets - origin) @ Basis.T
    
    # Calculate distance to plane in unit space
    projected_back = origin + Presets_2D @ Basis 
    diff = unit_presets - projected_back
    
    if diff.ndim == 1:
        dists = np.linalg.norm(diff)
    else:
        dists = np.linalg.norm(diff, axis=1)
    return Presets_2D, dists
        
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
def project(unit_preset:np.ndarray, mins, maxs, basis:np.ndarray, origin:np.ndarray=None):
    """(N,D) -> (N,2) in 0..1"""
    T = to_unit(unit_preset, mins, maxs)          # (N,D)
    if origin is not None:
        T = T - origin
    Y = T @ basis                            # (N,2)
    return np.clip(Y, 0.0, 1.0)

def lift(selected_unit_presets, mins, maxs, basis, origin:np.ndarray=None):
    """(k,2) -> (k,D) projected back onto the plane spanned by basis."""
    T_plane = selected_unit_presets @ basis.T
    if origin is not None:
        T_plane = T_plane + origin
    T_plane = np.clip(T_plane, 0.0, 1.0)
    return from_unit(T_plane, mins, maxs)

def get_slope_of_parameter_in_plane(param_idx: int) -> tuple[float,float]:
    """Return the (u,v) slope of the given parameter in the current 2D plane."""
    assert Basis is not None
    x,y = Basis[:, param_idx]  # (2,)
    return x,y

# Build basis

def assign_parameters_to_basis(x_param: int, y_param: int):
    global Basis, Slice_origin
    D = len(param_names)
    Basis = np.zeros((2, D), float)
    Basis[0, x_param] = 1.0
    Basis[1, y_param] = 1.0
    Slice_origin = np.zeros(D, float) # Axis views usually start at origin

# QR decomposition version
def assign_basis_from_three_points(p1, p2, p3):
    global Basis, Slice_origin
    A = np.stack([p2 - p1, p3 - p1], axis=1)  # (D,2)
    Q, R = np.linalg.qr(A)
    Basis = Q.T  # (2,D), columns are orthonormal
    Slice_origin = (p1 + p2 + p3) / 3.0  # Center the slice at the centroid of the three points
    
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