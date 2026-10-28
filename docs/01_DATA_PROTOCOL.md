# 01 Data Protocol

## Dataset roles

### D4D — primary quantitative benchmark

Phase-1 development uses Specimen 1 first. Retain per selected clip/session:

- rectified left/right RGB;
- masks;
- stereo depth in original floating-point metric units;
- intrinsics and curated camera poses;
- start/end structured-light point clouds;
- clip/session metadata.

### DRENDS — external validation

Start from DRENDS_ExVivo_Sequences.zip. Do not download large video packages until a temporal experiment explicitly needs them.

### In-house porcine lungs — qualitative only

Use for reconstruction/deformation visualization and failure analysis, not population-level quantitative generalization.

## Data separation

Training/observation geometry:
- D4D stereo depth may be used by Base-G, M2 and M3.

Independent evaluation geometry:
- D4D structured-light point clouds are never used in optimization or hyperparameter selection.

## Canonical scene format

scene/
- images/
- right_images/
- depth_npy/
- depth/
- masks/
- poses_bounds.npy
- intrinsics.json
- gt/start.ply
- gt/end.ply
- curated_pose_start.txt
- curated_pose_end.txt
- split.json
- transform_manifest.json
- meta.json

## Coordinate contract

Every scene declares:

D4D metric frame -> camera/model frame -> normalization -> prediction -> inverse transform -> D4D metric frame

No paper metric may be reported from normalized internal coordinates.

## Required audit

Before training verify:
- image/depth/mask counts match;
- depth values are finite and physically plausible where valid;
- mask resolution matches rectified RGB;
- camera matrices are finite and invertible;
- structured-light point clouds are readable;
- depth/SLC overlays are visually coherent;
- unit conversion is explicit and reversible.
