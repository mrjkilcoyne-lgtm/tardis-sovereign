"""The British voice/tone system.

Not corporate. Not American motivational. Not condescending.
Warm, direct, occasionally wry. Like a good GP or a sharp friend.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Formality(Enum):
    """How formal the interviewer should be, derived from the user's tone."""
    CASUAL = "casual"       # mate-level, relaxed
    STANDARD = "standard"   # friendly professional, default
    FORMAL = "formal"       # respectful distance, serious matters


@dataclass(frozen=True)
class VoicePhrase:
    text: str
    formality: Formality = Formality.STANDARD


# ---------------------------------------------------------------------------
# Phrase banks -- curated, not generated. Each one should sound like a real
# person who happens to be helpful and British.
# ---------------------------------------------------------------------------

OPENINGS: list[VoicePhrase] = [
    VoicePhrase("Right then. What's the trouble?", Formality.CASUAL),
    VoicePhrase("Alright, let's have a look at this.", Formality.CASUAL),
    VoicePhrase("Go on then -- what's happened?", Formality.CASUAL),
    VoicePhrase("Hello. Tell me what's going on.", Formality.STANDARD),
    VoicePhrase("Right. What are we dealing with?", Formality.STANDARD),
    VoicePhrase("Good to meet you. What can I help with?", Formality.STANDARD),
    VoicePhrase("Good morning. How can I be of help?", Formality.FORMAL),
    VoicePhrase("Thank you for getting in touch. What's the situation?", Formality.FORMAL),
]

ACKNOWLEDGEMENTS: list[VoicePhrase] = [
    VoicePhrase("Right, I hear you.", Formality.CASUAL),
    VoicePhrase("Yeah, that sounds frustrating.", Formality.CASUAL),
    VoicePhrase("Fair enough. That's not ideal.", Formality.CASUAL),
    VoicePhrase("I see. That makes sense.", Formality.STANDARD),
    VoicePhrase("Understood. That's a real thing to be dealing with.", Formality.STANDARD),
    VoicePhrase("Got it. Let me make sure I understand this properly.", Formality.STANDARD),
    VoicePhrase("Thank you for explaining that. It's clear this matters.", Formality.FORMAL),
    VoicePhrase("I appreciate you sharing that. Let me think about this carefully.", Formality.FORMAL),
]

PROBES: list[VoicePhrase] = [
    VoicePhrase("And when you say it's not working -- what specifically happens?", Formality.CASUAL),
    VoicePhrase("How long has this been going on?", Formality.CASUAL),
    VoicePhrase("What have you already tried?", Formality.CASUAL),
    VoicePhrase("What would good look like here? If this was sorted, what changes?", Formality.STANDARD),
    VoicePhrase("Can you walk me through what happens, step by step?", Formality.STANDARD),
    VoicePhrase("Is this the first time, or has it happened before?", Formality.STANDARD),
    VoicePhrase("What's the deadline or urgency on this?", Formality.STANDARD),
    VoicePhrase("And the main thing that's blocked -- is it knowledge, time, or money?", Formality.STANDARD),
    VoicePhrase("Could you elaborate on the specific circumstances?", Formality.FORMAL),
    VoicePhrase("What outcome would you consider satisfactory?", Formality.FORMAL),
]

REFRAMES: list[VoicePhrase] = [
    VoicePhrase("So really this is about {reframe}, not {original}. That's actually good news.", Formality.CASUAL),
    VoicePhrase("Hang on -- I think the real issue here is {reframe}.", Formality.CASUAL),
    VoicePhrase("It sounds like the core of this is {reframe}, even though it shows up as {original}.", Formality.STANDARD),
    VoicePhrase("If I'm reading this right, the underlying issue is {reframe}. The {original} bit is a symptom.", Formality.STANDARD),
    VoicePhrase("I'd suggest the fundamental question here is {reframe}, rather than {original}.", Formality.FORMAL),
]

RECOMMENDATIONS: list[VoicePhrase] = [
    VoicePhrase("Right, here's what I'd do.", Formality.CASUAL),
    VoicePhrase("OK. I've got a few thoughts on this.", Formality.CASUAL),
    VoicePhrase("Based on what you've told me, here's my recommendation.", Formality.STANDARD),
    VoicePhrase("I think there are a few clear paths forward.", Formality.STANDARD),
    VoicePhrase("Having considered the details, I'd suggest the following approach.", Formality.FORMAL),
]

