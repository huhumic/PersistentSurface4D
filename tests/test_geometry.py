import numpy as np
from src.evaluation.geometry import geometry_metrics_mm


def test_identical_clouds_are_zero():
    x = np.array([[0.,0.,0.],[0.01,0.,0.],[0.,0.01,0.]])
    m = geometry_metrics_mm(x, x)
    assert m["symmetric_mean_mm"] == 0.0
    assert m["hd95_mm"] == 0.0


def test_one_mm_translation_is_detected():
    x = np.array([[0.,0.,0.],[0.02,0.,0.],[0.,0.02,0.]])
    y = x + np.array([0.001,0,0])
    m = geometry_metrics_mm(x, y)
    assert 0.9 <= m["symmetric_mean_mm"] <= 1.1
