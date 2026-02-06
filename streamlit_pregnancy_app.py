"""
A7DO — Pregnancy & Fetal Development (Streamlit UI)
"""

from __future__ import annotations

from dataclasses import dataclass
import math
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


def build_ecg_series(postnatal_days: int, points: int = 140) -> list[float]:
    base = 110 + min(postnatal_days, 30) * 0.2
    series = []
    for idx in range(points):
        drift = 6 * math.sin((idx + postnatal_days) / 6.5)
        flutter = 3 * math.sin((idx + postnatal_days) / 2.9)
        heartbeat = base + drift + flutter
        series.append(max(85, min(160, heartbeat)))
    return series


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

st.title("🧬 A7DO — Pregnancy & Fetal Development")

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
        "Manual progression keeps developmental boundaries authoritative."
        "</div>",
        unsafe_allow_html=True,
    )

if st.session_state.pregnancy_running:
    advance_day(1)

metrics = st.columns(3)
metrics[0].metric("Gestational Weeks", f"{snapshot.gestational_weeks:.2f}")
metrics[1].metric("Biological Days", f"{snapshot.biological_days}")
metrics[2].metric("Trimester", f"{snapshot.trimester}")

st.subheader("❤️ Life-Support Systems")
st.dataframe(build_life_support_table(), width="stretch")

st.subheader("🦴 Prenatal Body Formation")
st.dataframe(
    build_prenatal_body_table(snapshot.trimester),
    width="stretch",
)

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
if snapshot.gestational_weeks >= birth_weeks:
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

st.subheader("🌍 External World Activation")
if snapshot.gestational_weeks >= birth_weeks:
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
else:
    st.info(
        "External world interfaces remain locked. "
        "ECG monitoring and neonatal regulation activate at birth."
    )

st.caption(
    "Prenatal phase structure and autonomic systems only. "
    "No cognition, learning, selfness, attention, or memory is active."
)
