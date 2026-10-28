"""Deterministic visibility-state classification."""
from __future__ import annotations

from enum import IntEnum
import numpy as np


class Visibility(IntEnum):
    VISIBLE = 0
    OCCLUDED = 1
    OUT_OF_VIEW = 2
    INVALID = 3


def classify_visibility(
    uv: np.ndarray,
    z_m: np.ndarray,
    depth_m: np.ndarray,
    valid_mask: np.ndarray,
    tau_m: float,
) -> np.ndarray:
    uv = np.asarray(uv)
    z_m = np.asarray(z_m)
    h, w = depth_m.shape
    if uv.shape != (len(z_m), 2):
        raise ValueError("uv must be Nx2 and match z")

    state = np.full(len(z_m), Visibility.OUT_OF_VIEW, dtype=np.uint8)
    u = np.rint(uv[:, 0]).astype(np.int64)
    v = np.rint(uv[:, 1]).astype(np.int64)

    inside = (u >= 0) & (u < w) & (v >= 0) & (v < h) & np.isfinite(z_m) & (z_m > 0)
    idx = np.flatnonzero(inside)
    if not len(idx):
        return state

    d = depth_m[v[idx], u[idx]]
    m = valid_mask[v[idx], u[idx]].astype(bool)
    valid = m & np.isfinite(d) & (d > 0)

    state[idx[~valid]] = Visibility.INVALID
    good = idx[valid]
    residual = z_m[good] - depth_m[v[good], u[good]]

    state[good[np.abs(residual) <= tau_m]] = Visibility.VISIBLE
    state[good[residual > tau_m]] = Visibility.OCCLUDED
    state[good[residual < -tau_m]] = Visibility.INVALID
    return state
