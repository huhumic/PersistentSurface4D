"""Framework-light interfaces for M1/M2/M3."""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Protocol

import torch


class SurfaceState(IntEnum):
    VISIBLE = 0
    OCCLUDED = 1
    OUT_OF_VIEW = 2
    INVALID = 3


@dataclass
class SurfaceMemory:
    state: torch.Tensor
    confidence: torch.Tensor
    age: torch.Tensor
    history: torch.Tensor


class MemoryUpdater(Protocol):
    def __call__(self, *, xyz: torch.Tensor, observation: dict, previous: SurfaceMemory) -> SurfaceMemory: ...


class DeformationPropagator(Protocol):
    def __call__(self, *, base_xyz: torch.Tensor, memory: SurfaceMemory, anchors: dict) -> torch.Tensor: ...


class ReappearanceCorrector(Protocol):
    def loss(self, *, predicted_xyz: torch.Tensor, observation: dict, memory: SurfaceMemory) -> torch.Tensor: ...
