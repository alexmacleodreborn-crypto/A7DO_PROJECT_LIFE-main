"""
A7DO — Pregnancy & Fetal Development (Streamlit UI)
"""

from __future__ import annotations

from dataclasses import dataclass
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
if snapshot.trimester == 3:
    st.success("Birth threshold reached — LifeLoop may initialize.")
else:
    remaining = max(0, int(40 - snapshot.gestational_weeks))
    st.info(
        f"Estimated weeks until birth: {remaining}"
    )

st.caption(
    "Prenatal phase structure and autonomic systems only. "
    "No cognition, learning, selfness, attention, or memory is active."
)
