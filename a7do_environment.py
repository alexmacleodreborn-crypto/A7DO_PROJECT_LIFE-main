"""
Runnable A7DO environment bootstrap.
Builds a complete agent + world loop from the existing project files.
"""

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LifeLoop = load_module(
    "life_loop",
    "00_CORE_EXISTENCE/bootstrap/life_loop.py",
).LifeLoop
Dashboard = load_module(
    "dashboard",
    "12_INTERFACE_AND_OBSERVABILITY/dashboard.py",
).Dashboard


def build_environment():
    return LifeLoop()


def run_environment(ticks: int = 10):
    life = build_environment()
    for _ in range(ticks):
        if not life.pulse.is_alive():
            break
        life.tick()
    return life


def main():
    parser = argparse.ArgumentParser(description="Run the A7DO world environment.")
    parser.add_argument("--ticks", type=int, default=10, help="Number of ticks to run.")
    parser.add_argument(
        "--render-dashboard",
        action="store_true",
        help="Render the text dashboard after running.",
    )
    args = parser.parse_args()

    life = run_environment(ticks=args.ticks)
    snapshot = life.snapshot.capture()

    print(json.dumps(snapshot["world"], indent=2))

    if args.render_dashboard:
        print()
        print(Dashboard(life.snapshot).render_text())


if __name__ == "__main__":
    main()
