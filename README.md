# A7DO Project Life

## Foundation snapshot

A7DO is defined as a life-like system that develops, moves, feels, spends energy, and fails physically before it can think.
This foundation now unifies AI, SLED learning, embodied development, and robotics into a single mathematical framework.

### What is formalized

- **Organism state equation** for full-system dynamics.
- **Robotics dynamics** (Lagrangian, muscles, joints) for embodied control.
- **Nervous system model** from neurons to fields to reflex arcs.
- **Energy + metabolism constraints** to govern feasible behavior.
- **SLED learning as variational physics**, not reward hacks.
- **Cognition gated by biology**, not assumed.
- **Developmental law** that prevents symbol-first cognition.

### Core consequence

> Nothing thinks unless it can move, feel, burn energy, and fail physically.

### Selected next step

1. **Extend this into a control-theory appendix** (stability, Lyapunov, safety).

### Scenario example

```python
import importlib.util
from pathlib import Path

scenario_path = Path("09_WORLD_MODEL/environments/scenarios/a7do_world.py")
spec = importlib.util.spec_from_file_location("a7do_world", scenario_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print(module.A7DO_BORN_PERSON_WORLD.describe_world())
```
