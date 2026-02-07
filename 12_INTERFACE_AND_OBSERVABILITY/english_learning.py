"""
A7DO — English language learning helpers for Streamlit dashboards.
"""

from __future__ import annotations

import random
import re
from typing import Callable

import streamlit as st

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


class EnglishLearning:
    def __init__(self, session_state: st.session_state.__class__, prefix: str = "english"):
        self.session_state = session_state
        self.prefix = prefix
        self.energy_cost = 0.2
        self._init_state()

    def _key(self, name: str) -> str:
        return f"{self.prefix}_{name}"

    def _get(self, name: str, default=None):
        return self.session_state.get(self._key(name), default)

    def _set(self, name: str, value) -> None:
        self.session_state[self._key(name)] = value

    def _init_state(self) -> None:
        if self._get("init"):
            return

        self._set("init", True)
        self._set("age", 0)
        self._set("K", 0.2)
        self._set("I", 0.1)
        self._set("intent", 0.0)
        self._set("vocab", {})
        self._set("concepts", {})
        self._set("patterns", {})
        self._set("invited", False)
        self._set("expression_ready", False)
        self._set("first_output", None)
        self._set("chat", [])
        self._set("last_status", "idle")

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-z']+", text.lower())

    def _absorb_words(self, words: list[str], weight: float = 0.03) -> None:
        vocab = self._get("vocab", {})
        concepts = self._get("concepts", {})
        for word in words:
            vocab[word] = vocab.get(word, 0) + 1
            concepts[word] = concepts.get(word, 0) + weight
        self._set("vocab", vocab)
        self._set("concepts", concepts)

    def _absorb_sentence(self, sentence: str) -> None:
        words = self._tokenize(sentence)
        self._absorb_words(words, weight=0.05)

        patterns = self._get("patterns", {})
        pattern = tuple(words)
        patterns[pattern] = patterns.get(pattern, 0) + 1
        self._set("patterns", patterns)

    def language_understanding(self) -> float:
        concepts = self._get("concepts", {})
        if not concepts:
            return 0.0
        stable = sum(1 for value in concepts.values() if value > 0.6)
        return stable / len(concepts)

    def advance(self, energy_gate: Callable[[], str] | None = None) -> float:
        if energy_gate is not None:
            status = energy_gate()
            if status != "ok":
                self._set("last_status", status)
                return self.language_understanding()

        self._absorb_words(random.sample(BASIC_WORDS, k=3))
        self._absorb_sentence(random.choice(SENTENCE_PATTERNS))
        self._absorb_words(random.sample(CONNECTORS, k=1), weight=0.02)

        understanding = self.language_understanding()
        self._set("age", self._get("age", 0) + 1)
        self._set(
            "I",
            min(1.0, self._get("I", 0.1) + 0.01 + understanding * 0.02),
        )
        self._set("K", self._get("K", 0.2) + 0.03 * self._get("I", 0.1))
        self._set("intent", self._get("intent", 0.0) + 0.04 * understanding)

        if not self._get("invited") and self._get("K", 0.0) >= 1.2:
            self._set("invited", True)

        if (
            self._get("invited")
            and not self._get("expression_ready")
            and (understanding >= 0.4 or self._get("age", 0) > 60)
        ):
            self._set("expression_ready", True)

        self._set("last_status", "advanced")
        return understanding

    def metrics(self) -> dict[str, float | int | str]:
        return {
            "age": self._get("age", 0),
            "K": self._get("K", 0.0),
            "I": self._get("I", 0.0),
            "intent": self._get("intent", 0.0),
            "vocab_size": len(self._get("vocab", {})),
            "pattern_count": len(self._get("patterns", {})),
            "last_status": self._get("last_status", "idle"),
            "understanding": self.language_understanding(),
        }

    def is_invited(self) -> bool:
        return bool(self._get("invited"))

    def expression_ready(self) -> bool:
        return bool(self._get("expression_ready"))

    def first_output(self):
        return self._get("first_output")

    def set_first_output(self, output: str) -> None:
        self._set("first_output", output)

    def chat_history(self) -> list[tuple[str, str]]:
        return list(self._get("chat", []))

    def add_user_message(self, message: str) -> str:
        self._absorb_sentence(message)
        chat = self._get("chat", [])
        chat.append(("You", message))

        if self.first_output() is None:
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

        chat.append(("A7DO", reply))
        self._set("chat", chat)
        return reply
