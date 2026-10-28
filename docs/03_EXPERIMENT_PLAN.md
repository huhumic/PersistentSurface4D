# 03 Experiment Plan

## Stage 0 — infrastructure gate

### S0.1 GPU/environment audit

Target: RTX 3090 24 GB on Ubuntu.

Record:
- driver;
- CUDA runtime;
- PyTorch;
- total/peak VRAM;
- compute capability.

### S0.2 official Deform3DGS smoke reproduction

Run official EndoNeRF cases before D4D adaptation.

Pass criteria:
- training completes;
- renderer completes;
- exported PLY is readable;
- metrics are finite;
- runtime and peak VRAM are recorded.

No method development starts before this gate passes.

## Stage 1 — D4D adapter and geometry audit

Start with Specimen 1.

Convert one deterministic whole-deformation clip and one incremental clip. Selection must be metadata-based, not chosen after observing model performance.

Pass criteria:
- exact frame-count agreement;
- no silent unit normalization;
- reversible coordinate transform;
- depth/SLC overlay archived.

## Stage 2 — establish geometry floor

On identical pilot clips run:
1. official-style Deform3DGS;
2. Base-G.

Go/no-go:
If Base-G does not improve robust independent geometry on both pilot deformation types, stop M1/M2/M3 and debug geometry/coordinates first.

## Stage 3 — sequential module development

Variants:
- Deform3DGS
- Base-G
- Base-G + M1
- Base-G + M1 + M2
- Full = Base-G + M1 + M2 + M3

M1 gate:
- state transitions must be stable/interpretable;
- direct metric gain may be small.

M2 gate:
- target occluded/out-of-view geometry;
- visible geometry must not materially regress.

M3 gate:
- target reappearance error and long-horizon drift.

Engineering decision signal, not a promised result:
- <5% consistent relative gain on intended subset: weak;
- >=5% across multiple clips: continue;
- >=10% on failure subset with stable overall geometry: strong candidate.

## Stage 4 — external method comparison

First wave:
- Deform3DGS;
- SurgicalGS;
- EndoPlanar;
- ColonSplat;
- Ours.

Second wave:
- PhysioSplat;
- EndoSurf if time permits.

EndoRD-GS and Endo-HDR are related-work references unless executable code becomes available.

## Fairness contract

Adapted methods receive the same canonical RGB, masks, camera poses, split and available stereo depth. Preserve published method-specific settings where feasible. Equal-loss comparisons belong only in controlled ablations.

## Stage 5 — scale-up

Progression:
1. two D4D clips;
2. usable Specimen 1 sessions;
3. multi-specimen evaluation;
4. leave-one-specimen-out only after method/hyperparameters are frozen.

## Stage 6 — external validation

DRENDS:
- depth/temporal external validation.

In-house porcine lungs:
- qualitative reconstruction;
- deformation trajectories;
- visibility states;
- reappearance examples;
- failure cases.

## Required metrics

Geometry in mm:
- mean surface distance;
- median surface distance;
- P95;
- HD95;
- symmetric Chamfer-style distance.

Region-specific:
- visible;
- occluded;
- out-of-view;
- reappearance.

Appearance:
- PSNR;
- SSIM;
- LPIPS on valid non-instrument pixels.

Efficiency:
- training time per clip;
- peak VRAM;
- rendering FPS;
- number of Gaussians.

Every run stores frozen config, repository SHA, third-party SHAs, dataset manifest, seed, GPU snapshot, runtime, metrics and failure status.
