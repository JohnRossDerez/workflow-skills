"""CPU example of restoration, state export, and owned-resource cleanup.

This model is a stand-in; it does not establish any ML library's semantics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class Model:
    weight: int = 0
    step: int = 0
    closed: bool = False

    def restore(self, snapshot: dict[str, int]) -> None:
        self.weight = snapshot["weight"]
        self.step = snapshot["step"]

    def train_to(self, target_step: int) -> None:
        self.weight += target_step - self.step
        self.step = target_step

    def close(self) -> None:
        self.closed = True


def load_snapshot(checkpoint: Path) -> dict[str, int]:
    snapshot = json.loads(checkpoint.read_text())
    if not isinstance(snapshot, dict):
        raise ValueError("checkpoint must be an object")
    for field in ("weight", "step"):
        if type(snapshot.get(field)) is not int:
            raise ValueError(f"checkpoint {field} must be an integer")
    if snapshot["step"] < 0:
        raise ValueError("checkpoint step cannot be negative")
    return {"weight": snapshot["weight"], "step": snapshot["step"]}


def publish_state(model: Model, output: Path) -> None:
    payload = json.dumps({"weight": model.weight, "step": model.step})
    temporary = output.with_name(output.name + ".pending")
    try:
        temporary.write_text(payload)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def run_export(
    checkpoint: Path,
    output: Path,
    target_step: int,
    acquire: Callable[[], Model] = Model,
) -> None:
    if type(target_step) is not int or target_step < 0:
        raise ValueError("target step must be a nonnegative integer")
    snapshot = load_snapshot(checkpoint)
    model = acquire()
    try:
        model.restore(snapshot)
        if model.step < target_step:
            model.train_to(target_step)
        publish_state(model, output)
    finally:
        model.close()


def broken_completed_export(
    checkpoint: Path, output: Path, target_step: int, acquire: Callable[[], Model]
) -> None:
    """Historical failure pattern: skip training without restoring completed state."""
    snapshot = load_snapshot(checkpoint)
    model = acquire()
    try:
        if snapshot["step"] < target_step:
            model.restore(snapshot)
            model.train_to(target_step)
        publish_state(model, output)
    finally:
        model.close()
