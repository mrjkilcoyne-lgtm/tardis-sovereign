"""Psychic Paper - Shows exactly what you need it to show.

Like The Doctor's psychic paper: a single surface that becomes
whatever credential the situation requires. Reads the context,
morphs to match, and presents itself with quiet confidence.
"""

from .context import read_context, Context
from .engine import PsychicPaper
from .schemas import DOCUMENT_TYPES

__all__ = ["PsychicPaper", "read_context", "Context", "DOCUMENT_TYPES"]
