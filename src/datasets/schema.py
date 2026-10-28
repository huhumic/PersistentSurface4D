from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class CanonicalScene:
    root: Path

    @property
    def images(self) -> Path:
        return self.root / "images"

    @property
    def right_images(self) -> Path:
        return self.root / "right_images"

    @property
    def depth_npy(self) -> Path:
        return self.root / "depth_npy"

    @property
    def masks(self) -> Path:
        return self.root / "masks"

    @property
    def gt_start(self) -> Path:
        return self.root / "gt" / "start.ply"

    @property
    def gt_end(self) -> Path:
        return self.root / "gt" / "end.ply"

    def meta(self) -> dict:
        return json.loads((self.root / "meta.json").read_text(encoding="utf-8"))

    def split(self) -> dict:
        return json.loads((self.root / "split.json").read_text(encoding="utf-8"))
