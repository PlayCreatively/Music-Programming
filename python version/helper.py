"""
Mathematical helper functions for vector operations and projections.
"""

import numpy as np
import imgui
import globals as G

# --- Color Helpers ---
def rgba_f(r, g, b, a=255):
    """Convert 0–255 RGB to 0–1 RGBA float tuple."""
    return r / 255.0, g / 255.0, b / 255.0, a / 255.0

def rgba_u32(r, g, b, a=255):
    """Convert 0–255 RGBA to ImGui packed color (for draw_list)."""
    return imgui.get_color_u32_rgba(*rgba_f(r, g, b, a))

# --- Math helpers ---
def to_unit(X, mins, maxs):
    """Normalize X values to 0..1 range based on mins and maxs."""
    span = np.where((maxs - mins) != 0, (maxs - mins), 1.0)
    return (X - mins) / span

def from_unit(T, mins, maxs):
    """Denormalize 0..1 values T back to original range."""
    return mins + T * (maxs - mins)

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
            # Find the smallest positive t that hits a boundary, assuming start is valid [0,1].
            if t >= 0:
                t_max = t

    t_max = max(0.0, min(t_max, 1.0))
    return start + t_max * direction

def pca_basis(points: np.ndarray, dim: int=2) -> np.ndarray:
    """Compute the top 'dim' principal components of the given points."""
    # Center the points
    centered = points - np.mean(points, axis=0)
    # Compute covariance matrix
    cov = np.cov(centered, rowvar=False)
    # Eigen decomposition
    eigvals, eigvecs = np.linalg.eigh(cov)
    # Sort eigenvectors by eigenvalues in descending order
    sorted_indices = np.argsort(eigvals)[::-1]
    top_eigvecs = eigvecs[:, sorted_indices[:dim]]
    return top_eigvecs.T  # Return as (dim, D)

# --- UI Helpers ---
def is_cursor_within_circle(circle_center, radius) -> bool:
    """Check if the cursor is within a circle defined by center and radius."""
    dx = G.mouse_pos[0] - circle_center[0]
    dy = G.mouse_pos[1] - circle_center[1]
    
    distance_squared = dx * dx + dy * dy
    return distance_squared <= radius * radius
