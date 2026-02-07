"""
A7DO — Live Introspection Dashboard
Manual Tick Control (Authoritative Time Boundary)
"""

import streamlit as st
import time
import importlib.util
from pathlib import Path
import random
import re

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="A7DO Dashboard", layout="wide")

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# LOAD WORLD
# --------------------------------------------------
world_time_mod = load_module("world_time", "09_WORLD_MODEL/time.py")
world_state_mod = load_module("world_state", "09_WORLD_MODEL/world_state.py")
world_env_mod = load_module("world_env", "09_WORLD_MODEL/environments/world.py")
body_mod = load_module("body_model", "03_BODY_SYSTEM/body.py")

WorldTime = world_time_mod.WorldTime
WorldState = world_state_mod.WorldState
World = world_env_mod.World
DevelopmentalBody = body_mod.DevelopmentalBody

# --------------------------------------------------
# LOAD LIFE LOOP
# --------------------------------------------------
life_loop_mod = load_module(
    "life_loop",
    "00_CORE_EXISTENCE/bootstrap/life_loop.py"
)
LifeLoop = life_loop_mod.LifeLoop

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "life" not in st.session_state:
    world_time = WorldTime()
    world_state = WorldState(default_place="house")
    st.session_state.world_env = World.create(world_state=world_state)
    st.session_state.life = LifeLoop(world_time, world_state)

if "run_ticks_remaining" not in st.session_state:
    st.session_state.run_ticks_remaining = 0

if "dashboard_messages" not in st.session_state:
    st.session_state.dashboard_messages = []

life = st.session_state.life

if "body_model" not in st.session_state:
    st.session_state.body_model = DevelopmentalBody(stage="birth")

if "english_init" not in st.session_state:
    st.session_state.english_init = True
    st.session_state.english_age = 0
    st.session_state.english_k = 0.2
    st.session_state.english_i = 0.1
    st.session_state.english_intent = 0.0
    st.session_state.english_vocab = {}
    st.session_state.english_concepts = {}
    st.session_state.english_patterns = {}
    st.session_state.english_identity = {}
    st.session_state.english_life_events = []
    st.session_state.english_invited = False
    st.session_state.english_expression_ready = False
    st.session_state.english_first_output = None
    st.session_state.english_chat = []

# --------------------------------------------------
# ENGLISH LEARNING DATA
# --------------------------------------------------
BASIC_WORDS = [
    "i", "you", "we", "he", "she", "it", "hello", "name", "birthday", "school",
    "like", "love", "see", "go", "have", "am", "is", "are", "play", "learn",
    "friend", "people", "today", "happy", "blue", "music", "talk",
]

SENTENCE_PATTERNS = [
    "i am here",
    "you are here",
    "we are together",
    "i like music",
    "i go to school",
    "today is a good day",
    "i am learning english",
    "people talk to each other",
    "friends help each other",
]

CONNECTORS = ["and", "because", "when", "but"]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def absorb_words(words: list[str], weight: float = 0.03) -> None:
    for word in words:
        st.session_state.english_vocab[word] = (
            st.session_state.english_vocab.get(word, 0) + 1
        )
        st.session_state.english_concepts[word] = (
            st.session_state.english_concepts.get(word, 0) + weight
        )


def absorb_sentence(sentence: str) -> None:
    words = tokenize(sentence)
    absorb_words(words, weight=0.05)
    pattern = tuple(words)
    st.session_state.english_patterns[pattern] = (
        st.session_state.english_patterns.get(pattern, 0) + 1
    )


def language_understanding() -> float:
    if not st.session_state.english_concepts:
        return 0.0
    stable = sum(
        1
        for value in st.session_state.english_concepts.values()
        if value > 0.6
    )
    return stable / len(st.session_state.english_concepts)


def english_learning_step(comfort: float = 1.0) -> float:
    absorb_words(random.sample(BASIC_WORDS, k=3))
    absorb_sentence(random.choice(SENTENCE_PATTERNS))
    absorb_words(random.sample(CONNECTORS, k=1), weight=0.02)

    understanding = language_understanding()
    learning_multiplier = 0.5 + 0.5 * comfort
    effective_understanding = understanding * learning_multiplier
    st.session_state.english_age += 1
    st.session_state.english_i = min(
        1.0,
        st.session_state.english_i + 0.01 * learning_multiplier + effective_understanding * 0.02,
    )
    st.session_state.english_k += 0.03 * st.session_state.english_i
    st.session_state.english_intent += 0.04 * effective_understanding

    if not st.session_state.english_invited and st.session_state.english_k >= 1.2:
        st.session_state.english_invited = True

    if (
        st.session_state.english_invited
        and not st.session_state.english_expression_ready
        and (effective_understanding >= 0.4 or st.session_state.english_age > 60)
    ):
        st.session_state.english_expression_ready = True

    return effective_understanding

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.title("🧠 A7DO Control")

