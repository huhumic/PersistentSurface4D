import numpy as np
from src.evaluation.visibility import Visibility, classify_visibility


def test_visibility_states():
    depth = np.ones((4, 4), dtype=np.float32)
    mask = np.ones((4, 4), dtype=bool)
    uv = np.array([[1,1], [2,2], [10,10]], dtype=float)
    z = np.array([1.0, 1.1, 1.0], dtype=float)
    s = classify_visibility(uv, z, depth, mask, tau_m=0.02)
    assert s[0] == Visibility.VISIBLE
    assert s[1] == Visibility.OCCLUDED
    assert s[2] == Visibility.OUT_OF_VIEW
