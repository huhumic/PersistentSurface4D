#!/usr/bin/env python3
"""Audit a canonical scene before training. This never modifies data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def _files(path: Path, suffixes: tuple[str, ...]) -> list[Path]:
    return sorted(p for p in path.iterdir() if p.is_file() and p.suffix.lower() in suffixes)


def audit(root: Path) -> dict:
    required = ["images", "right_images", "depth_npy", "masks", "gt", "meta.json", "split.json", "transform_manifest.json"]
    missing = [x for x in required if not (root / x).exists()]
    if missing:
        raise RuntimeError(f"Missing required entries: {missing}")

    left = _files(root / "images", (".png", ".jpg", ".jpeg"))
    right = _files(root / "right_images", (".png", ".jpg", ".jpeg"))
    depth = _files(root / "depth_npy", (".npy",))
    masks = _files(root / "masks", (".png", ".jpg", ".jpeg"))

    counts = {"left": len(left), "right": len(right), "depth": len(depth), "masks": len(masks)}
    if len(set(counts.values())) != 1 or not left:
        raise RuntimeError(f"Frame-count mismatch: {counts}")

    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    if meta.get("depth_unit") not in {"m", "meter", "metre"}:
        raise RuntimeError(f"depth_unit must be metres, got {meta.get('depth_unit')!r}")

    sample_ids = sorted({0, len(left)//2, len(left)-1})
    depth_stats = []
    for i in sample_ids:
        im = np.asarray(Image.open(left[i]))
        ma = np.asarray(Image.open(masks[i]))
        de = np.load(depth[i])
        if de.ndim != 2:
            raise RuntimeError(f"Depth must be HxW at frame {i}, got {de.shape}")
        h, w = de.shape
        if im.shape[:2] != (h, w):
            raise RuntimeError(f"RGB/depth mismatch at frame {i}")
        if ma.shape[:2] != (h, w):
            raise RuntimeError(f"Mask/depth mismatch at frame {i}")
        valid = de[np.isfinite(de) & (de > 0)]
        if valid.size == 0:
            raise RuntimeError(f"No valid positive depth at frame {i}")
        depth_stats.append({
            "frame": i,
            "min_m": float(valid.min()),
            "median_m": float(np.median(valid)),
            "p99_m": float(np.percentile(valid, 99)),
            "max_m": float(valid.max()),
        })

    for ply in (root/"gt"/"start.ply", root/"gt"/"end.ply"):
        if not ply.exists() or ply.stat().st_size == 0:
            raise RuntimeError(f"Missing/empty independent SLC GT: {ply}")

    split = json.loads((root / "split.json").read_text(encoding="utf-8"))
    for key in ("train", "test"):
        if key not in split or not isinstance(split[key], list):
            raise RuntimeError(f"split.json missing list {key!r}")

    return {
        "scene": str(root),
        "counts": counts,
        "sample_depth_stats": depth_stats,
        "train_frames": len(split["train"]),
        "test_frames": len(split["test"]),
        "status": "PASS",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scene", type=Path)
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args()
    try:
        report = audit(args.scene)
        code = 0
    except Exception as exc:
        report = {"scene": str(args.scene), "status": "FAIL", "error": repr(exc)}
        code = 2

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
