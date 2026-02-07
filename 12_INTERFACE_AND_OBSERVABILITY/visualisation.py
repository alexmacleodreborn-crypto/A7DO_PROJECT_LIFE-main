import importlib.util
import time
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


english_mod = load_module("english_learning", "english_learning.py")
EnglishLearning = english_mod.EnglishLearning


class WebDashboard:
    """
    Read-only Streamlit dashboard.
    Displays live introspection snapshots, evidence, and calibrated confidence.
    """

    def __init__(
        self,
        snapshot,
        ledger=None,
        calibrator=None,
        refresh_seconds: float = 1.0,
        life_loop=None,
        english_learning: bool = True,
    ):
        self.snapshot = snapshot
        self.ledger = ledger
        self.calibrator = calibrator
        self.refresh_seconds = refresh_seconds
        self.life_loop = life_loop
        self.english_learning = english_learning

    def run(self):
        st.set_page_config(
            page_title="A7DO — Live Introspection Dashboard",
            layout="wide",
        )
        st.title("🧠 A7DO — Live Introspection Dashboard")

        placeholder = st.empty()

        english_learning = None
        if self.english_learning:
            english_learning = EnglishLearning(st.session_state)

        while True:
            view = self.snapshot.capture()

            with placeholder.container():
                col1, col2 = st.columns(2)

                # ==================================================
                # LEFT COLUMN
                # ==================================================
                with col1:
                    # -----------------------------
                    # World
                    # -----------------------------
                    st.subheader("🌍 World State")
                    st.json(view.get("world", {}))

                    # -----------------------------
                    # Prediction (raw + calibrated)
                    # -----------------------------
                    st.subheader("🔮 Prediction")
                    prediction = view.get("prediction", {})

                    raw_conf = prediction.get("confidence")
                    calibrated_conf = None

                    if (
                        raw_conf is not None
                        and self.calibrator is not None
                        and self.ledger is not None
                    ):
                        calibrated_conf = (
                            self.calibrator.calibrated_confidence(raw_conf)
                        )

                    pred_display = dict(prediction)
                    if calibrated_conf is not None:
                        pred_display["calibrated_confidence"] = calibrated_conf

                    st.json(pred_display)

                    # -----------------------------
                    # Evidence + Plots
                    # -----------------------------
                    if self.ledger is not None:
                        st.subheader("📊 Evidence (Recent)")
                        events = self.ledger.recent(50)

                        if not events:
                            st.write("No evidence recorded yet.")
                        else:
                            # -----------------------------
                            # Table
                            # -----------------------------
                            table = [
                                {
                                    "time": e["time"],
                                    "expected": e["prediction"].get(
                                        "expected_strain"
                                    ),
                                    "observed": e["outcome"].get("strain"),
                                    "error": e["error"],
                                    "confidence": e["confidence"],
                                }
                                for e in events
                            ]
                            st.dataframe(
                                table,
                                use_container_width=True,
                            )

                            # -----------------------------
                            # Extract series
                            # -----------------------------
                            errors = [
                                e["error"]
                                for e in events
                                if e.get("error") is not None
                            ]
                            confidences = [
                                e["confidence"]
                                for e in events
                                if e.get("error") is not None
                            ]

                            # -----------------------------
                            # Error vs Time
                            # -----------------------------
                            if errors:
                                st.subheader("📈 Error vs Time")
                                st.line_chart(
                                    {"error": errors}
                                )

                            # -----------------------------
                            # Confidence vs Error
                            # -----------------------------
                            if errors and confidences:
                                st.subheader("🎯 Confidence vs Error")
                                st.scatter_chart(
                                    {
                                        "confidence": confidences,
                                        "error": errors,
                                    }
                                )

                # ==================================================
                # RIGHT COLUMN
                # ==================================================
                with col2:
                    st.subheader("🧠 Attention")
                    st.json(view.get("attention", []))

                    st.subheader("🏛️ Council")
                    st.json(view.get("council", {}))

                    if english_learning is not None:
                        st.subheader("🧠 English Language Learning")
                        metrics = english_learning.metrics()

                        st.write(
                            f"**Energy Cost / Cycle:** {english_learning.energy_cost:.2f}"
                        )
                        st.write(
                            f"**Learning Status:** {metrics['last_status']}"
                        )
                        st.write(f"**Age (cycles):** {metrics['age']}")
                        st.write(f"**Portal Score K:** {metrics['K']:.2f}")
                        st.write(
                            f"**Language Understanding:** {metrics['understanding']:.2f}"
                        )
                        st.write(f"**Vocabulary Size:** {metrics['vocab_size']}")
                        st.write(
                            f"**Sentence Patterns Learned:** {metrics['pattern_count']}"
                        )
                        st.write(f"**Intent:** {metrics['intent']:.2f}")

                        def energy_gate() -> str:
                            if self.life_loop is None:
                                return "blocked: no life loop"
                            if not self.life_loop.pulse.is_alive():
                                return "blocked: pulse inactive"
                            try:
                                self.life_loop.physics.allow(
                                    english_learning.energy_cost,
                                    self.life_loop.energy.level(),
                                )
                            except Exception:
                                return "blocked: insufficient energy"
                            self.life_loop.energy.spend(
                                english_learning.energy_cost
                            )
                            return "ok"

                        if st.button(
                            "Advance Language Cycle",
                            key="english_advance_cycle",
                        ):
                            english_learning.advance(energy_gate)

                        st.info(
                            "📘 Learning English continuously: words, sentences, and structure."
                        )

                        if english_learning.is_invited():
                            st.success("📨 A7DO is ready to speak with you")

                            with st.form(
                                "english_chat_form",
                                clear_on_submit=True,
                            ):
                                user_msg = st.text_input(
                                    "You:",
                                    key="english_chat_input",
                                )
                                send = st.form_submit_button("Send")

                            if send and user_msg:
                                english_learning.add_user_message(user_msg)

                            for speaker, message in english_learning.chat_history():
                                st.markdown(
                                    f"**{speaker}:** {message}"
                                )

                        st.subheader("🟢 First Expression")
                        if (
                            english_learning.expression_ready()
                            and english_learning.first_output() is None
                        ):
                            st.warning(
                                "A7DO is ready for a first expression."
                            )
                            out = st.text_area(
                                "A7DO First Expression",
                                key="english_first_expression",
                            )

                            if out:
                                english_learning.set_first_output(out)
                        elif english_learning.first_output():
                            st.success("First expression captured.")
                            st.text_area(
                                "A7DO Output",
                                english_learning.first_output(),
                                disabled=True,
                                key="english_output",
                            )

                # -----------------------------
                # Memory (full width)
                # -----------------------------
                st.subheader("📚 Recent Memory")
                st.json(view.get("memory", []))

            time.sleep(self.refresh_seconds)
