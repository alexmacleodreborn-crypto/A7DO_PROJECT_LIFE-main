"""
A7DO Minimal Runnable Life Loop (MRLL)
TEST-LOCKED CORE + WORLD INTEGRATION
"""

import time
import importlib.util
from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# CORE
# --------------------------------------------------
self_id_mod = load_module("self_id", "00_CORE_EXISTENCE/identity/self_id.py")
clock_mod = load_module("clock", "00_CORE_EXISTENCE/heartbeat/clock.py")
pulse_mod = load_module("pulse", "00_CORE_EXISTENCE/heartbeat/pulse.py")

# --------------------------------------------------
# PHYSICS
# --------------------------------------------------
physics_mod = load_module("physics_gate", "01_PHYSICS_SANITY_SANDYS_LAW/gating.py")

# --------------------------------------------------
# METABOLISM
# --------------------------------------------------
energy_mod = load_module("energy_budget", "05_METABOLISM_AND_HOMEOSTASIS/energy_budget.py")
recovery_mod = load_module("recovery", "05_METABOLISM_AND_HOMEOSTASIS/recovery.py")
overload_mod = load_module("overload", "05_METABOLISM_AND_HOMEOSTASIS/overload.py")
regulation_mod = load_module("regulation", "05_METABOLISM_AND_HOMEOSTASIS/regulation.py")

# --------------------------------------------------
# SAFETY
# --------------------------------------------------
shutdown_mod = load_module("shutdown", "11_SAFETY_AND_GOVERNANCE/shutdown_authority.py")

# --------------------------------------------------
# BODY
# --------------------------------------------------
reflex_mod = load_module("reflex", "02_NERVOUS_SYSTEM/peripheral_nervous_system/reflexes.py")
motor_mod = load_module("motor", "03_BODY_SYSTEM/motor_control/gross_motor.py")
proprio_mod = load_module("proprio", "04_SENSORY_SYSTEM/proprioception/body_orientation.py")

# --------------------------------------------------
# MEMORY
# --------------------------------------------------
episodic_mod = load_module("episodic", "07_MEMORY_SYSTEM/episodic.py")

# --------------------------------------------------
# LIFECYCLE
# --------------------------------------------------
lifecycle_stages_mod = load_module(
    "lifecycle_stages",
    "00_CORE_EXISTENCE/lifecycle/stages.py",
)
lifecycle_transitions_mod = load_module(
    "lifecycle_transitions",
    "00_CORE_EXISTENCE/lifecycle/transitions.py",
)

# --------------------------------------------------
# DEVELOPMENT
# --------------------------------------------------
embryonic_mod = load_module("embryonic", "08_DEVELOPMENT_SYSTEM/embryonic.py")
infant_mod = load_module("infant", "08_DEVELOPMENT_SYSTEM/infant.py")
toddler_mod = load_module("toddler", "08_DEVELOPMENT_SYSTEM/toddler.py")
child_mod = load_module("child", "08_DEVELOPMENT_SYSTEM/child.py")
adolescent_mod = load_module("adolescent", "08_DEVELOPMENT_SYSTEM/adolescent.py")
adult_mod = load_module("adult", "08_DEVELOPMENT_SYSTEM/adult.py")

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
SelfIdentity = self_id_mod.SelfIdentity
SystemClock = clock_mod.SystemClock
Pulse = pulse_mod.Pulse

PhysicsGate = physics_mod.PhysicsGate

EnergyBudget = energy_mod.EnergyBudget
RecoverySystem = recovery_mod.RecoverySystem
OverloadMonitor = overload_mod.OverloadMonitor
HomeostasisRegulator = regulation_mod.HomeostasisRegulator

ShutdownAuthority = shutdown_mod.ShutdownAuthority

ReflexArc = reflex_mod.ReflexArc
GrossMotor = motor_mod.GrossMotor
BodyOrientationSense = proprio_mod.BodyOrientationSense

