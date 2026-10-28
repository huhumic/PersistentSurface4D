"""Common physical-space point-cloud geometry metrics.

Inputs are metres. Outputs are millimetres.
"""
from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree


def _as_points(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 3 or len(x) == 0:
        raise ValueError(f"Expected non-empty Nx3 array, got {x.shape}")
    if not np.isfinite(x).all():
        raise ValueError("Point cloud contains NaN/Inf")
    return x


def directed_distances_m(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    src, dst = _as_points(src), _as_points(dst)
    d, _ = cKDTree(dst).query(src, k=1, workers=-1)
    return d


def geometry_metrics_mm(pred_m: np.ndarray, gt_m: np.ndarray) -> dict[str, float]:
    pred_m, gt_m = _as_points(pred_m), _as_points(gt_m)
    p2g = directed_distances_m(pred_m, gt_m)
    g2p = directed_distances_m(gt_m, pred_m)
    sym_mm = np.concatenate([p2g, g2p]) * 1000.0
    p2g_mm, g2p_mm = p2g * 1000.0, g2p * 1000.0
    return {
        "pred_to_gt_mean_mm": float(p2g_mm.mean()),
        "gt_to_pred_mean_mm": float(g2p_mm.mean()),
        "symmetric_mean_mm": float(sym_mm.mean()),
        "symmetric_median_mm": float(np.median(sym_mm)),
        "symmetric_p95_mm": float(np.percentile(sym_mm, 95)),
        "hd95_mm": float(max(np.percentile(p2g_mm, 95), np.percentile(g2p_mm, 95))),
        "chamfer_l2_mm2": float((np.mean(p2g**2) + np.mean(g2p**2)) * 1e6),
    }
