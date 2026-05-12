"""Strategies. Each one is a legitimate way to multiply capital.

Some are fixed points (guaranteed small returns).
Some are multiplicities (variable, potentially larger).
All are legal. All are real.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Strategy:
    name: str
    category: str           # fixed_point, multiplicity, recurring, one_shot
    description: str
    min_capital: float      # minimum to start
    expected_return: str    # realistic range
    time_horizon: str       # how long before returns
    risk_level: str         # none, low, medium, high
    effort: str             # passive, low, medium, active
    skills_needed: list[str] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    notes: str = ""


STRATEGIES: list[Strategy] = [

    # ── FIXED POINTS (guaranteed or near-guaranteed) ──

    Strategy(
        name="Bank Account Switching Bonuses",
        category="fixed_point",
        description="UK banks pay £100-175 to switch current accounts. Repeatable every few months.",
        min_capital=0,
        expected_return="£100-175 per switch",
        time_horizon="2-4 weeks",
        risk_level="none",
        effort="low",
        platforms=["First Direct (£175)", "Nationwide (£100)", "HSBC (£125)", "Lloyds", "NatWest"],
        notes="Requires direct debits and pay-in. Can chain 3-4 per year.",
    ),

    Strategy(
        name="Savings Account Rate Optimisation",
        category="fixed_point",
        description="Move capital to highest-rate easy access or notice accounts. Chase rates monthly.",
        min_capital=1,
        expected_return="4.5-5.2% AER currently",
        time_horizon="Immediate",
        risk_level="none",
        effort="low",
        platforms=["Chase (5.1%)", "Chip (regular saver)", "Plum", "Trading 212 (5.1%)", "Moneybox"],
        notes="FSCS protected up to £85k per institution.",
    ),

    Strategy(
        name="Cashback and Reward Stacking",
        category="fixed_point",
        description="Route all spending through cashback cards/apps. Stack: card + app + retailer.",
        min_capital=0,
        expected_return="2-8% on spending",
        time_horizon="Monthly",
        risk_level="none",
        effort="low",
        platforms=["Amex (cashback)", "Chase debit (1%)", "TopCashback", "Quidco", "Airtime Rewards"],
        notes="Chase debit gives 1% on everything for 12 months. Amex offers stack on top.",
    ),

    Strategy(
        name="Matched Betting (intro offers)",
        category="fixed_point",
        description="Mathematically lock in profit from bookmaker sign-up offers. Not gambling.",
        min_capital=50,
        expected_return="£500-1000 from intro offers",
        time_horizon="2-4 weeks",
        risk_level="none",
        effort="medium",
        skills_needed=["basic maths", "attention to detail"],
        platforms=["OddsMonkey", "Profit Accumulator"],
        notes="Completely legal. Uses free bets to guarantee profit regardless of outcome. Requires focus.",
    ),

    # ── MULTIPLICITIES (variable returns, higher potential) ──

    Strategy(
        name="Competition Entry Automation",
        category="multiplicity",
        description="Systematic entry into skill-based and prize draw competitions. Volume game.",
        min_capital=0,
        expected_return="£50-500/month (variable)",
        time_horizon="Ongoing",
        risk_level="low",
        effort="medium",
        skills_needed=["persistence", "basic writing"],
        platforms=["ThePrizeFinder", "Loquax", "Twitter/X comps", "Instagram comps"],
        notes="Skill-based comps (25 words or less) have much better odds. COMBOT can automate discovery.",
    ),

    Strategy(
        name="Freelance Micro-Tasks",
        category="multiplicity",
        description="Short technical tasks: code review, data labelling, writing, testing.",
        min_capital=0,
        expected_return="£10-50/hour",
        time_horizon="Immediate",
        risk_level="none",
        effort="active",
        skills_needed=["technical skills", "writing"],
        platforms=["Prolific", "UserTesting (£10/test)", "Appen", "Scale AI", "Fiverr"],
        notes="Prolific pays well for academic studies. UserTesting is £10 for 20 min.",
    ),

    Strategy(
        name="API Arbitrage / Data Services",
        category="multiplicity",
        description="Build micro-services that add value between APIs. Translation, enrichment, caching.",
        min_capital=10,
        expected_return="£100-1000/month",
        time_horizon="2-4 weeks to build",
        risk_level="low",
        effort="active",
        skills_needed=["programming", "API knowledge"],
        platforms=["RapidAPI", "AWS Marketplace", "Civo (for hosting)"],
        notes="You have the sovereign dispatch infrastructure already. Ship a useful API.",
    ),

    Strategy(
        name="Content Monetisation",
        category="multiplicity",
        description="Substack, YouTube, or blog monetisation from existing knowledge base.",
        min_capital=0,
        expected_return="£0-5000/month (builds over time)",
        time_horizon="3-6 months to meaningful revenue",
        risk_level="none",
        effort="active",
        skills_needed=["writing", "subject expertise"],
        platforms=["Substack", "YouTube", "Medium Partner Program", "Ghost"],
        notes="You have deep policy/tech knowledge. The Brunel Engine is a natural lead magnet.",
    ),

    Strategy(
        name="Invention Licensing",
        category="multiplicity",
        description="Use InventorForge to generate patentable inventions, license to manufacturers.",
        min_capital=0,
        expected_return="Royalties (variable, potentially significant)",
        time_horizon="6-12 months",
        risk_level="medium",
        effort="active",
        skills_needed=["creative thinking", "persistence"],
        platforms=["InventorForge (your own)", "InventRight", "Licensing Expo"],
        notes="The hex-inventions repo is already generating daily teardowns. Pipeline exists.",
    ),

    # ── RECURRING (steady drip) ──

    Strategy(
        name="Referral Programme Chains",
        category="recurring",
        description="Systematic referral across fintech apps. Each signup earns £5-50.",
        min_capital=0,
        expected_return="£5-50 per referral",
        time_horizon="Immediate per referral",
        risk_level="none",
        effort="low",
        platforms=["Trading 212 (free share)", "Freetrade", "Monzo", "Revolut", "Chase", "Chip"],
        notes="Share referral links through your network and content.",
    ),

    Strategy(
        name="Print on Demand / Digital Products",
        category="recurring",
        description="Design once, sell forever. T-shirts, stickers, digital templates, Notion templates.",
        min_capital=0,
        expected_return="£50-500/month passive once established",
        time_horizon="2-4 weeks to launch",
        risk_level="none",
        effort="medium",
        skills_needed=["design sense", "marketing"],
        platforms=["Redbubble", "Etsy", "Gumroad", "Printful"],
        notes="The psychic paper aesthetic is genuinely cool. Sell the vibe.",
    ),

    Strategy(
        name="Grant Applications",
        category="one_shot",
        description="UK grants for innovation, social enterprise, creative projects.",
        min_capital=0,
        expected_return="£1,000-50,000",
        time_horizon="1-3 months",
        risk_level="none",
        effort="active",
        skills_needed=["writing", "project planning"],
        platforms=["Innovate UK Smart Grants", "UnLtd", "Nesta", "Arts Council", "National Lottery Community Fund"],
        notes="InventorForge + TARDIS infrastructure is genuinely innovative. Write the applications.",
    ),
]


def filter_strategies(
    max_capital: float = 200,
    max_risk: str = "medium",
    categories: list[str] | None = None,
) -> list[Strategy]:
    """Filter strategies by what's available right now."""
    risk_order = {"none": 0, "low": 1, "medium": 2, "high": 3}
    max_risk_val = risk_order.get(max_risk, 2)

    results = []
    for s in STRATEGIES:
        if s.min_capital > max_capital:
            continue
        if risk_order.get(s.risk_level, 3) > max_risk_val:
            continue
        if categories and s.category not in categories:
            continue
        results.append(s)
    return results
