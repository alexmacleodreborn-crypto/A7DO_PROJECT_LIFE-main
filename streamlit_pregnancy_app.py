"""
A7DO — Pregnancy & Fetal Development (Streamlit UI)
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import math
from pathlib import Path
import streamlit as st


@dataclass
class PregnancySnapshot:
    gestational_weeks: float
    biological_days: int

    @property
    def trimester(self) -> int:
        if self.gestational_weeks < 13:
            return 1
        if self.gestational_weeks < 27:
            return 2
        return 3


def init_state() -> None:
    if "pregnancy" not in st.session_state:
        st.session_state.pregnancy = PregnancySnapshot(
            gestational_weeks=7.43,
            biological_days=52,
        )
    if "pregnancy_running" not in st.session_state:
        st.session_state.pregnancy_running = False
    if "life_loop" not in st.session_state:
        st.session_state.life_loop = None
    if "world_env" not in st.session_state:
        st.session_state.world_env = None


ROOT = Path(__file__).resolve().parent


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@st.cache_resource
def get_physics_gate():
    physics_mod = load_module(
        "physics_gate",
        "01_PHYSICS_SANITY_SANDYS_LAW/gating.py",
    )
    return physics_mod.PhysicsGate()


def advance_day(days: int = 1) -> None:
    snapshot = st.session_state.pregnancy
    st.session_state.pregnancy = PregnancySnapshot(
        gestational_weeks=snapshot.gestational_weeks + (days / 7.0),
        biological_days=snapshot.biological_days + days,
    )


def build_life_support_table() -> list[dict[str, str]]:
    return [
        {"System": "Heartbeat", "State": "FUNCTIONAL_AUTONOMIC"},
        {"System": "Umbilical Cord", "State": "PRIMARY_LIFE_SUPPORT"},
        {"System": "Energy Source", "State": "EXTERNAL"},
    ]


def build_development_timeline(
    gestational_weeks: float,
    postnatal_days: int,
    birth_weeks: int,
) -> list[dict[str, str]]:
    prenatal_events = [
        (4, "Neural tube closes"),
        (6, "Heart begins coordinated beating"),
        (8, "Limb buds form"),
        (12, "Reflexes appear"),
        (16, "Movement becomes strong"),
        (24, "Sensory pathways online"),
        (28, "Sleep/wake cycles stabilize"),
        (32, "Autonomic regulation matures"),
        (36, "Systems prepare for birth"),
        (birth_weeks, "Birth event"),
    ]
    postnatal_events = [
        (0, "External world activation"),
        (1, "Breathing + circulation adjust"),
        (2, "ECG monitoring online"),
        (7, "Feeding rhythm stabilizes"),
        (14, "Thermal regulation steadies"),
        (30, "Early motor control strengthens"),
    ]
    timeline: list[dict[str, str]] = []
    for week, label in prenatal_events:
        status = "UPCOMING"
        if gestational_weeks >= week:
            status = "ONLINE"
        if week == birth_weeks and gestational_weeks >= birth_weeks:
            status = "BIRTH_EVENT"
        timeline.append(
            {
                "Phase": "Prenatal",
                "Time": f"Week {week}",
                "Event": label,
                "Status": status,
            }
        )
    for day, label in postnatal_events:
        status = "LOCKED"
        if gestational_weeks >= birth_weeks:
            status = "UPCOMING"
            if postnatal_days >= day:
                status = "ONLINE"
        timeline.append(
            {
                "Phase": "Postnatal",
                "Time": f"Day {day}",
                "Event": label,
                "Status": status,
            }
        )
    return timeline


def build_ecg_series(postnatal_days: int, points: int = 140) -> list[float]:
    base = 110 + min(postnatal_days, 30) * 0.2
    series = []
    for idx in range(points):
        drift = 6 * math.sin((idx + postnatal_days) / 6.5)
        flutter = 3 * math.sin((idx + postnatal_days) / 2.9)
        heartbeat = base + drift + flutter
        series.append(max(85, min(160, heartbeat)))
    return series


def logistic(x: float, mid: float, k: float) -> float:
    return 1.0 / (1.0 + math.exp(-k * (x - mid)))


def build_growth_metrics(gestational_weeks: float) -> dict[str, float | str]:
    # Physics-gated growth using Sandy's Law (energy conservation).
    physics = get_physics_gate()

    # Simplified biological curves (logistic) for fetal growth.
    weight_kg = 0.01 + 3.3 * logistic(gestational_weeks, mid=30, k=0.33)
    length_cm = 3.0 + 47.0 * logistic(gestational_weeks, mid=28, k=0.28)
    head_cm = 2.5 + 32.0 * logistic(gestational_weeks, mid=26, k=0.30)

    # Energy model (unitless) from A7DO math: E(t+1) = E(t) - W - H + I
    intake = 8.0 + gestational_weeks * 0.25
    work = 1.8 + gestational_weeks * 0.08
    heat = 1.2 + gestational_weeks * 0.05
    energy_next = max(0.0, intake - work - heat)
    growth_cost = 2.5 + gestational_weeks * 0.12

    growth_allowed = True
    try:
        physics.allow(growth_cost, energy_next)
    except Exception:
        growth_allowed = False

    return {
        "weight_kg": round(weight_kg, 3),
        "length_cm": round(length_cm, 1),
        "head_circumference_cm": round(head_cm, 1),
        "energy_intake": round(intake, 2),
        "energy_work": round(work, 2),
        "energy_heat": round(heat, 2),
        "energy_available": round(energy_next, 2),
        "growth_cost": round(growth_cost, 2),
        "growth_allowed": "YES" if growth_allowed else "NO",
    }


def build_postnatal_growth(postnatal_days: int) -> dict[str, float | int]:
    return {
        "age_days": postnatal_days,
        "brain": round(1.0 + postnatal_days * 0.003, 3),
        "spine": round(1.1 + postnatal_days * 0.002, 3),
        "nervous": round(1.0 + postnatal_days * 0.003, 3),
        "limb_strength": round(0.45 + postnatal_days * 0.0015, 3),
    }


def build_neonatal_physiology(postnatal_days: int) -> dict[str, float | bool]:
    energy = 20 + min(postnatal_days, 30) * 0.08
    fatigue = max(0.15, 0.65 - postnatal_days * 0.01)
    return {
        "energy": round(energy, 2),
        "fatigue": round(fatigue, 3),
        "awake": postnatal_days > 1,
    }


def build_external_regulation(postnatal_days: int) -> dict[str, float]:
    return {
        "heartbeat_bpm": round(70 + min(postnatal_days, 30) * 0.12, 1),
        "warmth": round(0.7 + min(postnatal_days, 14) * 0.01, 2),
        "feeding_rate": round(0.18 + min(postnatal_days, 20) * 0.004, 3),
        "calming": round(0.28 + min(postnatal_days, 20) * 0.005, 3),
    }


def build_prenatal_body_table(trimester: int) -> list[dict[str, str]]:
    if trimester == 1:
        return [
            {
                "Body Node": "limbs/arms/hand",
                "State": "FORMING",
                "Notes": "Hand plate",
            },
            {
                "Body Node": "limbs/legs/foot",
                "State": "FORMING",
                "Notes": "Foot plate",
            },
            {
                "Body Node": "morphology/muscles",
                "State": "REFLEX_CAPABLE",
                "Notes": "Spinal reflex activity",
            },
        ]
    if trimester == 2:
        return [
            {
                "Body Node": "limbs/arms",
                "State": "STRONG_REFLEX",
                "Notes": "Coordinated flexion",
            },
            {
                "Body Node": "morphology/muscles",
                "State": "STRONG_REFLEX",
                "Notes": "Muscle strength increasing",
            },
            {
                "Body Node": "morphology/posture",
                "State": "AUTONOMIC_TONE",
                "Notes": "Postural stability",
            },
        ]
    return [
        {
            "Body Node": "limbs/legs",
            "State": "READY_POSTNATAL",
            "Notes": "Strong kicking",
        },
        {
            "Body Node": "motor_control/coordination",
            "State": "READY_POSTNATAL",
            "Notes": "Coordinated movement",
        },
        {
            "Body Node": "morphology/posture",
            "State": "READY_POSTNATAL",
            "Notes": "Stable posture",
        },
    ]


def build_neural_table(trimester: int) -> list[dict[str, str]]:
    if trimester == 1:
        return [
            {"System": "Nervous System", "State": "PRESENT_LOCKED"},
            {"System": "Sleep / Wake", "State": "ABSENT"},
            {"System": "Reflexes", "State": "FORMING"},
        ]
    if trimester == 2:
        return [
            {"System": "Nervous System", "State": "FUNCTIONAL_AUTONOMIC"},
            {"System": "Sleep / Wake", "State": "FUNCTIONAL_AUTONOMIC"},
            {"System": "Reflexes", "State": "FUNCTIONAL_AUTONOMIC"},
        ]
    return [
        {"System": "Nervous System", "State": "READY_POSTNATAL"},
        {"System": "Sleep / Wake", "State": "READY_POSTNATAL"},
        {"System": "Reflexes", "State": "READY_POSTNATAL"},
    ]


def build_cognitive_table(trimester: int) -> list[dict[str, str]]:
    if trimester == 3:
        return [
            {"System": "Motivation Expression", "State": "ENABLED"},
            {"System": "Attention", "State": "ENABLED"},
            {"System": "Memory", "State": "ENABLED"},
            {"System": "LifeLoop Allowed", "State": "YES"},
        ]
    return [
        {"System": "Motivation Expression", "State": "LOCKED"},
        {"System": "Attention", "State": "LOCKED"},
        {"System": "Memory", "State": "LOCKED"},
        {"System": "LifeLoop Allowed", "State": "NO"},
    ]


st.set_page_config(
    page_title="A7DO — Pregnancy & Fetal Development",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: #0d1117;
        color: #e6edf3;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px;
    }
    .section-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_state()

snapshot = st.session_state.pregnancy
birth_weeks = 40
postnatal_days = max(0, snapshot.biological_days - (birth_weeks * 7))
is_postnatal = snapshot.gestational_weeks >= birth_weeks
auto_step_days = max(1, int(round(1 + (snapshot.gestational_weeks / birth_weeks) * 2)))

if is_postnatal and st.session_state.life_loop is None:
    world_time_mod = load_module("world_time", "09_WORLD_MODEL/time.py")
    world_state_mod = load_module("world_state", "09_WORLD_MODEL/world_state.py")
    world_env_mod = load_module("world_env", "09_WORLD_MODEL/environments/world.py")
    life_loop_mod = load_module("life_loop", "00_CORE_EXISTENCE/bootstrap/life_loop.py")

    WorldTime = world_time_mod.WorldTime
    WorldState = world_state_mod.WorldState
    World = world_env_mod.World
    LifeLoop = life_loop_mod.LifeLoop

    world_time = WorldTime()
    world_state = WorldState(default_place="house")
    st.session_state.world_env = World.create(world_state=world_state)
    st.session_state.life_loop = LifeLoop(world_time, world_state)

st.title("🧬 A7DO — Pregnancy & Fetal Development")

stage_label = "Postnatal" if is_postnatal else f"Prenatal (T{snapshot.trimester})"
st.markdown(
    "<div class='section-card'>"
    "<strong>Stage</strong><br>"
    f"{stage_label} — Week {snapshot.gestational_weeks:.2f} / Day {snapshot.biological_days}"
    "</div>",
    unsafe_allow_html=True,
)

left, middle, right = st.columns([1.2, 2, 1.2])
with left:
    st.subheader("Pregnancy Control")
    if st.button("▶️ Start Pregnancy", width="stretch"):
        st.session_state.pregnancy_running = True
    if st.button("⏸ Pause", width="stretch"):
        st.session_state.pregnancy_running = False

with middle:
    st.markdown("&nbsp;")
    if st.button("⏩ Advance One Day"):
        advance_day(1)

with right:
    st.markdown(
        "<div class='section-card'>"
        "<strong>Notes</strong><br>"
        f"Auto-step rate: {auto_step_days} day(s) per cycle."
        "</div>",
        unsafe_allow_html=True,
    )

if st.session_state.pregnancy_running:
    advance_day(auto_step_days)

metrics = st.columns(3)
metrics[0].metric("Gestational Weeks", f"{snapshot.gestational_weeks:.2f}")
metrics[1].metric("Biological Days", f"{snapshot.biological_days}")
metrics[2].metric("Phase", "Postnatal" if is_postnatal else "Prenatal")

st.subheader("ðŸ§­ Linear Development Timeline")
st.dataframe(
    build_development_timeline(
        snapshot.gestational_weeks,
        postnatal_days,
        birth_weeks,
    ),
    width="stretch",
)

st.divider()
st.header("Prenatal Phase")

st.subheader("❤️ Life-Support Systems")
st.dataframe(build_life_support_table(), width="stretch")

st.subheader("🦴 Prenatal Body Formation")
st.dataframe(
    build_prenatal_body_table(snapshot.trimester),
    width="stretch",
)

st.subheader("📏 Biology Growth (Physics-Gated)")
st.json(build_growth_metrics(snapshot.gestational_weeks))

st.subheader("🧠 Autonomic & Neural Status")
st.dataframe(build_neural_table(snapshot.trimester), width="stretch")

st.subheader("📈 Motivation Capacity (Upper Bound Only)")
motivation_progress = min(snapshot.gestational_weeks / 40, 1.0)
st.progress(motivation_progress)
st.caption(
    f"Motivation capacity = {motivation_progress:.2f} "
    "(expression locked until birth)."
)

st.subheader("🔐 Cognitive Availability")
st.dataframe(
    build_cognitive_table(snapshot.trimester),
    width="stretch",
)

st.subheader("🎂 Birth Status")
if is_postnatal:
    st.success("Birth threshold reached — LifeLoop may initialize.")
    st.markdown(
        "<div class='section-card'>"
        "<strong>Transition</strong><br>"
        "Maternal field ➜ placental support ➜ birth ➜ neonatal regulation ➜ "
        "independent life."
        "</div>",
        unsafe_allow_html=True,
    )
else:
    remaining = max(0, int(birth_weeks - snapshot.gestational_weeks))
    st.info(
        f"Estimated weeks until birth: {remaining}"
    )

st.divider()
st.header("Postnatal Phase")
st.subheader("🌍 External World Activation")
if is_postnatal:
    st.markdown(
        "<div class='section-card'>"
        "<strong>Neonatal Life Online</strong><br>"
        "External sensors, caregiver regulation, and ECG monitoring now active."
        "</div>",
        unsafe_allow_html=True,
    )
    st.subheader("❤️ ECG (Heart Rate)")
    st.line_chart(build_ecg_series(postnatal_days))
    neonatal_left, neonatal_right = st.columns(2)
    with neonatal_left:
        st.subheader("🧠 Postnatal Growth")
        st.json(build_postnatal_growth(postnatal_days))
        st.subheader("🤱 External Regulation (MotherBot)")
        st.json(build_external_regulation(postnatal_days))
    with neonatal_right:
        st.subheader("🩺 Physiology")
        st.json(build_neonatal_physiology(postnatal_days))
    st.divider()
    st.header("LifeLoop (Active After Birth)")
    life = st.session_state.life_loop
    if life is not None:
        control_left, control_right = st.columns([1, 2])
        with control_left:
            if st.button("Tick LifeLoop (1)", width="stretch"):
                life.tick()
            run_n = st.number_input(
                "Run N LifeLoop ticks",
                min_value=1,
                max_value=100,
                value=5,
                step=1,
            )
            if st.button("Run LifeLoop N", width="stretch"):
                for _ in range(int(run_n)):
                    life.tick()
        with control_right:
            st.json({
                "energy": life.energy.level(),
                "strain": life.overload.strain,
                "last_action": getattr(life.motor, "last_action", None),
                "lifecycle_stage": str(life.lifecycle.stage),
                "time_internal": life.internal_time,
                "time_real": life.clock.now(),
                "time_world": life.world_time.t,
            })
            st.subheader("Recent Memory")
            st.json(life.memory.recent(5))
else:
    st.info(
        "External world interfaces remain locked. "
        "ECG monitoring and neonatal regulation activate at birth."
    )
    st.caption("LifeLoop locked until birth.")

if is_postnatal:
    st.caption(
        "Postnatal phase active. External regulation and neonatal systems "
        "are now online."
    )
else:
    st.caption(
        "Prenatal phase structure and autonomic systems only. "
        "No cognition, learning, selfness, attention, or memory is active."
    )