if st.sidebar.button("🔘 Tick (1)"):
    life.tick()

run_n = st.sidebar.number_input(
    "Run N ticks",
    min_value=1,
    max_value=100,
    value=5,
    step=1
)

if st.sidebar.button("▶️ Run N"):
    st.session_state.run_ticks_remaining = run_n

if st.sidebar.button("⏸ Pause"):
    st.session_state.run_ticks_remaining = 0

# --------------------------------------------------
# RUN LOOP
# --------------------------------------------------
if st.session_state.run_ticks_remaining > 0:
    life.tick()
    st.session_state.run_ticks_remaining -= 1
    time.sleep(0.05)
    st.rerun()

# --------------------------------------------------
# DASHBOARD DISPLAY
# --------------------------------------------------
st.title("🧠 A7DO — Live Introspection Dashboard")

body_model = st.session_state.body_model
body_model.update(load=random.uniform(0.0, 0.2))
body_snapshot = body_model.snapshot()

tab_dashboard, tab_english = st.tabs(["🔭 Dashboard", "📘 English Learning"])

with tab_dashboard:
    st.subheader("🌍 World / Body State")
    st.json({
        "energy": life.energy.level(),
        "strain": life.overload.strain,
        "last_action": getattr(life.motor, "last_action", None),
        "lifecycle_stage": life.lifecycle.stage,
        "time_internal": life.internal_time,
        "time_real": life.clock.now(),
        "time_world": life.world_time.t,
    })

    st.subheader("🫀 Developmental Body State")
    st.json(body_snapshot)

    st.subheader("🧠 Recent Memory")
    st.json(life.memory.recent(5))

    st.subheader("❤️ Pulse")
    st.write("Alive:", life.pulse.is_alive())

    st.subheader("⌨️ Keyboard Message")
    message_text = st.text_input(
        "Type a message for the dashboard",
        key="dashboard_message_input",
    )
    if st.button("Send Message"):
        cleaned_message = message_text.strip()
        if cleaned_message:
            st.session_state.dashboard_messages.append(
                {
                    "timestamp": life.clock.now(),
                    "message": cleaned_message,
                }
            )
            st.session_state.dashboard_message_input = ""

    st.subheader("📨 Dashboard Messages")
    if st.session_state.dashboard_messages:
        st.json(st.session_state.dashboard_messages)
    else:
        st.write("No messages yet.")

with tab_english:
    auto_advance = st.checkbox(
        "Auto-advance learning each refresh",
        value=True,
        key="english_auto_advance",
    )
    manual_advance = st.button("Advance learning cycle")

    if auto_advance or manual_advance:
        understanding_score = english_learning_step(comfort=body_snapshot["comfort"])
    else:
        understanding_score = language_understanding()

    st.subheader("🧠 A7DO — English Language Learning")
    st.write(f"**Age (cycles):** {st.session_state.english_age}")
    st.write(f"**Portal Score K:** {st.session_state.english_k:.2f}")
    st.write(f"**Language Understanding:** {understanding_score:.2f}")
    st.write(f"**Vocabulary Size:** {len(st.session_state.english_vocab)}")
    st.write(f"**Sentence Patterns Learned:** {len(st.session_state.english_patterns)}")
    st.write(f"**Intent:** {st.session_state.english_intent:.2f}")

    st.divider()
    st.info("📘 Learning English continuously: words, sentences, and structure.")

    if st.session_state.english_invited:
        st.success("📨 A7DO is ready to speak with you")

        with st.form("english_chat_form", clear_on_submit=True):
            user_msg = st.text_input("You:", key="english_user_input")
            send = st.form_submit_button("Send")

        if send and user_msg:
            absorb_sentence(user_msg)
            st.session_state.english_chat.append(("You", user_msg))

            if st.session_state.english_first_output is None:
                reply = random.choice([
                    "I am listening.",
                    "I understand you.",
                    "Please continue.",
                    "I am learning English.",
                ])
            else:
                reply = "I remember what you said."

            st.session_state.english_chat.append(("A7DO", reply))

        for speaker, message in st.session_state.english_chat:
            st.markdown(f"**{speaker}:** {message}")

    st.divider()
    st.subheader("🟢 First Expression")

    if (
        st.session_state.english_expression_ready
        and st.session_state.english_first_output is None
    ):
        st.warning("A7DO is ready for a first expression.")
        out = st.text_area("A7DO First Expression", key="english_first_expression")

        if out:
            st.session_state.english_first_output = out

    elif st.session_state.english_first_output:
        st.success("First expression captured.")
        st.text_area(
            "A7DO Output",
            st.session_state.english_first_output,
            disabled=True,
        )
