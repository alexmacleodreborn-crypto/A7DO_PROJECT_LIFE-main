"""
A7DO — English Language Learning (Streamlit UI)
"""

from __future__ import annotations

import random
import re

import streamlit as st
from streamlit_autorefresh import st_autorefresh

# =========================================================
# A7DO — ENGLISH LANGUAGE LEARNING EXTENSION
# =========================================================

st.set_page_config(page_title="A7DO English Learning", layout="centered")

# ---------------------------------------------------------
# CLOCK
# ---------------------------------------------------------
tick = st_autorefresh(interval=600, limit=None, key="a7do_clock")

# ---------------------------------------------------------
# INITIAL STATE
# ---------------------------------------------------------
if "init" not in st.session_state:
    st.session_state.init = True

    # Development
    st.session_state.age = 0
    st.session_state.K = 0.2
    st.session_state.I = 0.1
    st.session_state.intent = 0.0

    # Language learning
    st.session_state.vocab = {}
    st.session_state.concepts = {}
    st.session_state.patterns = {}

    # Identity & memory
    st.session_state.identity = {}
    st.session_state.life_events = []

    # Emergence
    st.session_state.invited = False
    st.session_state.expression_ready = False
    st.session_state.first_output = None

    # Conversation
    st.session_state.chat = []

# ---------------------------------------------------------
# ENGLISH LEARNING DATA
# ---------------------------------------------------------
BASIC_WORDS = [
    "i",
    "you",
    "we",
    "he",
    "she",
    "it",
    "hello",
    "name",
    "birthday",
    "school",
    "like",
    "love",
    "see",
    "go",
    "have",
    "am",
    "is",
    "are",
    "play",
    "learn",
    "friend",
    "people",
    "today",
    "happy",
    "blue",
    "music",
    "talk",
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

# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def absorb_words(words: list[str], weight: float = 0.03) -> None:
    for word in words:
        st.session_state.vocab[word] = st.session_state.vocab.get(word, 0) + 1
        st.session_state.concepts[word] = st.session_state.concepts.get(word, 0) + weight


def absorb_sentence(sentence: str) -> None:
    words = tokenize(sentence)
    absorb_words(words, weight=0.05)

    pattern = tuple(words)
    st.session_state.patterns[pattern] = st.session_state.patterns.get(pattern, 0) + 1


def language_understanding() -> float:
    if not st.session_state.concepts:
        return 0.0
    stable = sum(1 for value in st.session_state.concepts.values() if value > 0.6)
    return stable / len(st.session_state.concepts)


# ---------------------------------------------------------
# AUTO ENGLISH LEARNING STEP
# ---------------------------------------------------------
# Vocabulary exposure
absorb_words(random.sample(BASIC_WORDS, k=3))

# Sentence exposure
absorb_sentence(random.choice(SENTENCE_PATTERNS))

# Connector exposure
absorb_words(random.sample(CONNECTORS, k=1), weight=0.02)

# Development update
U_lang = language_understanding()

st.session_state.age += 1
st.session_state.I = min(1.0, st.session_state.I + 0.01 + U_lang * 0.02)
st.session_state.K += 0.03 * st.session_state.I
st.session_state.intent += 0.04 * U_lang

# Invitation trigger
if not st.session_state.invited and st.session_state.K >= 1.2:
    st.session_state.invited = True

# Expression readiness
if (
    st.session_state.invited
    and not st.session_state.expression_ready
    and (U_lang >= 0.4 or st.session_state.age > 60)
):
    st.session_state.expression_ready = True

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.title("🧠 A7DO — English Language Learning")

st.write(f"**Age (cycles):** {st.session_state.age}")
st.write(f"**Portal Score K:** {st.session_state.K:.2f}")
st.write(f"**Language Understanding:** {U_lang:.2f}")
st.write(f"**Vocabulary Size:** {len(st.session_state.vocab)}")
st.write(f"**Sentence Patterns Learned:** {len(st.session_state.patterns)}")
st.write(f"**Intent:** {st.session_state.intent:.2f}")

st.divider()
st.info("📘 Learning English continuously: words, sentences, and structure.")

# ---------------------------------------------------------
# INVITATION & CONVERSATION
# ---------------------------------------------------------
if st.session_state.invited:
    st.success("📨 A7DO is ready to speak with you")

    with st.form("chat_form", clear_on_submit=True):
        user_msg = st.text_input("You:")
        send = st.form_submit_button("Send")

    if send and user_msg:
        absorb_sentence(user_msg)
        st.session_state.chat.append(("You", user_msg))

        # Progressive English reply
        if st.session_state.first_output is None:
            reply = random.choice(
                [
                    "I am listening.",
                    "I understand you.",
                    "Please continue.",
                    "I am learning English.",
                ]
            )
        else:
            reply = "I remember what you said."

        st.session_state.chat.append(("A7DO", reply))

    for speaker, message in st.session_state.chat:
        st.markdown(f"**{speaker}:** {message}")

st.divider()

# ---------------------------------------------------------
# FIRST EXPRESSION
# ---------------------------------------------------------
st.subheader("🟢 First Expression")

if st.session_state.expression_ready and st.session_state.first_output is None:
    st.warning("A7DO is ready for a first expression.")
    out = st.text_area("A7DO First Expression")

    if out:
        st.session_state.first_output = out

elif st.session_state.first_output:
    st.success("First expression captured.")
    st.text_area("A7DO Output", st.session_state.first_output, disabled=True)
