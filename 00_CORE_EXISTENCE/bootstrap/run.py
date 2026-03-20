import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_local_module(name: str, filename: str):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


initialize_seed = load_local_module(
    "seed_init",
    "seed_init.py",
).initialize_seed

def run():
    core = initialize_seed()
    print("A7DO initialized")
    print(core["identity"].as_dict())

if __name__ == "__main__":
    run()
