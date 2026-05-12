"""Scanner. Produces daily briefings of what's available right now.

Time runs both directions. Look at what's coming, what's here,
and what's closing soon.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime

from .strategies import STRATEGIES, Strategy, filter_strategies


@dataclass
class Opportunity:
    """A specific, actionable opportunity right now."""
    strategy: Strategy
    action: str             # specific next step
    urgency: str            # now, this_week, this_month, ongoing
    estimated_return: str
    time_to_complete: str
    link: str = ""


@dataclass
class OpportunityBriefing:
    """The daily briefing. What TARDIS found."""
    generated_at: datetime = field(default_factory=datetime.now)
    capital_available: float = 200.0
    fixed_points: list[Opportunity] = field(default_factory=list)
    multiplicities: list[Opportunity] = field(default_factory=list)
    quick_wins: list[Opportunity] = field(default_factory=list)
    total_potential_monthly: str = ""

    def to_markdown(self) -> str:
        lines = [
            f"# Opportunity Briefing",
            f"*Generated {self.generated_at.strftime('%d %B %Y, %H:%M')}*",
            f"*Capital available: £{self.capital_available:.2f}*",
            "",
        ]

        if self.quick_wins:
            lines.append("## Quick Wins (do today)")
            lines.append("")
            for o in self.quick_wins:
                lines.append(f"**{o.strategy.name}** — {o.estimated_return}")
                lines.append(f"  {o.action}")
                if o.link:
                    lines.append(f"  {o.link}")
                lines.append("")

        if self.fixed_points:
            lines.append("## Fixed Points (guaranteed returns)")
            lines.append("")
            for o in self.fixed_points:
                lines.append(f"**{o.strategy.name}** [{o.urgency}]")
                lines.append(f"  Return: {o.estimated_return} | Time: {o.time_to_complete}")
                lines.append(f"  → {o.action}")
                if o.strategy.notes:
                    lines.append(f"  _{o.strategy.notes}_")
                lines.append("")

        if self.multiplicities:
            lines.append("## Multiplicities (variable, higher potential)")
            lines.append("")
            for o in self.multiplicities:
                lines.append(f"**{o.strategy.name}** [{o.urgency}] — Risk: {o.strategy.risk_level}")
                lines.append(f"  Return: {o.estimated_return} | Time: {o.time_to_complete}")
                lines.append(f"  → {o.action}")
                if o.strategy.notes:
                    lines.append(f"  _{o.strategy.notes}_")
                lines.append("")

        if self.total_potential_monthly:
            lines.append(f"---")
            lines.append(f"**Total potential monthly (if all actioned): {self.total_potential_monthly}**")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "generated_at": self.generated_at.isoformat(),
            "capital": self.capital_available,
            "quick_wins": [{"name": o.strategy.name, "action": o.action, "return": o.estimated_return} for o in self.quick_wins],
            "fixed_points": [{"name": o.strategy.name, "action": o.action, "return": o.estimated_return, "urgency": o.urgency} for o in self.fixed_points],
            "multiplicities": [{"name": o.strategy.name, "action": o.action, "return": o.estimated_return, "risk": o.strategy.risk_level} for o in self.multiplicities],
        }


def scan_opportunities(capital: float = 200.0, risk_tolerance: str = "medium") -> OpportunityBriefing:
    """Scan all strategies and produce an actionable briefing.

    Args:
        capital: How much money is available to deploy
        risk_tolerance: none, low, medium, high
    """
    available = filter_strategies(max_capital=capital, max_risk=risk_tolerance)

    briefing = OpportunityBriefing(capital_available=capital)

    for s in available:
        opp = _strategy_to_opportunity(s, capital)

        if s.category == "fixed_point":
            briefing.fixed_points.append(opp)
        else:
            briefing.multiplicities.append(opp)

        # Quick wins: can be started today, low effort
        if s.effort in ("low", "passive") and s.min_capital <= capital:
            briefing.quick_wins.append(opp)

    # Sort quick wins by immediacy
    urgency_order = {"now": 0, "this_week": 1, "this_month": 2, "ongoing": 3}
    briefing.quick_wins.sort(key=lambda o: urgency_order.get(o.urgency, 3))
    briefing.fixed_points.sort(key=lambda o: urgency_order.get(o.urgency, 3))

    briefing.total_potential_monthly = _estimate_monthly(available, capital)

    return briefing


def _strategy_to_opportunity(s: Strategy, capital: float) -> Opportunity:
    """Convert a strategy into a specific actionable opportunity."""
    actions = {
        "Bank Account Switching Bonuses": "Open First Direct account via switching service. Needs 2 direct debits + £1000 pay-in.",
        "Savings Account Rate Optimisation": f"Move £{capital:.0f} to Chase easy-access (5.1% AER). Takes 10 minutes.",
        "Cashback and Reward Stacking": "Apply for Chase debit card (1% cashback on everything). Route all spending through it.",
        "Matched Betting (intro offers)": "Sign up to OddsMonkey (free trial). Follow the intro offer guides. Start with smallest bets.",
        "Competition Entry Automation": "Set up ThePrizeFinder account. Enter 10 skill-based comps today (25-words-or-less).",
        "Freelance Micro-Tasks": "Sign up to Prolific.co and UserTesting.com. Complete profile for better study matches.",
        "API Arbitrage / Data Services": "Pick one useful API combination. Build with sovereign dispatch. List on RapidAPI.",
        "Content Monetisation": "Start Substack with your policy/tech analysis. First 3 posts this week.",
        "Invention Licensing": "Use hex-inventions daily teardown to identify licensable improvement. Draft provisional patent.",
        "Referral Programme Chains": "Share Trading 212 and Chase referral links. Each successful referral = £10-50.",
        "Print on Demand / Digital Products": "Create 5 designs on Redbubble. Use the TARDIS/psychic paper aesthetic.",
        "Grant Applications": "Draft Innovate UK Smart Grant application for InventorForge platform.",
    }

    urgency_map = {
        "fixed_point": "this_week",
        "multiplicity": "this_month",
        "recurring": "ongoing",
        "one_shot": "this_month",
    }

    return Opportunity(
        strategy=s,
        action=actions.get(s.name, f"Research and start: {s.name}"),
        urgency=urgency_map.get(s.category, "ongoing"),
        estimated_return=s.expected_return,
        time_to_complete=s.time_horizon,
    )


def _estimate_monthly(strategies: list[Strategy], capital: float) -> str:
    """Conservative estimate of combined monthly potential."""
    # Fixed points are more predictable
    fixed_min = 0
    for s in strategies:
        if s.category == "fixed_point":
            # Extract first number from expected_return
            nums = [int(c) for c in s.expected_return.replace(",", "").split() if c.isdigit()]
            if nums:
                fixed_min += nums[0] // max(1, int(s.time_horizon.split()[0]) if s.time_horizon[0].isdigit() else 1)

    return f"£{max(200, fixed_min)}-£2,000+ (conservative to optimistic)"
