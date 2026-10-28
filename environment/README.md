# Environment strategy

Use separate environments for preprocessing and legacy 3DGS baselines.

## ps4d-prep

Purpose:
- D4D/DRENDS preprocessing;
- coordinate audits;
- common evaluation.

Recommended:
- Python 3.10+
- numpy/scipy/pillow/pyyaml
- open3d
- trimesh
- opencv-python

## ps4d-deform

Purpose:
- faithful Deform3DGS reproduction on RTX 3090.

Start from upstream dependency versions instead of forcing the preprocessing environment onto legacy CUDA extensions. Freeze exact versions after the first successful build.

## Policy

- Do not force all baselines into one environment.
- Save pip freeze, nvidia-smi, PyTorch/CUDA versions and CUDA extension build logs with each baseline's first successful run.
