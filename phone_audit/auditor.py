"""The Auditor. Reverse engineers your app stack and rebuilds it better.

Feed it a list of what's on your phone. It'll tell you what's
snooping, what's redundant, what's missing, and how to rebuild
the whole thing sleeker, faster, and sovereign.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime

from .alternatives import (
    KNOWN_SNOOPS, REPLACEMENTS, COMBINATIONS,
    AppProfile, Alternative,
)


@dataclass
class AppVerdict:
    """What the auditor thinks about one app."""
    app_name: str
    keep: bool
    reason: str
    privacy_score: int
    snooping_level: str
    replacement: Alternative | None = None
    data_at_risk: list[str] = field(default_factory=list)


@dataclass
class AuditReport:
    """The full audit. What to keep, kill, replace, and add."""
    generated_at: datetime = field(default_factory=datetime.now)
    total_apps: int = 0
    verdicts: list[AppVerdict] = field(default_factory=list)
    recommended_combinations: list[dict] = field(default_factory=list)
    missing_essentials: list[Alternative] = field(default_factory=list)
    privacy_score_before: float = 0.0
    privacy_score_after: float = 0.0
    monthly_savings: str = ""

    def to_markdown(self) -> str:
        lines = [
            "# Phone Audit Report",
            f"*Generated {self.generated_at.strftime('%d %B %Y')}*",
            f"*{self.total_apps} apps audited*",
            "",
            f"**Privacy Score: {self.privacy_score_before:.0f}/10 → {self.privacy_score_after:.0f}/10** (after recommendations)",
            "",
        ]

        # Snoops first
        snoops = [v for v in self.verdicts if v.snooping_level in ("hostile", "aggressive")]
        if snoops:
            lines.append("## Snoops (replace or blind these)")
            lines.append("")
            for v in snoops:
                lines.append(f"**{v.app_name}** — Snooping: {v.snooping_level} | Privacy: {v.privacy_score}/10")
                lines.append(f"  Data at risk: {', '.join(v.data_at_risk)}")
                if v.replacement:
                    lines.append(f"  → Replace with: **{v.replacement.name}** (privacy: {v.replacement.privacy_score}/10, {v.replacement.cost})")
                lines.append(f"  {v.reason}")
                lines.append("")

        # Keep
        keeps = [v for v in self.verdicts if v.keep and v.snooping_level not in ("hostile", "aggressive")]
        if keeps:
            lines.append("## Keep (these are fine)")
            lines.append("")
            for v in keeps:
                lines.append(f"- **{v.app_name}** — {v.reason}")
            lines.append("")

        # Replace
        replaces = [v for v in self.verdicts if not v.keep and v.replacement]
        if replaces:
            lines.append("## Replace")
            lines.append("")
            for v in replaces:
                lines.append(f"- **{v.app_name}** → **{v.replacement.name}** — {v.reason}")
            lines.append("")

        # Missing
        if self.missing_essentials:
            lines.append("## Add These (you're missing out)")
            lines.append("")
            for alt in self.missing_essentials:
                lines.append(f"**{alt.name}** ({alt.cost})")
                lines.append(f"  {', '.join(alt.power_features[:3])}")
                if alt.notes:
                    lines.append(f"  _{alt.notes}_")
                lines.append("")

        # Combinations
        if self.recommended_combinations:
            lines.append("## Power Combinations")
            lines.append("")
            for combo in self.recommended_combinations:
                lines.append(f"**{combo['name']}** ({combo['cost']})")
                lines.append(f"  Apps: {', '.join(combo['apps'])}")
                lines.append(f"  Replaces: {', '.join(combo['replaces'])}")
                lines.append(f"  _{combo['why']}_")
                lines.append("")

        return "\n".join(lines)


def audit_apps(app_names: list[str]) -> AuditReport:
    """Audit a list of app names and produce a full report.

    Args:
        app_names: List of app names (case-insensitive, partial match OK)
    """
    normalised = [_normalise(name) for name in app_names]
    report = AuditReport(total_apps=len(app_names))

    privacy_scores_before = []
    privacy_scores_after = []

    for raw, norm in zip(app_names, normalised):
        profile = KNOWN_SNOOPS.get(norm)
        replacement = _find_replacement(norm)

        if profile:
            verdict = AppVerdict(
                app_name=raw,
                keep=profile.snooping_level in ("none", "low"),
                reason=_verdict_reason(profile, replacement),
                privacy_score=profile.privacy_score,
                snooping_level=profile.snooping_level,
                replacement=replacement,
                data_at_risk=profile.data_collected,
            )
            privacy_scores_before.append(profile.privacy_score)
            privacy_scores_after.append(
                replacement.privacy_score if replacement else profile.privacy_score
            )
        else:
            # Unknown app - assume moderate
            verdict = AppVerdict(
                app_name=raw,
                keep=True,
                reason="Not in known snoop database. Probably fine, but review permissions.",
                privacy_score=5,
                snooping_level="unknown",
                replacement=replacement,
            )
            privacy_scores_before.append(5)
            privacy_scores_after.append(5)

        report.verdicts.append(verdict)

    # Missing essentials
    covered_categories = set()
    for norm in normalised:
        for alt in REPLACEMENTS:
            if norm in [r.lower().replace(" ", "_") for r in alt.replaces]:
                covered_categories.add(alt.category)

    essential_categories = {"messaging", "browser", "security", "email", "privacy"}
    missing = essential_categories - covered_categories
    for alt in REPLACEMENTS:
        if alt.category in missing and alt.privacy_score >= 9:
            if not any(m.name == alt.name for m in report.missing_essentials):
                report.missing_essentials.append(alt)

    # Combinations
    for combo in COMBINATIONS:
        relevance = sum(1 for app in combo["replaces"] if _normalise(app) in normalised)
        if relevance >= 1:
            report.recommended_combinations.append(combo)

    # Scores
    if privacy_scores_before:
        report.privacy_score_before = sum(privacy_scores_before) / len(privacy_scores_before)
        report.privacy_score_after = sum(privacy_scores_after) / len(privacy_scores_after)

    return report


def _normalise(name: str) -> str:
    """Normalise app name for matching."""
    return name.lower().strip().replace(" ", "_").replace("-", "_")


def _find_replacement(norm_name: str) -> Alternative | None:
    """Find the best privacy-respecting replacement."""
    for alt in REPLACEMENTS:
        normalised_replaces = [r.lower().replace(" ", "_") for r in alt.replaces]
        if norm_name in normalised_replaces:
            return alt
    return None


def _verdict_reason(profile: AppProfile, replacement: Alternative | None) -> str:
    """Generate a human-readable verdict."""
    if profile.snooping_level == "hostile":
        base = f"Actively hostile to your privacy. Collects {len(profile.data_collected)} data categories."
    elif profile.snooping_level == "aggressive":
        base = f"Aggressively tracks you. {len(profile.data_collected)} data categories harvested."
    elif profile.snooping_level == "moderate":
        base = f"Moderate tracking. Functional but could be replaced."
    else:
        base = "Acceptable privacy."

    if replacement:
        base += f" → {replacement.name} does the same job with privacy score {replacement.privacy_score}/10."

    return base
