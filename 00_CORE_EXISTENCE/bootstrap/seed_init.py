import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SelfIdentity = load_module(
    "self_id",
    "00_CORE_EXISTENCE/identity/self_id.py",
).SelfIdentity
SystemClock = load_module(
    "clock",
    "00_CORE_EXISTENCE/heartbeat/clock.py",
).SystemClock
Pulse = load_module(
    "pulse",
    "00_CORE_EXISTENCE/heartbeat/pulse.py",
).Pulse

def initialize_seed():
    identity = SelfIdentity()
    clock = SystemClock()
    pulse = Pulse()

    return {
        "identity": identity,
        "clock": clock,
        "pulse": pulse
    }
