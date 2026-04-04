"""Context reader. Reads the world to figure out what document is needed.

Looks at time, day, keywords, location hints, and situation descriptors
to pick the right document type. Quiet observation, not interrogation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime

from .schemas import DOCUMENT_TYPES, DocumentType


@dataclass
class Context:
    """What we know about the current situation."""
    situation: str = ""          # free text describing what's needed
    time: datetime = field(default_factory=datetime.now)
    location: str = ""           # venue, city, etc.
    audience: str = ""           # who's looking at this
    formality: str = "standard"  # casual, standard, formal, official
    urgency: str = "normal"      # normal, urgent, immediate
    # Pre-filled data the user wants on the document
    data: dict = field(default_factory=dict)


def read_context(
    situation: str = "",
    location: str = "",
    audience: str = "",
    formality: str = "standard",
    data: dict | None = None,
) -> Context:
    """Build a context from available signals."""
    return Context(
        situation=situation,
        time=datetime.now(),
        location=location,
        audience=audience,
        formality=formality,
        data=data or {},
    )


def detect_document_type(ctx: Context) -> DocumentType:
    """Figure out what document the situation calls for.

    Scores each document type against the context and picks
    the best match. Falls back to a generic pass if nothing fits.
    """
    text = f"{ctx.situation} {ctx.location} {ctx.audience}".lower()
    scores: list[tuple[float, str]] = []

    for type_id, doc_type in DOCUMENT_TYPES.items():
        score = _score_match(text, doc_type, ctx)
        scores.append((score, type_id))

    scores.sort(reverse=True)

    if scores and scores[0][0] > 0:
        return DOCUMENT_TYPES[scores[0][1]]

    # Default: conference badge (most versatile)
    return DOCUMENT_TYPES["conference_badge"]


def _score_match(text: str, doc_type: DocumentType, ctx: Context) -> float:
    """Score how well a document type matches the context."""
    score = 0.0

    # Keyword matching - each hit adds weight
    for kw in doc_type.context_keywords:
        if kw in text:
            score += 10.0
            # Exact word boundary match scores higher
            if re.search(rf'\b{re.escape(kw)}\b', text):
                score += 5.0

    # Formality alignment
    formal_docs = {"driving_licence", "security_badge", "permit"}
    casual_docs = {"membership", "event_ticket"}

    if ctx.formality == "official" and doc_type.type_id in formal_docs:
        score += 3.0
    elif ctx.formality == "casual" and doc_type.type_id in casual_docs:
        score += 3.0

    # Time-based hints
    hour = ctx.time.hour
    if 6 <= hour <= 9 and doc_type.type_id == "transport_pass":
        score += 2.0  # commute time
    if 18 <= hour <= 23 and doc_type.type_id in ("event_ticket", "invitation"):
        score += 2.0  # evening events

    # If user data keys match document fields, boost
    if ctx.data:
        field_names = {f.name for f in doc_type.fields}
        overlap = set(ctx.data.keys()) & field_names
        score += len(overlap) * 3.0

    return score
