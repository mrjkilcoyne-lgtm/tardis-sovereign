"""Problem domain definitions.

Each domain knows its typical patterns, good follow-up questions,
common misconceptions, and solution categories. Cross-domain detection
identifies compound problems.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Domain:
    """A problem domain the interviewer recognises."""
    name: str
    slug: str
    description: str
    keywords: tuple[str, ...]
    typical_patterns: tuple[str, ...]
    follow_up_questions: tuple[str, ...]
    misconceptions: tuple[str, ...]
    solution_categories: tuple[str, ...]
    specialist_title: str  # who to refer to if it's beyond us


# ---------------------------------------------------------------------------
# Domain catalogue
# ---------------------------------------------------------------------------

TECHNOLOGY = Domain(
    name="Technology",
    slug="technology",
    description="Software, hardware, systems, and digital infrastructure",
    keywords=(
        "code", "software", "app", "website", "server", "database", "bug",
        "crash", "error", "deploy", "api", "computer", "laptop", "phone",
        "wifi", "network", "cloud", "hosting", "linux", "windows", "mac",
        "programming", "developer", "git", "docker", "kubernetes",
    ),
    typical_patterns=(
        "It worked before and now it doesn't",
        "I don't know which technology to choose",
        "It's too slow / too expensive / too complex",
        "I need to migrate from X to Y",
        "Security concern or breach",
    ),
    follow_up_questions=(
        "What changed recently? Updates, new code, new users?",
        "What does the error message actually say?",
        "Is this affecting everyone or just you?",
        "What's your deadline on this?",
        "What's your technical comfort level?",
    ),
    misconceptions=(
        "More technology solves technology problems",
        "The newest tool is always the best tool",
        "If it works on my machine it works everywhere",
        "Security can wait until later",
    ),
    solution_categories=(
        "debug_and_fix", "architecture_change", "tool_migration",
        "training_and_upskilling", "outsource_to_specialist",
    ),
    specialist_title="software engineer or IT consultant",
)

FINANCIAL = Domain(
    name="Financial",
    slug="financial",
    description="Money, budgets, debt, investment, and financial planning",
    keywords=(
        "money", "budget", "debt", "loan", "mortgage", "savings", "investment",
        "tax", "pension", "salary", "income", "expense", "credit", "bank",
        "interest", "rent", "afford", "cost", "price", "bill", "invoice",
        "cash flow", "profit", "loss", "revenue", "funding",
    ),
    typical_patterns=(
        "More going out than coming in",
        "Unexpected large expense",
        "Don't know where the money goes",
        "Need to make a major financial decision",
        "Debt spiralling",
    ),
    follow_up_questions=(
        "Roughly what are we talking about -- hundreds, thousands, tens of thousands?",
        "Is this a one-off or ongoing?",
        "Have you spoken to your bank about this?",
        "What's the timeline before this becomes critical?",
        "Are there other people financially dependent on you?",
    ),
    misconceptions=(
        "Earning more always solves money problems",
        "All debt is bad debt",
        "You need a lot of money to start investing",
        "Budgets are just for people who are struggling",
    ),
    solution_categories=(
        "budgeting", "debt_management", "income_increase",
        "financial_restructuring", "professional_advice",
    ),
    specialist_title="financial adviser (FCA-regulated)",
)

LEGAL = Domain(
    name="Legal",
    slug="legal",
    description="Law, contracts, disputes, rights, and compliance",
    keywords=(
        "legal", "law", "contract", "solicitor", "lawyer", "court", "sue",
        "rights", "dispute", "complaint", "regulation", "compliance",
        "employment law", "tenant", "landlord", "copyright", "patent",
        "liability", "negligence", "gdpr", "data protection", "terms",
    ),
    typical_patterns=(
        "Someone isn't honouring an agreement",
        "I don't know my rights",
        "I've received a legal threat",
        "I need a contract reviewed or created",
        "Regulatory compliance question",
    ),
    follow_up_questions=(
        "Is there anything in writing -- emails, contracts, messages?",
        "What jurisdiction are we in?",
        "Have you already spoken to a solicitor?",
        "What's the monetary value at stake?",
        "Are there any deadlines or limitation periods approaching?",
    ),
    misconceptions=(
        "Being morally right means being legally right",
        "Verbal agreements aren't binding",
        "You always need a solicitor for everything",
        "The law is the same everywhere in the UK",
    ),
    solution_categories=(
        "self_help_legal", "mediation", "citizens_advice",
        "solicitor_referral", "regulatory_complaint",
    ),
    specialist_title="solicitor or legal adviser",
)

CAREER = Domain(
    name="Career",
    slug="career",
    description="Jobs, career direction, workplace problems, professional development",
    keywords=(
        "job", "career", "work", "boss", "manager", "promotion", "fired",
        "redundant", "interview", "cv", "resume", "salary", "raise",
        "colleague", "workplace", "profession", "skill", "qualification",
        "freelance", "self-employed", "unemployed", "career change",
    ),
    typical_patterns=(
        "Stuck and not progressing",
        "Toxic workplace or bad management",
        "Want to change direction entirely",
        "Can't get interviews / can't convert interviews",
        "Work-life balance has collapsed",
    ),
    follow_up_questions=(
        "How long have you been in this role / situation?",
        "What did you actually enjoy doing, at any point?",
        "Is this about money, meaning, or both?",
        "What would you do if money wasn't a factor?",
        "What's stopping you from making a change right now?",
    ),
    misconceptions=(
        "You need to have it all figured out",
        "Changing careers means starting from zero",
        "Passion always pays the bills",
        "Loyalty to one company is always rewarded",
    ),
    solution_categories=(
        "cv_and_applications", "networking", "upskilling",
        "career_pivot_plan", "workplace_negotiation", "coaching",
    ),
    specialist_title="career coach or recruitment consultant",
)

CREATIVE = Domain(
    name="Creative",
    slug="creative",
    description="Design, art, writing, music, creative projects and blocks",
    keywords=(
        "design", "art", "write", "writing", "music", "creative", "brand",
        "logo", "film", "video", "photography", "portfolio", "publish",
        "editor", "gallery", "commission", "illustration", "animation",
        "ux", "ui", "content", "blog", "novel", "script", "podcast",
    ),
    typical_patterns=(
        "Creative block -- can't start or can't finish",
        "Don't know how to get my work out there",
        "Client wants changes that ruin the work",
        "Can't make creative work pay",
        "Comparing myself to others and freezing",
    ),
    follow_up_questions=(
        "What's the project, specifically?",
        "Is this for you or for a client/audience?",
        "Where are you stuck -- the idea, the execution, or the release?",
        "What's your creative background?",
        "What does done look like for this?",
    ),
    misconceptions=(
        "Inspiration has to strike before you can work",
        "Good work sells itself",
        "You need expensive tools to make good things",
        "Creative people shouldn't think about money",
    ),
    solution_categories=(
        "creative_process", "tools_and_resources", "audience_building",
        "monetisation", "collaboration", "professional_development",
    ),
    specialist_title="creative mentor or industry professional",
)

WELLBEING = Domain(
    name="Wellbeing",
    slug="wellbeing",
    description="Mental health, physical health, stress, burnout, and self-care",
    keywords=(
        "stress", "anxiety", "depression", "burnout", "sleep", "health",
        "tired", "exhausted", "overwhelmed", "therapy", "counselling",
        "mental health", "panic", "worry", "lonely", "isolated",
        "exercise", "diet", "weight", "pain", "chronic", "addiction",
        "drink", "smoking", "self-care", "wellbeing", "wellness",
    ),
    typical_patterns=(
        "Everything feels too much",
        "Physical symptoms with no clear cause",
        "Can't switch off",
        "Avoiding things I know I should do",
        "Feeling disconnected from everything",
    ),
    follow_up_questions=(
        "How long have you been feeling like this?",
        "Is there a specific trigger, or is it more general?",
        "Are you sleeping and eating reasonably?",
        "Have you spoken to your GP about this?",
        "Do you have people around you who know what's going on?",
    ),
    misconceptions=(
        "You should be able to handle it on your own",
        "Asking for help is weakness",
        "It's just stress, it'll pass",
        "Other people have it worse, so I shouldn't complain",
    ),
    solution_categories=(
        "self_care_basics", "professional_support", "lifestyle_change",
        "community_and_connection", "crisis_resources",
    ),
    specialist_title="GP, therapist, or counsellor",
)

BUSINESS = Domain(
    name="Business",
    slug="business",
    description="Starting, running, growing, or fixing a business",
    keywords=(
        "business", "startup", "company", "founder", "entrepreneur",
        "customer", "client", "market", "product", "service", "sales",
        "marketing", "growth", "scale", "hire", "team", "partner",
        "investor", "pitch", "revenue", "profit", "strategy", "plan",
    ),
    typical_patterns=(
        "Good idea, no idea how to start",
        "Growing but breaking at the seams",
        "Sales have plateaued or dropped",
        "Co-founder or partnership conflict",
        "Need funding but don't know the landscape",
    ),
    follow_up_questions=(
        "What stage is the business at?",
        "What's your revenue situation?",
        "Who are your customers, specifically?",
        "What's the one thing that would change everything?",
        "How many people are involved?",
    ),
    misconceptions=(
        "Build it and they will come",
        "You need funding to start",
        "More features means better product",
        "Growth solves all problems",
    ),
    solution_categories=(
        "validation", "go_to_market", "operations",
        "funding_and_finance", "team_and_culture", "strategy",
    ),
    specialist_title="business adviser or mentor",
)

HOUSING = Domain(
    name="Housing",
    slug="housing",
    description="Renting, buying, repairs, neighbours, and accommodation",
    keywords=(
        "house", "flat", "rent", "landlord", "tenant", "mortgage", "move",
        "repair", "damp", "mould", "heating", "council", "housing",
        "neighbour", "noise", "lease", "deposit", "eviction", "homeless",
        "property", "estate agent", "surveyor", "planning permission",
    ),
    typical_patterns=(
        "Landlord won't fix something",
        "Can't afford to stay, can't afford to move",
        "Neighbour dispute",
        "Buying process has gone wrong",
        "Need to find somewhere to live urgently",
    ),
    follow_up_questions=(
        "Are you renting or do you own?",
        "How long have you been at this address?",
        "Is there a tenancy agreement or contract?",
        "Have you put the complaint in writing?",
        "Is anyone's health or safety at risk?",
    ),
    misconceptions=(
        "Landlords can do whatever they want",
        "You have to accept poor conditions",
        "Buying is always better than renting",
        "The council will sort it quickly",
    ),
    solution_categories=(
        "tenant_rights", "landlord_communication", "council_and_local_authority",
        "legal_action", "alternative_housing", "buying_guidance",
    ),
    specialist_title="housing adviser or solicitor",
)

EDUCATION = Domain(
    name="Education",
    slug="education",
    description="Learning, courses, qualifications, schools, and self-improvement",
    keywords=(
        "course", "university", "college", "school", "degree", "learn",
        "study", "exam", "qualification", "training", "teacher", "student",
        "tuition", "scholarship", "apprenticeship", "masters", "phd",
        "homework", "grades", "research", "tutor", "education",
    ),
    typical_patterns=(
        "Don't know what to study",
        "Struggling with coursework or exams",
        "Is this qualification worth the money?",
        "Want to learn but can't afford formal education",
        "Considering going back to education",
    ),
    follow_up_questions=(
        "What are you trying to achieve with this education?",
        "What's your current situation -- working, studying, or neither?",
        "What's your budget for this?",
        "How do you learn best?",
        "What's your timeline?",
    ),
    misconceptions=(
        "A degree is the only path to a good career",
        "Online courses aren't real education",
        "You're too old to go back to learning",
        "More qualifications always means better prospects",
    ),
    solution_categories=(
        "formal_education", "online_learning", "self_directed",
        "apprenticeships", "funding_and_grants", "career_alignment",
    ),
    specialist_title="career adviser or education consultant",
)

RELATIONSHIPS = Domain(
    name="Relationships",
    slug="relationships",
    description="Family, friends, partners, and interpersonal dynamics",
    keywords=(
        "relationship", "partner", "spouse", "husband", "wife", "boyfriend",
        "girlfriend", "family", "parent", "child", "friend", "argument",
        "communication", "trust", "boundary", "divorce", "separation",
        "dating", "conflict", "toxic", "narcissist", "support",
    ),
    typical_patterns=(
        "Communication has broken down",
        "Boundary violations",
        "Considering ending a relationship",
        "Family pressure or expectations",
        "Feeling taken for granted",
    ),
    follow_up_questions=(
        "Who are the people involved?",
        "How long has this dynamic been going on?",
        "Have you tried talking to them about it directly?",
        "Is anyone in this situation unsafe?",
        "What would a good outcome look like for you?",
    ),
    misconceptions=(
        "If you love someone enough, it'll work out",
        "Other people should just know what you need",
        "Ending a relationship means failure",
        "Family always comes first, no matter what",
    ),
    solution_categories=(
        "communication_strategies", "boundary_setting", "couples_therapy",
        "family_mediation", "self_reflection", "separation_support",
    ),
    specialist_title="therapist or relationship counsellor",
)

# ---------------------------------------------------------------------------
# Domain registry
# ---------------------------------------------------------------------------

ALL_DOMAINS: dict[str, Domain] = {
    d.slug: d for d in [
        TECHNOLOGY, FINANCIAL, LEGAL, CAREER, CREATIVE,
        WELLBEING, BUSINESS, HOUSING, EDUCATION, RELATIONSHIPS,
    ]
}


def detect_domains(text: str, top_n: int = 3) -> list[tuple[Domain, float]]:
    """Score text against all domains by keyword overlap. Returns sorted list."""
    lower = text.lower()
    scores: list[tuple[Domain, float]] = []

    for domain in ALL_DOMAINS.values():
        hits = sum(1 for kw in domain.keywords if kw in lower)
        if hits > 0:
            score = hits / len(domain.keywords)
            scores.append((domain, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


# ---------------------------------------------------------------------------
# Cross-domain detection
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CrossDomain:
    """When two domains collide, it's usually a specific kind of problem."""
    domain_a: str
    domain_b: str
    label: str
    description: str
    specialist_title: str


