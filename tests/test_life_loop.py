import importlib.util
from pathlib import Path
import pytest

# --------------------------------------------------
# Load life_loop via file path (numbered folders safe)
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

def load_life_loop():
    path = ROOT / "00_CORE_EXISTENCE/bootstrap/life_loop.py"
    spec = importlib.util.spec_from_file_location("life_loop", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LifeLoop

# --------------------------------------------------
# TESTS
# --------------------------------------------------

def test_withdrawal_without_energy_triggers_shutdown():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    # Drain all energy manually
    life.energy.available = 0.0

    # Force strain high enough to cause pain
    life.overload.strain = 1.0

    life.tick()

    assert not life.pulse.is_alive(), "Life should shut down with no energy"


def test_memory_write_consumes_energy():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    energy_before = life.energy.level()

    life.record_memory(
        event={"type": "test", "time": 0.0},
        salience=0.5
    )

    energy_after = life.energy.level()

    assert energy_after < energy_before, "Memory write must consume energy"


def test_salience_attached_to_memory():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    life.record_memory(
        event={"type": "salience_test", "time": 1.0},
        salience=0.9
    )

    memories = life.memory.recent(1)
    memory = memories[0]

    memory_id = f"{memory['event']['type']}_{memory['time']}"

    assert life.salience.get(memory_id) == 0.9, "Salience must be stored correctly"

def test_proprioception_only_after_motor():
    LifeLoop = load_life_loop()
    life = LifeLoop(stage_schedule=[(0, "infant")])

    # Force pain condition
    life.overload.strain = 1.0

    life.tick()

    # Look for proprioception in memory
    memories = life.memory.recent(5)
    found = any(
        m["event"]["type"] == "pain_withdrawal"
        and "body_state" in m["event"]
        for m in memories
    )

    assert found, "Proprioception should be recorded after withdrawal"

def test_physics_gate_blocks_illegal_energy_use():
    LifeLoop = load_life_loop()
    life = LifeLoop()

    # Set energy lower than base cost
    life.energy.available = 0.1

    life.tick()

    assert not life.pulse.is_alive(), "PhysicsGate must enforce shutdown on violation"


def test_lifecycle_progresses_pregnancy_birth_infant_then_next():
    LifeLoop = load_life_loop()

    # Compressed developmental timeline to validate stage ordering.
    life = LifeLoop(
        stage_schedule=[
            (0, "womb"),
            (2, "birth"),
            (3, "infant"),
            (5, "toddler"),
        ]
    )

    stages = []
    for _ in range(6):
        life.tick()
        stages.append(life.lifecycle.stage)

    assert "womb" in stages, "Pregnancy (womb) stage should occur first"
    assert "birth" in stages, "Birth stage should occur after womb"
    assert "infant" in stages, "Infant stage should occur after birth"
    assert "toddler" in stages, "Next stage should occur after infant"

    womb_i = stages.index("womb")
    birth_i = stages.index("birth")
    infant_i = stages.index("infant")
    toddler_i = stages.index("toddler")

    assert womb_i < birth_i < infant_i < toddler_i
