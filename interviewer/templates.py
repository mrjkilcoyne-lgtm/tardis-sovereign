"""Output templates.

Clean, readable formats for interview results.
The report should feel like it was written by someone who genuinely listened.
"""

from __future__ import annotations

import json
import textwrap
from typing import Any

from .conversation import InterviewResult


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def to_markdown(result: InterviewResult) -> str:
    """Full markdown report. Thorough but readable."""
    lines: list[str] = []

    lines.append("# Interview Report")
    lines.append("")
    lines.append(f"**Domain:** {result.primary_domain.replace('_', ' ').title()}")
    if result.secondary_domains:
        secondary = ", ".join(d.replace("_", " ").title() for d in result.secondary_domains)
        lines.append(f"**Also involves:** {secondary}")
    if result.cross_domain:
        lines.append(f"**Cross-domain pattern:** {result.cross_domain.replace('_', ' ').title()}")
    lines.append(f"**Confidence:** {result.confidence_score:.0%}")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## What You Told Me")
    lines.append("")
    lines.append(result.summary)
    lines.append("")

    # Diagnosis
    lines.append("## What I Think Is Going On")
    lines.append("")
    lines.append(result.diagnosis)
    lines.append("")

    # Pathways
    lines.append("## What I'd Recommend")
    lines.append("")

    pathways = result.pathways
    if pathways.get("quick_win"):
        qw = pathways["quick_win"]
        lines.append("### The Quick Win")
        lines.append("")
        lines.append(f"**{qw['title']}**")
        lines.append("")
        lines.append(qw["description"])
        lines.append("")
        if qw.get("steps"):
            for i, step in enumerate(qw["steps"], 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        lines.append(f"- **Cost:** {qw['estimated_cost']}")
        lines.append(f"- **Time:** {qw['estimated_time']}")
        lines.append(f"- **Difficulty:** {qw['difficulty'].title()}")
        lines.append("")

    if pathways.get("structural_fix"):
        sf = pathways["structural_fix"]
        lines.append("### The Structural Fix")
        lines.append("")
        lines.append(f"**{sf['title']}**")
        lines.append("")
        lines.append(sf["description"])
        lines.append("")
        if sf.get("steps"):
            for i, step in enumerate(sf["steps"], 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        lines.append(f"- **Cost:** {sf['estimated_cost']}")
        lines.append(f"- **Time:** {sf['estimated_time']}")
        lines.append(f"- **Difficulty:** {sf['difficulty'].title()}")
        lines.append("")

    if pathways.get("adaptation"):
        ad = pathways["adaptation"]
        lines.append("### If You Need to Live With It For Now")
        lines.append("")
        lines.append(f"**{ad['title']}**")
        lines.append("")
        lines.append(ad["description"])
        lines.append("")
        lines.append(f"- **Cost:** {ad['estimated_cost']}")
        lines.append(f"- **Time:** {ad['estimated_time']}")
        lines.append("")

    # Specialist flag
    if result.needs_specialist:
        lines.append("---")
        lines.append("")
        lines.append("### A Note on Professional Help")
        lines.append("")
        lines.append(
            f"I'd genuinely recommend speaking to a **{result.specialist_type}** "
            f"about this. Not because the situation is hopeless -- because it's "
            f"important enough to get right."
        )
        lines.append("")

    # Recommended actions summary
    if result.recommended_actions:
        lines.append("---")
        lines.append("")
        lines.append("## Your Next Steps")
        lines.append("")
        for action in result.recommended_actions:
            lines.append(f"- [ ] {action}")
        lines.append("")

    # Conversation log
    if result.raw_exchanges:
        lines.append("---")
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>Full Conversation</summary>")
        lines.append("")
        for ex in result.raw_exchanges:
            lines.append(f"**You:** {ex['user']}")
            lines.append("")
            lines.append(f"**Interviewer:** {ex['interviewer']}")
            lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def to_json(result: InterviewResult, pretty: bool = True) -> str:
    """Structured JSON output."""
    indent = 2 if pretty else None
    return json.dumps(result.to_dict(), indent=indent, ensure_ascii=False)


# ---------------------------------------------------------------------------
# One-page summary
# ---------------------------------------------------------------------------

def to_one_page(result: InterviewResult) -> str:
    """A concise, one-page text summary. No markdown, just clean text."""
    lines: list[str] = []
    sep = "=" * 60

    lines.append(sep)
    lines.append("INTERVIEW SUMMARY")
    lines.append(sep)
    lines.append("")

    lines.append(f"Domain:     {result.primary_domain.replace('_', ' ').title()}")
    lines.append(f"Confidence: {result.confidence_score:.0%}")
    if result.needs_specialist:
        lines.append(f"Specialist:  Recommended ({result.specialist_type})")
    lines.append("")

    lines.append("SITUATION")
    lines.append("-" * 40)
    lines.append(textwrap.fill(result.summary, width=60))
    lines.append("")

    lines.append("DIAGNOSIS")
    lines.append("-" * 40)
    lines.append(textwrap.fill(result.diagnosis, width=60))
    lines.append("")

    lines.append("RECOMMENDED ACTIONS")
    lines.append("-" * 40)
    for i, action in enumerate(result.recommended_actions, 1):
        lines.append(textwrap.fill(f"{i}. {action}", width=60, subsequent_indent="   "))
    lines.append("")

    lines.append(sep)
    lines.append(f"Based on {result.exchange_count} exchanges.")
    lines.append(sep)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML report (for web interface)
# ---------------------------------------------------------------------------

def to_html_report(result: InterviewResult) -> str:
    """HTML-formatted report for the web interface."""
    pathways = result.pathways

    def solution_card(title: str, data: dict[str, Any]) -> str:
        if not data:
            return ""
        steps_html = ""
        if data.get("steps"):
            steps_li = "".join(f"<li>{s}</li>" for s in data["steps"])
            steps_html = f"<ol>{steps_li}</ol>"
        return f"""
        <div class="solution-card">
            <h3>{title}</h3>
            <h4>{data['title']}</h4>
            <p>{data['description']}</p>
            {steps_html}
            <div class="meta">
                <span class="tag">Cost: {data['estimated_cost']}</span>
                <span class="tag">Time: {data['estimated_time']}</span>
                <span class="tag">Difficulty: {data['difficulty'].title()}</span>
            </div>
        </div>
        """

    specialist_html = ""
    if result.needs_specialist:
        specialist_html = f"""
        <div class="specialist-note">
            <strong>Professional help recommended:</strong> I'd suggest speaking to a
            <strong>{result.specialist_type}</strong> about this.
            Not because it's hopeless -- because it's important enough to get right.
        </div>
        """

    actions_html = ""
    if result.recommended_actions:
        actions_li = "".join(f"<li>{a}</li>" for a in result.recommended_actions)
        actions_html = f"""
        <div class="actions">
            <h3>Your Next Steps</h3>
            <ul>{actions_li}</ul>
        </div>
        """

    return f"""
    <div class="interview-report">
        <div class="report-header">
            <h2>Interview Report</h2>
            <div class="meta-bar">
                <span class="domain-tag">{result.primary_domain.replace('_', ' ').title()}</span>
                <span class="confidence">Confidence: {result.confidence_score:.0%}</span>
            </div>
        </div>

        <div class="section">
            <h3>What You Told Me</h3>
            <p>{result.summary}</p>
        </div>

        <div class="section">
            <h3>What I Think Is Going On</h3>
            <p>{result.diagnosis}</p>
        </div>

        <div class="section">
            <h3>What I'd Recommend</h3>
            {solution_card("The Quick Win", pathways.get("quick_win", {}))}
            {solution_card("The Structural Fix", pathways.get("structural_fix", {}))}
            {solution_card("If You Need to Live With It", pathways.get("adaptation", {}))}
        </div>

        {specialist_html}
        {actions_html}

        <div class="report-footer">
            Based on {result.exchange_count} exchanges.
        </div>
    </div>
    """