EpisodicMemory = episodic_mod.EpisodicMemory

LifeStage = lifecycle_stages_mod.LifeStage
LifecycleManager = lifecycle_transitions_mod.LifecycleManager

EmbryonicStage = embryonic_mod.EmbryonicStage
InfantStage = infant_mod.InfantStage
ToddlerStage = toddler_mod.ToddlerStage
ChildStage = child_mod.ChildStage
AdolescentStage = adolescent_mod.AdolescentStage
AdultStage = adult_mod.AdultStage
WorldTime = load_module("world_time", "09_WORLD_MODEL/time.py").WorldTime
WorldState = load_module("world_state", "09_WORLD_MODEL/world_state.py").WorldState
AttentionSystem = load_module(
    "attention",
    "06_LIMBIC_AND_VALUE_SYSTEM/attention.py",
).AttentionSystem
ActionEnergyLearner = load_module(
    "energy_learning",
    "03_BODY_SYSTEM/motor_control/energy_learning.py",
).ActionEnergyLearner
Predictor = load_module(
    "predictor",
    "09_WORLD_MODEL/prediction.py",
).Predictor
Council = load_module(
    "council",
    "10_MULTI_AGENT_COUNCIL/council.py",
).Council
IntrospectionSnapshot = load_module(
    "snapshot",
    "12_INTERFACE_AND_OBSERVABILITY/snapshot.py",
).IntrospectionSnapshot


