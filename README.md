# PersistentSurface4D

Research codebase for **non-rigid soft-tissue dynamic optical surface reconstruction**.

## Scope

This repository supports the second thesis research point:

- Research point 1: continuous 4D medical image reconstruction.
- Research point 2: non-rigid soft-tissue dynamic optical surface reconstruction.
- Unified system: volumetric reconstruction + optical surface reconstruction + deformation visualization.

The optical branch studies persistent metric surface reconstruction under partial visibility, occlusion and reappearance.

## Proposed method

Engineering backbone: Deform3DGS.

Non-novel geometry floor:
- Base-G: Deform3DGS + metric depth supervision + optional normal/smoothness constraints.

Proposed modules:
1. M1 — Visibility-state Surface Memory.
2. M2 — Reliability-guided Deformation Propagation.
3. M3 — Reappearance Consistency Correction.

## Dataset roles

- D4D: primary quantitative benchmark.
- DRENDS: external depth/temporal validation.
- Two in-house ex-vivo porcine-lung inflation experiments: qualitative feasibility only.

## Non-negotiable protocol

- D4D stereo depth may be used as training/observation geometry.
- D4D structured-light point clouds are evaluation-only and must never enter training/tuning losses.
- All geometric errors are transformed back to physical coordinates and reported in mm.
- Every run records config, commit SHA, dataset manifest, seed, GPU, runtime and metrics.
- Baselines use the same RGB/mask/camera/split inputs while preserving method-specific losses where feasible.

See docs/03_EXPERIMENT_PLAN.md for the locked execution sequence.
