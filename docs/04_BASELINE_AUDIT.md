# 04 Baseline Audit

Snapshot date: 2026-10-28.

| Repository | Role | Pinned commit | Status |
|---|---|---|---|
| jinlab-imvr/Deform3DGS | mother model | b06f0a501bd1c71aa70d9a48a8dd4810ccddb2b7 | complete training/render/data code; legacy stack |
| neneyork/SurgicalGS | geometry baseline/reference | 62f6d5fa4031685edb01f2efa8a63b004db8110b | usable; depth/smoothness terms present |
| ThatphumCpre/EndoPlanar | geometry baseline/reference | f5fd519319e901ad4c7f6b60e6c550c71fc5d7f6 | usable; depth/normal/planar terms present |
| wMito/ColonSplat | recent geometry competitor | d317a4e7d1541290ab9478ba11658bbed2020afa | active; geometry evaluation present |
| hritam-98/physiosplat | optional recent comparator | 54c38915e64f1e9c300a638b15614043d44fff17 | public model/trainer/tests; heavier |
| reubendocea/d4d | official dataset loader | 38c464f80c1c51b5922e187cc5fa07418b72f1b9 | active official loader |

## Implementation notes

Deform3DGS:
- native EndoNeRF-style loader;
- 3000-iteration EndoNeRF config;
- flexible deformation is a practical insertion point for persistent memory;
- first reproduction should use RTX 3090 rather than forcing legacy CUDA extensions onto a Blackwell laptop.

SurgicalGS:
- explicit rendered depth, GT depth and smoothness/TV losses;
- use as geometry baseline/reference, not novelty source.

EndoPlanar:
- plane depth, rendered/depth-derived normals, scaling regularization and depth/TV terms;
- useful geometry reference.

ColonSplat:
- important recent geometry competitor with Chamfer/Hausdorff/HD95-style evaluation.

PhysioSplat:
- HexPlane deformation, biomechanics, tool/tissue handling, heavier 30k-iteration design;
- keep as second-wave comparator.

Not mandatory executable baselines:
- EndoRD-GS: public repository currently lacks implementation.
- Endo-HDR: code not currently released.
