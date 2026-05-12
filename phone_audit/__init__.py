"""Phone Audit - TARDIS-grade device rationalisation.

Reverse engineers your app stack. Figures out what you actually use,
what's snooping on you, what you're missing, and what could be combined.
Then rebuilds it better, sleeker, more private, more powerful.

She doesn't follow fashion. She sets it.
"""

from .auditor import audit_apps, AuditReport
from .alternatives import REPLACEMENTS

__all__ = ["audit_apps", "AuditReport", "REPLACEMENTS"]
