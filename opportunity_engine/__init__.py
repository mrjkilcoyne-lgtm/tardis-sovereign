"""Opportunity Engine - Finds legitimate openings in the world.

Scans competitions, grants, freelance platforms, API arbitrage,
cashback, referral programmes, and creative monetisation paths.
Produces a daily briefing of what's available right now.

Fixed points and multiplicities. Time runs both ways.
"""

from .scanner import scan_opportunities, OpportunityBriefing
from .strategies import STRATEGIES

__all__ = ["scan_opportunities", "OpportunityBriefing", "STRATEGIES"]
