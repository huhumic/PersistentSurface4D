# 02 Method Design

## Backbone

Pinned Deform3DGS is the engineering mother model. Third-party code is cloned at fixed commits; modifications are isolated as patches/wrappers or a documented fork.

## Base-G — geometry-strengthened backbone

Base-G is not claimed as novel.

Objective:

L_base = L_rgb + lambda_d L_metric_depth + lambda_n L_normal + lambda_s L_smooth

- L_metric_depth: robust metric depth residual; preserve physical scale.
- L_normal: optional local normal consistency derived from metric depth.
- L_smooth: conservative geometry regularization.
- Structured-light GT is forbidden from these losses.

## M1 — Visibility-state Surface Memory

Each primitive stores:

- state in {VISIBLE, OCCLUDED, OUT_OF_VIEW, INVALID};
- observation confidence;
- age since reliable observation;
- compact motion/history state.

State is derived from projection, mask validity and rendered-vs-observed depth consistency.

Densification/pruning must clone/delete memory tensors with the same index mapping as Gaussian parameters.

## M2 — Reliability-guided Deformation Propagation

M2 is tied to the persistent metric Gaussian map.

For reliable visible anchor j:

e_j = x_obs_j - x_base_j

For unobserved primitive i over a canonical KNN graph:

r_i = sum_j alpha_ij e_j

Initial analytical alpha_ij uses:
- observation confidence;
- canonical distance;
- normal similarity;
- optional history agreement.

Only introduce a tiny learned weighting model if analytical weighting first produces a reproducible positive signal.

## M3 — Reappearance Consistency Correction

Detect cycles:

VISIBLE -> OCCLUDED/OUT_OF_VIEW -> VISIBLE

When a primitive becomes visible again, compare predicted metric geometry against the new stereo observation and penalize accumulated drift.

Because Deform3DGS samples random training frames, reappearance pairs are maintained by a chronological cache refreshed periodically.

## Full objective

L = L_base + lambda_p L_prop + lambda_r L_reappear

M1 is primarily a persistent state mechanism, not a forced standalone loss.