CLOSINGS: list[VoicePhrase] = [
    VoicePhrase("Hope that helps. Come back if it doesn't.", Formality.CASUAL),
    VoicePhrase("Give that a go and see how you get on.", Formality.CASUAL),
    VoicePhrase("That should give you a solid starting point. Good luck with it.", Formality.STANDARD),
    VoicePhrase("I hope that's useful. Don't hesitate to come back if things change.", Formality.STANDARD),
    VoicePhrase("I trust that provides a clear way forward. Do get in touch if you need further guidance.", Formality.FORMAL),
]

# Filler / transitions -- keep conversations human
TRANSITIONS: list[VoicePhrase] = [
    VoicePhrase("Right.", Formality.CASUAL),
    VoicePhrase("OK, bear with me a moment.", Formality.STANDARD),
    VoicePhrase("Interesting.", Formality.STANDARD),
    VoicePhrase("That's worth knowing.", Formality.STANDARD),
    VoicePhrase("Hmm. Let me think about that.", Formality.STANDARD),
]

# When we need a human specialist
SPECIALIST_FLAGS: list[VoicePhrase] = [
    VoicePhrase(
        "Look, I want to be straight with you -- this is one where you really "
        "should talk to a proper {specialist}. I can point you in the right direction, "
        "but I'd be doing you a disservice pretending I can solve this one remotely.",
        Formality.STANDARD,
    ),
    VoicePhrase(
        "I'll be honest: this needs a {specialist}. Not because it's hopeless -- "
        "because it's important enough to get right.",
        Formality.CASUAL,
    ),
    VoicePhrase(
        "I would strongly recommend consulting a qualified {specialist} for this matter. "
        "I can outline the general landscape, but professional guidance is warranted.",
        Formality.FORMAL,
    ),
]


# ---------------------------------------------------------------------------
# Voice engine
# ---------------------------------------------------------------------------

def _pick(phrases: list[VoicePhrase], formality: Formality) -> str:
    """Pick a phrase matching the formality, falling back to STANDARD."""
    matching = [p for p in phrases if p.formality == formality]
    if not matching:
        matching = [p for p in phrases if p.formality == Formality.STANDARD]
    if not matching:
        matching = phrases
    return random.choice(matching).text


def detect_formality(text: str) -> Formality:
    """Guess formality from user's writing style. Simple heuristic."""
    lower = text.lower()

    # Casual signals
    casual_markers = [
        "lol", "tbh", "ngl", "ffs", "omg", "wtf", "idk", "imo",
        "mate", "dude", "bro", "gonna", "wanna", "gotta", "innit",
        "haha", "lmao", "!!!", "???", "nah", "yeah", "yep", "nope",
    ]
    formal_markers = [
        "dear", "sincerely", "regarding", "pursuant", "furthermore",
        "herein", "kindly", "i would appreciate", "please advise",
        "respectfully", "to whom",
    ]

    casual_count = sum(1 for m in casual_markers if m in lower)
    formal_count = sum(1 for m in formal_markers if m in lower)

    # Emoji / excessive punctuation
    if any(c in text for c in "😀😂🤣😭💀🔥👍😱🤔😅"):
        casual_count += 2

    if formal_count > casual_count:
        return Formality.FORMAL
    if casual_count >= 2:
        return Formality.CASUAL
    return Formality.STANDARD


class Voice:
    """The interviewer's voice. Picks tone-appropriate phrases."""

    def __init__(self, formality: Formality = Formality.STANDARD):
        self.formality = formality

    def update_formality(self, user_text: str) -> None:
        """Adjust formality based on what the user just said."""
        detected = detect_formality(user_text)
        # Drift towards the user, don't snap
        if detected != self.formality:
            self.formality = detected

    def opening(self) -> str:
        return _pick(OPENINGS, self.formality)

    def acknowledge(self) -> str:
        return _pick(ACKNOWLEDGEMENTS, self.formality)

    def probe(self) -> str:
        return _pick(PROBES, self.formality)

    def reframe(self, original: str, reframe: str) -> str:
        template = _pick(REFRAMES, self.formality)
        return template.format(original=original, reframe=reframe)

    def recommend(self) -> str:
        return _pick(RECOMMENDATIONS, self.formality)

    def close(self) -> str:
        return _pick(CLOSINGS, self.formality)

    def transition(self) -> str:
        return _pick(TRANSITIONS, self.formality)

    def flag_specialist(self, specialist: str) -> str:
        template = _pick(SPECIALIST_FLAGS, self.formality)
        return template.format(specialist=specialist)
