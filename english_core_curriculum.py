# =========================================================
# A7DO — CORE ENGLISH CURRICULUM MODULE
# =========================================================
# Purpose:
# Anchor grammar, identity, and sentence frames so
# language understanding grows meaningfully.
# =========================================================

import random
import re

# ---------------------------------------------------------
# CORE ENGLISH FRAMES (VERY IMPORTANT)
# ---------------------------------------------------------
CORE_FRAMES = {
    "identity": [
        "i am a7do",
        "my name is a7do",
        "you are a7do",
    ],
    "state": [
        "i am learning english",
        "i am here",
        "i am listening",
    ],
    "perception": [
        "i hear you",
        "i see words",
    ],
    "action": [
        "i am learning",
        "i am listening",
    ],
    "preference": [
        "i like blue",
        "i like music",
    ],
    "memory": [
        "i remember this",
        "i remember you",
    ],
}


# ---------------------------------------------------------
# TOKENISER (match your existing style)
# ---------------------------------------------------------
def _tokenize(text):
    return re.findall(r"[a-z']+", text.lower())


# ---------------------------------------------------------
# CORE LEARNING STEP
# ---------------------------------------------------------
def run_core_english_curriculum(state, weight=0.08):
    """
    state must expose:
      - state.vocab (dict)
      - state.concepts (dict)
      - state.patterns (dict)  [optional]
      - state.identity (dict)  [optional]

    This function mutates state in-place.
    """

    category = random.choice(list(CORE_FRAMES.keys()))
    sentence = random.choice(CORE_FRAMES[category])

    words = _tokenize(sentence)

    # --- Vocabulary + concept reinforcement ---
    for word in words:
        state.vocab[word] = state.vocab.get(word, 0) + 1
        state.concepts[word] = state.concepts.get(word, 0) + weight

    # --- Sentence pattern stability ---
    if hasattr(state, "patterns") and state.patterns is not None:
        key = tuple(words)
        state.patterns[key] = state.patterns.get(key, 0) + 1

    # --- Identity grounding ---
    if "my name is" in sentence and hasattr(state, "identity"):
        if state.identity is None:
            state.identity = {}
        state.identity["name"] = "A7DO"

    return sentence, category
