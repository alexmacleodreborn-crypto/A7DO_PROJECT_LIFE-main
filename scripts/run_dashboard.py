import importlib.util
from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# LOAD MODULES (NUMBERED FOLDERS SAFE)
# --------------------------------------------------
visual_mod = load_module(
    "visualisation",
    "12_INTERFACE_AND_OBSERVABILITY/visualisation.py",
)
snapshot_mod = load_module(
    "snapshot",
    "12_INTERFACE_AND_OBSERVABILITY/snapshot.py",
)
world_mod = load_module(
    "world_state",
    "09_WORLD_MODEL/world_state.py",
)
world_env_mod = load_module(
    "world_env",
    "09_WORLD_MODEL/environments/world.py",
)
memory_mod = load_module(
    "episodic",
    "07_MEMORY_SYSTEM/episodic.py",
)
attention_mod = load_module(
    "attention",
    "06_LIMBIC_AND_VALUE_SYSTEM/attention.py",
)
prediction_mod = load_module(
    "prediction",
    "09_WORLD_MODEL/prediction.py",
)
council_mod = load_module(
    "council",
    "10_MULTI_AGENT_COUNCIL/council.py",
)

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
WebDashboard = visual_mod.WebDashboard
IntrospectionSnapshot = snapshot_mod.IntrospectionSnapshot

WorldState = world_mod.WorldState
World = world_env_mod.World
EpisodicMemory = memory_mod.EpisodicMemory
AttentionSystem = attention_mod.AttentionSystem
Predictor = prediction_mod.Predictor
Council = council_mod.Council


def build_system():
    world = WorldState(default_place="house")
    World.create(world_state=world)
    memory = EpisodicMemory(capacity=20)
    attention = AttentionSystem(memory, focus_size=5)
    predictor = Predictor(world, memory)
    council = Council(world, memory, predictor, attention)

    # Seed with something visible
    memory.record({"type": "pain_withdrawal", "strain": 0.9}, salience=0.8)
    world.update(energy=4.0, strain=0.7)

    snapshot = IntrospectionSnapshot(
        world, memory, attention, predictor, council
    )
    return snapshot


if __name__ == "__main__":
    snapshot = build_system()
    WebDashboard(snapshot).run()