class LifeLoop:
    """
    The ONLY place A7DO experiences the world.
    World dependencies are injected (no nested loaders).
    """

    def __init__(self, world_time=None, world_state=None, stage_schedule=None):
        # Core
        self.identity = SelfIdentity()
        self.clock = SystemClock()      # real-world elapsed time
        self.pulse = Pulse()

        # Internal experiential time
        self.internal_time = 0

        # Injected world
        self.world_time = world_time or WorldTime()
        self.world = world_state or WorldState()

        # Physics / metabolism
        self.physics = PhysicsGate()
        self.energy = EnergyBudget(capacity=10.0)
        self.recovery = RecoverySystem(self.energy)
        self.overload = OverloadMonitor()
        self.regulator = HomeostasisRegulator(self.energy, self.overload)

        # Safety
        self.shutdown = ShutdownAuthority()

        # Body
        self.reflex = ReflexArc()
        self.motor = GrossMotor()
        self.proprio = BodyOrientationSense()

        # Memory
        self.memory = EpisodicMemory()
        self.salience = {}
        self.attention = AttentionSystem(self.memory, focus_size=5)
        self.energy_learner = ActionEnergyLearner()
        self.predictor = Predictor(self.world, self.memory)
        self.council = Council(
            self.world,
            self.memory,
            self.predictor,
            self.attention,
        )
        self.snapshot = IntrospectionSnapshot(
            self.world,
            self.memory,
            self.attention,
            self.predictor,
            self.council,
        )

        # Lifecycle / development
        self.lifecycle = LifecycleManager()
        # Start in womb (advance from seed)
        self.lifecycle.advance()

        self._development_by_stage = {
            LifeStage.WOMB: EmbryonicStage(),
            LifeStage.BIRTH: InfantStage(),
            LifeStage.INFANT: InfantStage(),
            LifeStage.TODDLER: ToddlerStage(),
            LifeStage.CHILD: ChildStage(),
            LifeStage.ADOLESCENT: AdolescentStage(),
            LifeStage.ADULT: AdultStage(),
        }

        self._stage_schedule = stage_schedule or [
            (0, LifeStage.ADULT),
        ]

    def record_memory(self, event: dict, salience: float = 0.0):
        self.physics.allow(0.1, self.energy.level())
        self.energy.spend(0.1)
        record = self.memory.record(event, salience=salience)
        memory_id = f"{event.get('type', 'event')}_{record['time']}"
        self.salience[memory_id] = salience
        return record

    def _current_development(self):
        return self._development_by_stage.get(self.lifecycle.stage)

    def _allowed_systems(self):
        stage = self._current_development()
        if stage is None:
            return {}
        return stage.allowed_systems()

    def _motor_allowed(self, allowed):
        motor = allowed.get("motor")
        if motor in (False, None):
            return False
        if motor == "reflex_only":
            return False
        if motor == "gross_only":
            return True
        if motor == "all":
            return True
        if isinstance(motor, list):
            return "gross" in motor or "coordinated" in motor
        return bool(motor)

    def _memory_allowed(self, allowed):
        memory = allowed.get("memory")
        if memory in (False, None):
            return False
        return True

    def _update_lifecycle(self):
        # Determine desired stage by internal time
        desired_stage = self.lifecycle.stage
        for t, stage in self._stage_schedule:
            if self.internal_time >= t:
                desired_stage = stage

        while self.lifecycle.stage != desired_stage:
            self.lifecycle.advance()

    # --------------------------------------------------
    # LIFE TICK — INTENTIONAL EXPERIENCE
    # --------------------------------------------------
    def tick(self):
        if not self.pulse.is_alive():
            return

        try:
            # ---- INTENTIONAL TIME BOUNDARY ----
            self.internal_time += 1
            real_time = self.clock.now()

            self._update_lifecycle()
            allowed = self._allowed_systems()

            # World evolves independently
            self.world_time.tick(delta=1.0)

            regulation = self.regulator.regulate()
            if regulation in {"rest", "reduce_activity"}:
                self.recovery.rest(1.0)
                self.overload.recover(0.15)

            current_weather = (
                "storm"
                if self.internal_time % 7 == 0
                else "clear"
            )
            current_light = "day" if self.internal_time % 10 < 6 else "night"

            # A7DO samples world here
            action = None
            self.world.update(
                energy=self.energy.level(),
                strain=self.overload.strain,
                last_action=action,
                last_sensation={
                    "weather": current_weather,
                    "light": current_light,
                    "regulation": regulation,
                },
                time=self.world_time.t,
            )

            # Base metabolism
            self.physics.allow(1.0, self.energy.level())
            self.energy.spend(1.0)

            # Reflex / withdrawal
            if self.overload.strain > 0.5:
                try:
                    if allowed.get("motor") not in (False, None):
                        self.physics.allow(0.5, self.energy.level())
                        self.energy.spend(0.5)
                        self.reflex.respond({"pain": self.overload.strain})
                except Exception:
                    pass

                if self._motor_allowed(allowed):
                    try:
                        self.physics.allow(0.7, self.energy.level())
                        self.energy.spend(0.7)
                        action = self.motor.execute("withdraw_limb")
                    except Exception:
                        action = None
                if action is not None:
                    self.world.update(last_action=action)

                body_state = None
                if action is not None:
                    try:
                        body_state = self.proprio.sense({"action": action})
                    except Exception:
                        body_state = None

                # Record experienced world
                if self._memory_allowed(allowed):
                    self.record_memory(
                        {
                            "type": "pain_withdrawal",
                            "strain": self.overload.strain,
                            "body_state": body_state,
                            "world": self.world.snapshot(),
                            "time_internal": self.internal_time,
                            "time_real": real_time,
                            "time_world": self.world_time.t,
                        },
                        salience=min(1.0, 0.5 + self.overload.strain),
                    )

            self.energy_learner.learn(self.attention.focus())

            # Load accumulates after action
            self.overload.apply_load(0.1)

            self.world.update(
                energy=self.energy.level(),
                strain=self.overload.strain,
                last_action=action,
                time=self.world_time.t,
            )

            # Memory decay
            if self._memory_allowed(allowed):
                self.memory.tick()

        except Exception as e:
            self.shutdown.trigger(str(e))
            self.pulse.set_state("dead")

    def run(self):
        while self.pulse.is_alive():
            self.tick()
            time.sleep(0.1)
