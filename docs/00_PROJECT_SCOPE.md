# 00 Project Scope

## Thesis positioning

Research point 2 is an independent method study. It does not need to form a serial pipeline with research point 1. The two are unified at system level through dynamic anatomy/deformation representation and visualization.

## Scientific question

Given calibrated optical observations of deforming soft tissue, how can a metric 3D surface remain geometrically accurate when regions transition through:

visible -> occluded/out-of-view -> re-visible

The project prioritizes geometry over novel-view rendering quality.

## Design targets

These are engineering targets, not publication claims until supported experimentally:

- M1: persistent visibility state and observation confidence.
- M2: reliability-aware propagation from trustworthy observed regions to currently unobserved regions.
- M3: geometric correction when unobserved regions re-enter view.

## Claims forbidden without evidence

- Do not claim first prediction of out-of-view soft-tissue deformation; SeeSaw already addresses this problem class.
- Do not call the in-house data clinical thoracoscopy.
- Do not call ex-vivo positive-pressure inflation physiological respiratory motion.
- Do not describe D4D structured-light geometry as error-free or sub-millimetre ground truth.