CROSS_DOMAINS: list[CrossDomain] = [
    CrossDomain("financial", "housing", "mortgage_or_rent",
                "Financial pressure related to housing costs",
                "mortgage adviser or housing charity"),
    CrossDomain("technology", "business", "startup_or_digital_business",
                "Building or running a technology business",
                "startup mentor or CTO-for-hire"),
    CrossDomain("career", "wellbeing", "burnout_or_work_stress",
                "Work is damaging health and wellbeing",
                "occupational therapist or career coach"),
    CrossDomain("legal", "housing", "tenant_rights_or_property_dispute",
                "Legal issues around property and tenancy",
                "housing solicitor"),
    CrossDomain("financial", "legal", "debt_or_contractual_dispute",
                "Financial obligations with legal dimensions",
                "debt adviser (e.g. StepChange) or solicitor"),
    CrossDomain("relationships", "wellbeing", "emotional_crisis",
                "Relationship problems affecting mental health",
                "therapist or counsellor"),
    CrossDomain("career", "education", "career_development",
                "Needing qualifications or skills for career progression",
                "career development adviser"),
    CrossDomain("creative", "business", "creative_business",
                "Making a creative practice commercially viable",
                "creative industries adviser"),
    CrossDomain("legal", "career", "employment_dispute",
                "Workplace legal issues like unfair dismissal or discrimination",
                "employment solicitor or ACAS"),
    CrossDomain("financial", "career", "income_and_career",
                "Career decisions driven by financial pressure",
                "financial coach with career expertise"),
]


def detect_cross_domain(
    domains: list[tuple[Domain, float]],
    threshold: float = 0.01,
) -> CrossDomain | None:
    """Check if the top domains form a known cross-domain pattern."""
    if len(domains) < 2:
        return None

    active = {d.slug for d, score in domains if score >= threshold}

    for cd in CROSS_DOMAINS:
        if cd.domain_a in active and cd.domain_b in active:
            return cd

    return None
