# lifecycle/transitions.py

import importlib.util
from pathlib import Path


def _load_local_module(name: str, filename: str):
    here = Path(__file__).resolve().parent
    path = here / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stages_mod = _load_local_module("stages", "stages.py")
LifeStage = stages_mod.LifeStage

VALID_TRANSITIONS = {
    LifeStage.SEED: LifeStage.WOMB,
    LifeStage.WOMB: LifeStage.BIRTH,
    LifeStage.BIRTH: LifeStage.INFANT,
    LifeStage.INFANT: LifeStage.TODDLER,
    LifeStage.TODDLER: LifeStage.CHILD,
    LifeStage.CHILD: LifeStage.ADOLESCENT,
    LifeStage.ADOLESCENT: LifeStage.ADULT,
}

class LifecycleManager:
    def __init__(self):
        self.stage = LifeStage.SEED

    def advance(self):
        if self.stage not in VALID_TRANSITIONS:
            raise RuntimeError("Invalid lifecycle transition")
        self.stage = VALID_TRANSITIONS[self.stage]
        return self.stage
