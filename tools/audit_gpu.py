#!/usr/bin/env python3
"""Emit a reproducibility snapshot of GPU/PyTorch."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path


def _cmd(args: list[str]) -> str | None:
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()
    except Exception:
        return None


def main() -> int:
    report: dict[str, object] = {
        "python": sys.version,
        "platform": platform.platform(),
        "nvidia_smi": _cmd(["nvidia-smi"]),
    }
    try:
        import torch
        report.update({
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
        })
        if torch.cuda.is_available():
            devices = []
            for i in range(torch.cuda.device_count()):
                p = torch.cuda.get_device_properties(i)
                devices.append({
                    "index": i,
                    "name": p.name,
                    "compute_capability": list(torch.cuda.get_device_capability(i)),
                    "total_memory_gb": round(p.total_memory / (1024**3), 3),
                })
            report["devices"] = devices
    except Exception as exc:
        report["torch_import_error"] = repr(exc)

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if len(sys.argv) > 1:
        out = Path(sys.argv[1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
