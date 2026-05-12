"""The conversation engine.

A state machine that listens, clarifies, diagnoses, and recommends.
Warm but precise. Asks good questions, not many questions.
Max 6 exchanges before it must produce a recommendation.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .domains import (
    ALL_DOMAINS, Domain, CrossDomain,
    detect_domains, detect_cross_domain,
)
from .router import Pathways, Solution, route, needs_human
from .voice import Voice, Formality, detect_formality


class State(Enum):
    GREETING = "greeting"
    LISTENING = "listening"
    CLARIFYING = "clarifying"
    DIAGNOSING = "diagnosing"
    RECOMMENDING = "recommending"
    CLOSING = "closing"


@dataclass
class Exchange:
    """A single conversational exchange."""
    user: str
    interviewer: str
    state: State
    timestamp: float = field(default_factory=time.time)


@dataclass
class InterviewResult:
    """The structured output of a completed interview."""
    summary: str
    diagnosis: str
    primary_domain: str
    secondary_domains: list[str]
    cross_domain: str | None
    pathways: dict[str, Any]       # quick_win, structural_fix, adaptation
    recommended_actions: list[str]
    confidence_score: float        # 0.0 to 1.0
    needs_specialist: bool
    specialist_type: str
    exchange_count: int
    raw_exchanges: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "diagnosis": self.diagnosis,
            "primary_domain": self.primary_domain,
            "secondary_domains": self.secondary_domains,
            "cross_domain": self.cross_domain,
            "pathways": self.pathways,
            "recommended_actions": self.recommended_actions,
            "confidence_score": self.confidence_score,
            "needs_specialist": self.needs_specialist,
            "specialist_type": self.specialist_type,
            "exchange_count": self.exchange_count,
        }


class Interview:
    """The conversation state machine.

    Usage::

        iv = Interview()
        greeting = iv.start()        # Returns greeting text
        response = iv.respond(text)  # Returns interviewer's response
        # ... continue until iv.is_complete
        result = iv.result           # InterviewResult
    """

    MAX_EXCHANGES = 6

    def __init__(self) -> None:
        self.state = State.GREETING
        self.voice = Voice()
        self.exchanges: list[Exchange] = []
        self.all_user_text: list[str] = []

        # Domain tracking -- updated as we listen
        self._domain_scores: list[tuple[Domain, float]] = []
        self._cross_domain: CrossDomain | None = None
        self._primary_domain: Domain | None = None

        # Diagnosis state
        self._problem_summary: str = ""
        self._diagnosis: str = ""
        self._pathways: Pathways | None = None
        self._confidence: float = 0.0
        self._result: InterviewResult | None = None

        # Clarifying questions asked (avoid repeats)
        self._questions_asked: list[str] = []

    @property
    def is_complete(self) -> bool:
        return self.state == State.CLOSING and self._result is not None

    @property
    def result(self) -> InterviewResult | None:
        return self._result

    @property
    def exchange_count(self) -> int:
        return len(self.exchanges)

    def start(self) -> str:
        """Begin the interview. Returns the greeting."""
        self.state = State.GREETING
        greeting = self.voice.opening()
        return greeting

    def respond(self, user_input: str) -> str:
        """Process user input and return the interviewer's response.

        This drives the state machine forward. After enough information,
        it diagnoses and recommends automatically.
        """
        user_input = user_input.strip()
        if not user_input:
            return "Sorry, I didn't catch that. Go on?"

        # Update voice to match user's tone
        self.voice.update_formality(user_input)
        self.all_user_text.append(user_input)

        # Update domain detection with all text so far
        combined_text = " ".join(self.all_user_text)
        self._domain_scores = detect_domains(combined_text)
        if self._domain_scores:
            self._primary_domain = self._domain_scores[0][0]
        self._cross_domain = detect_cross_domain(self._domain_scores)

        # State transitions
        if self.state == State.GREETING:
            return self._handle_greeting(user_input)
        elif self.state == State.LISTENING:
            return self._handle_listening(user_input)
        elif self.state == State.CLARIFYING:
            return self._handle_clarifying(user_input)
        elif self.state == State.DIAGNOSING:
            return self._handle_diagnosing(user_input)
        elif self.state == State.RECOMMENDING:
            return self._handle_recommending(user_input)
        else:
            return self._produce_closing()

    def _record(self, user: str, response: str) -> None:
        self.exchanges.append(Exchange(
            user=user, interviewer=response, state=self.state,
        ))

    def _should_diagnose(self) -> bool:
        """Decide if we have enough to diagnose."""
        # Must diagnose at MAX_EXCHANGES
        if self.exchange_count >= self.MAX_EXCHANGES - 1:
            return True
        # Can diagnose early if confident
        if self._domain_scores and self._domain_scores[0][1] > 0.15:
            if self.exchange_count >= 2:
                return True
        return False

    # -------------------------------------------------------------------
    # State handlers
    # -------------------------------------------------------------------

    def _handle_greeting(self, user_input: str) -> str:
        self.state = State.LISTENING
        ack = self.voice.acknowledge()
        # If they've already given substance, move to clarifying
        if len(user_input.split()) > 15 and self._domain_scores:
            self.state = State.CLARIFYING
            question = self._pick_clarifying_question()
            response = f"{ack} {question}"
        else:
            response = f"{ack} Tell me more about what's going on."
        self._record(user_input, response)
        return response

    def _handle_listening(self, user_input: str) -> str:
        if self._should_diagnose():
            return self._transition_to_diagnosis(user_input)

        self.state = State.CLARIFYING
        ack = self.voice.acknowledge()
        question = self._pick_clarifying_question()
        response = f"{ack} {question}"
        self._record(user_input, response)
        return response

    def _handle_clarifying(self, user_input: str) -> str:
        if self._should_diagnose():
            return self._transition_to_diagnosis(user_input)

        # Ask one more targeted question if we have a domain
        question = self._pick_clarifying_question()
        if question and self.exchange_count < self.MAX_EXCHANGES - 1:
            transition = self.voice.transition()
            response = f"{transition} {question}"
            self._record(user_input, response)
            return response

        # Otherwise, diagnose
        return self._transition_to_diagnosis(user_input)

    def _handle_diagnosing(self, user_input: str) -> str:
        # User responded to our diagnosis -- proceed to recommendation
        return self._produce_recommendation(user_input)

    def _handle_recommending(self, user_input: str) -> str:
        return self._produce_closing()

    def _transition_to_diagnosis(self, user_input: str) -> str:
        """Produce a diagnosis and ask for confirmation."""
        self.state = State.DIAGNOSING
        self._build_diagnosis()

        domain_name = self._primary_domain.name if self._primary_domain else "general"

        # Build the diagnosis statement
        parts = [self.voice.transition()]

        if self._cross_domain:
            parts.append(
                f"This looks like it sits across a couple of areas -- "
                f"{self._cross_domain.description.lower()}."
            )
        else:
            parts.append(f"This sounds like a {domain_name.lower()} issue at its core.")

        parts.append(f"If I'm reading this right: {self._diagnosis}")
        parts.append("Does that sound about right, or am I missing something?")

        response = " ".join(parts)
        self._record(user_input, response)
        return response

    def _produce_recommendation(self, user_input: str) -> str:
        """Produce the recommendation."""
        self.state = State.RECOMMENDING

        # Route to solutions
        if self._primary_domain:
            self._pathways = route(
                domain=self._primary_domain,
                problem_summary=self._diagnosis,
                cross_domain=self._cross_domain,
                severity=self._estimate_severity(),
            )

        recommend_intro = self.voice.recommend()
        parts = [recommend_intro]

        if self._pathways:
            if self._pathways.quick_win:
                qw = self._pathways.quick_win
                parts.append(f"\nFirst, the quick win: {qw.title}. {qw.description}")
                if qw.steps:
                    parts.append("Steps: " + " -> ".join(qw.steps[:3]))

            if self._pathways.structural_fix:
                sf = self._pathways.structural_fix
                parts.append(f"\nLonger term: {sf.title}. {sf.description}")

            if self._pathways.adaptation:
                ad = self._pathways.adaptation
                parts.append(f"\nAnd if you need to live with it for now: {ad.title}. {ad.description}")

            if needs_human(self._pathways):
                specialist = (self._pathways.structural_fix.specialist_type
                              if self._pathways.structural_fix
                              else self._primary_domain.specialist_title
                              if self._primary_domain else "specialist")
                parts.append("\n" + self.voice.flag_specialist(specialist))

        response = "\n".join(parts)
        self._build_result()
        self._record(user_input, response)

        # Auto-close
        closing = self.voice.close()
        self.state = State.CLOSING
        return response + "\n\n" + closing

    def _produce_closing(self) -> str:
        self.state = State.CLOSING
        if not self._result:
            self._build_diagnosis()
            if self._primary_domain:
                self._pathways = route(
                    domain=self._primary_domain,
                    problem_summary=self._diagnosis,
                    cross_domain=self._cross_domain,
                )
            self._build_result()
        return self.voice.close()

    # -------------------------------------------------------------------
    # Internal logic
    # -------------------------------------------------------------------

    def _pick_clarifying_question(self) -> str:
        """Pick the best follow-up question based on detected domain."""
        if self._primary_domain:
            for q in self._primary_domain.follow_up_questions:
                if q not in self._questions_asked:
                    self._questions_asked.append(q)
                    return q

        # Fallback generic questions
        generic = [
            "What's the most important thing to get right here?",
            "And what have you already tried?",
            "What would good look like?",
            "Is there a deadline on this?",
        ]
        for q in generic:
            if q not in self._questions_asked:
                self._questions_asked.append(q)
                return q

        return self.voice.probe()

    def _build_diagnosis(self) -> None:
        """Build a one-line diagnosis from accumulated information."""
        all_text = " ".join(self.all_user_text)
        words = all_text.split()

        # Extract key phrases (simple: first substantial sentence from user)
        # In a real system this would use NLP; here we summarise from keywords
        domain_name = self._primary_domain.name.lower() if self._primary_domain else "general"

        if self._cross_domain:
            self._diagnosis = (
                f"You're dealing with a {self._cross_domain.description.lower()}. "
                f"This involves both {self._cross_domain.domain_a} and "
                f"{self._cross_domain.domain_b} considerations."
            )
        elif self._primary_domain:
            # Match against typical patterns
            best_pattern = self._match_pattern(all_text)
            if best_pattern:
                self._diagnosis = (
                    f"This is a {domain_name} situation -- specifically, "
                    f"it looks like: {best_pattern.lower()}."
                )
            else:
                self._diagnosis = (
                    f"You've got a {domain_name} problem that needs addressing."
                )
        else:
            self._diagnosis = "You've described a situation that needs a clear plan of action."

        self._confidence = self._calculate_confidence()

    def _match_pattern(self, text: str) -> str | None:
        """Match user text against typical patterns for the primary domain."""
        if not self._primary_domain:
            return None
        lower = text.lower()
        best_score = 0
        best_pattern = None
        for pattern in self._primary_domain.typical_patterns:
            pattern_words = set(pattern.lower().split())
            overlap = sum(1 for w in pattern_words if w in lower)
            score = overlap / len(pattern_words) if pattern_words else 0
            if score > best_score:
                best_score = score
                best_pattern = pattern
        return best_pattern if best_score > 0.2 else None

    def _calculate_confidence(self) -> float:
        """Calculate confidence based on information gathered."""
        score = 0.3  # base

        # More exchanges = more information
        score += min(0.2, self.exchange_count * 0.05)

        # Strong domain signal
        if self._domain_scores:
            top_score = self._domain_scores[0][1]
            score += min(0.2, top_score * 2)

        # Cross-domain detection is a good sign
        if self._cross_domain:
            score += 0.1

        # Capped at 0.95 -- we're never certain
        return min(0.95, score)

    def _estimate_severity(self) -> float:
        """Estimate problem severity from language cues."""
        all_text = " ".join(self.all_user_text).lower()
        severity = 0.5

        urgent_words = [
            "urgent", "emergency", "desperate", "crisis", "immediately",
            "can't wait", "deadline", "tomorrow", "tonight", "asap",
            "losing", "lost", "evicted", "fired", "dangerous", "unsafe",
        ]
        mild_words = [
            "wondering", "curious", "thinking about", "might", "eventually",
            "someday", "no rush", "when I get around to",
        ]

        for w in urgent_words:
            if w in all_text:
                severity += 0.1
        for w in mild_words:
            if w in all_text:
                severity -= 0.1

        return max(0.1, min(1.0, severity))

    def _build_result(self) -> None:
        """Build the final InterviewResult."""
        domain_name = self._primary_domain.slug if self._primary_domain else "general"
        secondary = [d.slug for d, _ in self._domain_scores[1:]]
        cross = self._cross_domain.label if self._cross_domain else None

        # Build recommended actions
        actions: list[str] = []
        if self._pathways:
            if self._pathways.quick_win:
                actions.append(f"Quick win: {self._pathways.quick_win.title}")
                actions.extend(self._pathways.quick_win.steps[:3])
            if self._pathways.structural_fix:
                actions.append(f"Longer term: {self._pathways.structural_fix.title}")
            if self._pathways.adaptation:
                actions.append(f"Adaptation: {self._pathways.adaptation.title}")

        specialist_needed = needs_human(self._pathways) if self._pathways else False
        specialist_type = ""
        if specialist_needed and self._pathways and self._pathways.structural_fix:
            specialist_type = self._pathways.structural_fix.specialist_type
        elif self._primary_domain:
            specialist_type = self._primary_domain.specialist_title

        raw = [{"user": e.user, "interviewer": e.interviewer} for e in self.exchanges]

        self._result = InterviewResult(
            summary=self._build_summary(),
            diagnosis=self._diagnosis,
            primary_domain=domain_name,
            secondary_domains=secondary,
            cross_domain=cross,
            pathways=self._pathways.to_dict() if self._pathways else {},
            recommended_actions=actions,
            confidence_score=self._confidence,
            needs_specialist=specialist_needed,
            specialist_type=specialist_type,
            exchange_count=self.exchange_count,
            raw_exchanges=raw,
        )

    def _build_summary(self) -> str:
        """Build a human-readable summary of the conversation."""
        if not self.all_user_text:
            return "No conversation recorded."

        # Take the key points from user input
        first_input = self.all_user_text[0]
        if len(first_input) > 200:
            first_input = first_input[:200] + "..."

        domain_str = self._primary_domain.name if self._primary_domain else "General"
        return (
            f"Interview about a {domain_str.lower()} matter. "
            f"The user described: {first_input}"
        )


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def interview() -> Interview:
    """Create and return a new Interview instance.

    Usage::

        iv = interview()
        print(iv.start())
        while not iv.is_complete:
            user_input = input("> ")
            print(iv.respond(user_input))
        print(iv.result.to_dict())
    """
    return Interview()
