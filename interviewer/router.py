"""Solution router.

Takes a diagnosed problem and routes to actionable solutions.
Each solution has real-world detail: what to do, what it costs,
how long it takes, and how confident we are.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .domains import Domain, CrossDomain


class SolutionType(Enum):
    DIY = "diy"
    PRODUCT_SERVICE = "product_service"
    PROFESSIONAL_REFERRAL = "professional_referral"
    COMMUNITY_PEER = "community_peer"
    TOOL_RESOURCE = "tool_resource"
    BESPOKE_DESIGN = "bespoke_design"


class Difficulty(Enum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class Solution:
    """A single actionable solution."""
    solution_type: SolutionType
    title: str
    description: str
    steps: list[str] = field(default_factory=list)
    estimated_cost: str = "Free"        # "Free", "< GBP50", "GBP500-2000", etc.
    estimated_time: str = "< 1 hour"    # "< 1 hour", "1-3 days", "2-4 weeks"
    difficulty: Difficulty = Difficulty.MODERATE
    confidence: float = 0.7             # 0.0 to 1.0
    resources: list[str] = field(default_factory=list)  # URLs, book titles, org names
    caveats: list[str] = field(default_factory=list)
    needs_specialist: bool = False
    specialist_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.solution_type.value,
            "title": self.title,
            "description": self.description,
            "steps": self.steps,
            "estimated_cost": self.estimated_cost,
            "estimated_time": self.estimated_time,
            "difficulty": self.difficulty.value,
            "confidence": self.confidence,
            "resources": self.resources,
            "caveats": self.caveats,
            "needs_specialist": self.needs_specialist,
            "specialist_type": self.specialist_type,
        }


@dataclass
class Pathways:
    """Three pathways from problem to resolution."""
    quick_win: Solution | None = None
    structural_fix: Solution | None = None
    adaptation: Solution | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.quick_win:
            result["quick_win"] = self.quick_win.to_dict()
        if self.structural_fix:
            result["structural_fix"] = self.structural_fix.to_dict()
        if self.adaptation:
            result["adaptation"] = self.adaptation.to_dict()
        return result


# ---------------------------------------------------------------------------
# Solution templates per domain
# ---------------------------------------------------------------------------

# These are starting-point templates. The router selects and customises them
# based on the specific problem diagnosed.

_DOMAIN_SOLUTIONS: dict[str, dict[str, list[Solution]]] = {
    "technology": {
        "quick_win": [
            Solution(
                SolutionType.DIY, "Search and fix",
                "Look up the specific error message and apply the known fix.",
                steps=["Copy the exact error message", "Search with quotes", "Check Stack Overflow and GitHub issues",
                       "Apply the fix in a test environment first", "Verify it works"],
                estimated_cost="Free", estimated_time="1-3 hours", difficulty=Difficulty.EASY, confidence=0.6,
            ),
            Solution(
                SolutionType.TOOL_RESOURCE, "Use a diagnostic tool",
                "Run built-in diagnostics or a well-known tool to pinpoint the issue.",
                steps=["Identify the right diagnostic tool", "Run it", "Read the output carefully",
                       "Address what it flags"],
                estimated_cost="Free", estimated_time="< 1 hour", difficulty=Difficulty.MODERATE, confidence=0.65,
            ),
        ],
        "structural_fix": [
            Solution(
                SolutionType.DIY, "Refactor or rebuild the affected component",
                "If the problem keeps recurring, the architecture needs attention.",
                steps=["Map what depends on the broken part", "Design a cleaner approach",
                       "Build it alongside the old version", "Migrate gradually", "Remove the old version"],
                estimated_cost="Free (your time)", estimated_time="1-4 weeks",
                difficulty=Difficulty.HARD, confidence=0.7,
            ),
            Solution(
                SolutionType.PROFESSIONAL_REFERRAL, "Hire a specialist",
                "Some tech problems need someone who's solved this exact thing before.",
                estimated_cost="GBP 500-5,000", estimated_time="1-2 weeks",
                difficulty=Difficulty.EASY, confidence=0.8,
                needs_specialist=True, specialist_type="software engineer or IT consultant",
            ),
        ],
        "adaptation": [
            Solution(
                SolutionType.TOOL_RESOURCE, "Switch to a managed service",
                "If maintaining it is the problem, let someone else maintain it.",
                estimated_cost="GBP 10-200/month", estimated_time="1-2 weeks",
                difficulty=Difficulty.MODERATE, confidence=0.7,
            ),
        ],
    },
    "financial": {
        "quick_win": [
            Solution(
                SolutionType.DIY, "The 48-hour money audit",
                "Track every penny for 48 hours. Most people find the leak quickly.",
                steps=["Note every transaction for 48 hours", "Categorise: need, want, forgot-about",
                       "Cancel the forgot-abouts immediately", "Set a review date for the wants"],
                estimated_cost="Free", estimated_time="48 hours", difficulty=Difficulty.EASY, confidence=0.7,
            ),
        ],
        "structural_fix": [
            Solution(
                SolutionType.DIY, "Build a real budget",
                "Not a spreadsheet you'll ignore. A system that works with your habits.",
                steps=["List fixed outgoings", "Set a weekly spending limit for everything else",
                       "Use a separate account or prepaid card for spending money",
                       "Review weekly for the first month, then monthly"],
                estimated_cost="Free", estimated_time="2-3 hours setup, then ongoing",
                difficulty=Difficulty.MODERATE, confidence=0.75,
            ),
            Solution(
                SolutionType.PROFESSIONAL_REFERRAL, "See a financial adviser",
                "For complex situations (debt, investment, pensions), professional advice pays for itself.",
                estimated_cost="GBP 100-500 initial consultation", estimated_time="1-2 weeks to arrange",
                difficulty=Difficulty.EASY, confidence=0.85,
                needs_specialist=True, specialist_type="financial adviser (FCA-regulated)",
                resources=["MoneyHelper (free government service)", "StepChange (free debt advice)",
                           "Citizens Advice Bureau"],
            ),
        ],
        "adaptation": [
            Solution(
                SolutionType.COMMUNITY_PEER, "Find peer support",
                "Money problems are common. Forums and groups help with both knowledge and motivation.",
                estimated_cost="Free", estimated_time="Ongoing",
                difficulty=Difficulty.EASY, confidence=0.5,
                resources=["r/UKPersonalFinance", "MoneySavingExpert forums"],
            ),
        ],
    },
    "legal": {
        "quick_win": [
            Solution(
                SolutionType.TOOL_RESOURCE, "Know your rights first",
                "Before doing anything else, understand the legal position. Many issues resolve once you do.",
                steps=["Look up the specific issue on Citizens Advice", "Read the relevant legislation summary",
                       "Write down the key facts and dates", "Draft a clear, factual letter"],
                estimated_cost="Free", estimated_time="2-4 hours", difficulty=Difficulty.MODERATE, confidence=0.6,
                resources=["Citizens Advice (citizensadvice.org.uk)", "Gov.uk guidance pages"],
            ),
        ],
        "structural_fix": [
            Solution(
                SolutionType.PROFESSIONAL_REFERRAL, "Consult a solicitor",
                "Legal problems often need legal solutions. Many offer free initial consultations.",
                estimated_cost="Free initial consultation, then GBP 150-350/hour",
                estimated_time="1-2 weeks to arrange",
                difficulty=Difficulty.EASY, confidence=0.85,
                needs_specialist=True, specialist_type="solicitor",
                resources=["Law Society Find a Solicitor", "Legal Aid (if eligible)"],
            ),
        ],
        "adaptation": [
            Solution(
                SolutionType.COMMUNITY_PEER, "Mediation",
                "If both parties are willing, mediation is cheaper, faster, and less adversarial than court.",
                estimated_cost="GBP 50-300 per session", estimated_time="1-3 sessions",
                difficulty=Difficulty.MODERATE, confidence=0.6,
            ),
        ],
    },
}

# Default templates for domains without specific solutions
_DEFAULT_SOLUTIONS: dict[str, list[Solution]] = {
    "quick_win": [
        Solution(
            SolutionType.DIY, "Research and first steps",
            "Spend a focused hour understanding the landscape before taking action.",
            steps=["Define the problem in one sentence", "Search for others who've had the same issue",
                   "List three possible next steps", "Do the easiest one today"],
            estimated_cost="Free", estimated_time="1-2 hours", difficulty=Difficulty.EASY, confidence=0.5,
        ),
    ],
    "structural_fix": [
        Solution(
            SolutionType.PROFESSIONAL_REFERRAL, "Get expert guidance",
            "This is a situation where the right professional saves you time, money, and stress.",
            estimated_cost="Varies", estimated_time="1-2 weeks to arrange",
            difficulty=Difficulty.EASY, confidence=0.7,
            needs_specialist=True,
        ),
    ],
    "adaptation": [
        Solution(
            SolutionType.COMMUNITY_PEER, "Find your people",
            "Others have been through this. Their experience is invaluable.",
            estimated_cost="Free", estimated_time="Ongoing",
            difficulty=Difficulty.EASY, confidence=0.5,
        ),
    ],
}


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

def route(
    domain: Domain,
    problem_summary: str,
    cross_domain: CrossDomain | None = None,
    severity: float = 0.5,
) -> Pathways:
    """Route a diagnosed problem to actionable solutions.

    Args:
        domain: The primary problem domain.
        problem_summary: One-line summary of the diagnosed problem.
        cross_domain: Optional cross-domain pattern detected.
        severity: 0.0 (minor) to 1.0 (critical).

    Returns:
        Pathways with quick_win, structural_fix, and adaptation.
    """
    slug = domain.slug
    domain_solutions = _DOMAIN_SOLUTIONS.get(slug, {})

    def pick(category: str) -> Solution | None:
        options = domain_solutions.get(category, _DEFAULT_SOLUTIONS.get(category, []))
        if not options:
            return None
        # Pick highest-confidence option
        best = max(options, key=lambda s: s.confidence)
        # Customize specialist type from domain if needed
        if best.needs_specialist and not best.specialist_type:
            best.specialist_type = domain.specialist_title
        return best

    pathways = Pathways(
        quick_win=pick("quick_win"),
        structural_fix=pick("structural_fix"),
        adaptation=pick("adaptation"),
    )

    # Adjust for severity
    if severity > 0.8 and pathways.structural_fix:
        pathways.structural_fix.confidence = min(1.0, pathways.structural_fix.confidence + 0.1)

    # Add cross-domain specialist if detected
    if cross_domain and pathways.structural_fix:
        pathways.structural_fix.specialist_type = cross_domain.specialist_title
        pathways.structural_fix.needs_specialist = True

    return pathways


def needs_human(pathways: Pathways) -> bool:
    """Check if any pathway flags a human specialist."""
    for sol in [pathways.quick_win, pathways.structural_fix, pathways.adaptation]:
        if sol and sol.needs_specialist:
            return True
    return False
