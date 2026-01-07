# Normalization helper

import numpy as np


# --------- math helpers ---------
def to_unit(X, mins, maxs):
    span = np.where((maxs - mins) != 0, (maxs - mins), 1.0)
    return (X - mins) / span

def from_unit(T, mins, maxs):
    return mins + T * (maxs - mins)

# Project to 2-D and back
def project(X, mins, maxs, B):
    """(N,D) -> (N,2) in 0..1"""
    T = to_unit(X, mins, maxs)          # (N,D)
    Y = T @ B                            # (N,2)
    return np.clip(Y, 0.0, 1.0)

def lift(Ysel, mins, maxs, B):
    """(k,2) -> (k,D) projected back onto the plane spanned by B."""
    T_plane = np.clip(Ysel @ B.T, 0.0, 1.0)
    return from_unit(T_plane, mins, maxs)


# Build basis

def basis_from_dims(names, xdim, ydim):
    D = len(names)
    B = np.zeros((D,2), float)
    B[names.index(xdim), 0] = 1.0
    B[names.index(ydim), 1] = 1.0
    return B

def basis_from_three_points(p1, p2, p3):
    # All are (D,) in unit space.
    u = p2 - p1
    u /= np.linalg.norm(u) + 1e-12
    w = p3 - p1
    # Gram–Schmidt: v = w - (u·w)u
    v = w - np.dot(u, w) * u
    v /= np.linalg.norm(v) + 1e-12
    # Pack as columns
    return np.stack([u, v], axis=1)   # (D,2)
