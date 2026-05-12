"""Document type schemas. Each one knows its own shape, fields, and visual language.

Add new document types here. The psychic paper will learn them automatically.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DocumentField:
    """A single field on a document."""
    name: str               # internal key
    label: str              # display label
    required: bool = True
    auto_generate: bool = False  # system fills this in
    format: str = "text"    # text, date, number, barcode, qr, photo


@dataclass
class DocumentType:
    """A complete document template."""
    type_id: str            # unique key
    name: str               # human name
    category: str           # id, ticket, pass, licence, permit, card
    fields: list[DocumentField] = field(default_factory=list)
    color_primary: str = "#1a1a2e"
    color_accent: str = "#e94560"
    color_bg: str = "#ffffff"
    layout: str = "card"    # card, ticket, badge, full
    has_photo: bool = False
    has_barcode: bool = False
    has_qr: bool = True
    has_hologram: bool = False
    width_mm: int = 86      # ISO card default
    height_mm: int = 54
    # Context keywords that trigger this type
    context_keywords: list[str] = field(default_factory=list)


# ─── THE TEMPLATES ───────────────────────────────────────────────

DOCUMENT_TYPES: dict[str, DocumentType] = {}


def _register(doc: DocumentType):
    DOCUMENT_TYPES[doc.type_id] = doc
    return doc


# ── Press / Media Pass ──
_register(DocumentType(
    type_id="press_pass",
    name="Press Credentials",
    category="pass",
    layout="badge",
    color_primary="#1a1a2e",
    color_accent="#0f3460",
    color_bg="#f5f5f0",
    has_photo=True,
    has_barcode=True,
    height_mm=100,
    context_keywords=["press", "media", "journalist", "reporter", "conference", "briefing"],
    fields=[
        DocumentField("name", "Name"),
        DocumentField("title", "Title", required=False),
        DocumentField("org", "Organisation"),
        DocumentField("press_id", "Press ID", auto_generate=True),
        DocumentField("valid_date", "Valid", format="date"),
        DocumentField("zone", "Access Zone", required=False),
        DocumentField("photo", "Photo", format="photo", required=False),
    ],
))

# ── Event Ticket ──
_register(DocumentType(
    type_id="event_ticket",
    name="Event Ticket",
    category="ticket",
    layout="ticket",
    color_primary="#16213e",
    color_accent="#e94560",
    color_bg="#ffffff",
    has_qr=True,
    width_mm=180,
    height_mm=80,
    context_keywords=["event", "concert", "show", "gig", "festival", "theatre", "match", "game"],
    fields=[
        DocumentField("event_name", "Event"),
        DocumentField("venue", "Venue"),
        DocumentField("date", "Date", format="date"),
        DocumentField("time", "Time"),
        DocumentField("seat", "Seat / Area", required=False),
        DocumentField("ticket_type", "Type"),
        DocumentField("ticket_id", "Ticket #", auto_generate=True),
        DocumentField("holder", "Holder"),
    ],
))

# ── Boarding Pass ──
_register(DocumentType(
    type_id="boarding_pass",
    name="Boarding Pass",
    category="ticket",
    layout="ticket",
    color_primary="#0b0c10",
    color_accent="#66fcf1",
    color_bg="#f8f9fa",
    has_barcode=True,
    has_qr=True,
    width_mm=200,
    height_mm=90,
    context_keywords=["flight", "boarding", "airline", "airport", "travel", "gate", "departure"],
    fields=[
        DocumentField("passenger", "Passenger"),
        DocumentField("flight", "Flight"),
        DocumentField("from_city", "From"),
        DocumentField("to_city", "To"),
        DocumentField("date", "Date", format="date"),
        DocumentField("gate", "Gate"),
        DocumentField("seat", "Seat"),
        DocumentField("boarding_time", "Boarding"),
        DocumentField("class_type", "Class"),
        DocumentField("booking_ref", "Booking Ref", auto_generate=True),
    ],
))

# ── Driving Licence ──
_register(DocumentType(
    type_id="driving_licence",
    name="Driving Licence",
    category="licence",
    layout="card",
    color_primary="#003078",
    color_accent="#d4351c",
    color_bg="#ffffff",
    has_photo=True,
    has_hologram=True,
    context_keywords=["driving", "licence", "license", "drive", "vehicle", "car", "road"],
    fields=[
        DocumentField("surname", "Surname"),
        DocumentField("forenames", "Forenames"),
        DocumentField("dob", "Date of Birth", format="date"),
        DocumentField("issue_date", "Issue Date", format="date"),
        DocumentField("expiry_date", "Expiry Date", format="date"),
        DocumentField("licence_number", "Licence No.", auto_generate=True),
        DocumentField("address", "Address"),
        DocumentField("categories", "Categories"),
        DocumentField("photo", "Photo", format="photo", required=False),
    ],
))

# ── Membership Card ──
_register(DocumentType(
    type_id="membership",
    name="Membership Card",
    category="card",
    layout="card",
    color_primary="#2d2d2d",
    color_accent="#c9a84c",
    color_bg="#1a1a1a",
    has_qr=True,
    context_keywords=["member", "membership", "club", "gym", "library", "society", "association"],
    fields=[
        DocumentField("name", "Member"),
        DocumentField("member_id", "Member ID", auto_generate=True),
        DocumentField("org", "Organisation"),
        DocumentField("tier", "Tier", required=False),
        DocumentField("since", "Member Since", format="date"),
        DocumentField("expiry", "Valid Until", format="date"),
    ],
))

# ── Security / Access Badge ──
_register(DocumentType(
    type_id="security_badge",
    name="Security Clearance",
    category="pass",
    layout="badge",
    color_primary="#1b1b2f",
    color_accent="#e43f5a",
    color_bg="#f0f0f0",
    has_photo=True,
    has_hologram=True,
    has_barcode=True,
    height_mm=100,
    context_keywords=["security", "clearance", "access", "restricted", "authorised", "classified", "facility"],
    fields=[
        DocumentField("name", "Name"),
        DocumentField("clearance_level", "Clearance"),
        DocumentField("department", "Department"),
        DocumentField("badge_id", "Badge ID", auto_generate=True),
        DocumentField("issue_date", "Issued", format="date"),
        DocumentField("expiry_date", "Expires", format="date"),
        DocumentField("photo", "Photo", format="photo", required=False),
    ],
))

# ── Transport Pass ──
_register(DocumentType(
    type_id="transport_pass",
    name="Transport Pass",
    category="pass",
    layout="card",
    color_primary="#003078",
    color_accent="#e21836",
    color_bg="#ffffff",
    has_photo=True,
    has_qr=True,
    context_keywords=["transport", "bus", "train", "tube", "metro", "oyster", "rail", "transit"],
    fields=[
        DocumentField("name", "Holder"),
        DocumentField("pass_type", "Pass Type"),
        DocumentField("zones", "Zones"),
        DocumentField("valid_from", "Valid From", format="date"),
        DocumentField("valid_to", "Valid To", format="date"),
        DocumentField("pass_id", "Pass No.", auto_generate=True),
        DocumentField("photo", "Photo", format="photo", required=False),
    ],
))

# ── Conference / Delegate Badge ──
_register(DocumentType(
    type_id="conference_badge",
    name="Conference Badge",
    category="pass",
    layout="badge",
    color_primary="#2c3e50",
    color_accent="#3498db",
    color_bg="#ecf0f1",
    has_qr=True,
    height_mm=120,
    context_keywords=["conference", "delegate", "summit", "symposium", "workshop", "seminar", "keynote", "speaker"],
    fields=[
        DocumentField("name", "Name"),
        DocumentField("title", "Title", required=False),
        DocumentField("org", "Organisation"),
        DocumentField("role", "Role"),  # Speaker, Delegate, VIP, Organiser
        DocumentField("event_name", "Event"),
        DocumentField("date", "Date", format="date"),
        DocumentField("badge_id", "Badge #", auto_generate=True),
    ],
))

# ── Permit / Authorization ──
_register(DocumentType(
    type_id="permit",
    name="Permit",
    category="permit",
    layout="full",
    color_primary="#1a472a",
    color_accent="#2a623d",
    color_bg="#fefef9",
    has_qr=True,
    has_hologram=True,
    width_mm=210,
    height_mm=148,  # A5ish
    context_keywords=["permit", "permission", "authorisation", "authorization", "approved", "granted", "licence"],
    fields=[
        DocumentField("holder", "Issued To"),
        DocumentField("permit_type", "Permit Type"),
        DocumentField("description", "Description"),
        DocumentField("issuing_authority", "Issuing Authority"),
        DocumentField("permit_number", "Permit No.", auto_generate=True),
        DocumentField("issue_date", "Issue Date", format="date"),
        DocumentField("expiry_date", "Expiry Date", format="date"),
        DocumentField("conditions", "Conditions", required=False),
    ],
))

# ── Invitation ──
_register(DocumentType(
    type_id="invitation",
    name="Invitation",
    category="ticket",
    layout="card",
    color_primary="#2c2c54",
    color_accent="#d4a574",
    color_bg="#faf8f5",
    has_qr=True,
    width_mm=140,
    height_mm=90,
    context_keywords=["invitation", "invite", "invited", "reception", "gala", "dinner", "ceremony", "opening"],
    fields=[
        DocumentField("guest", "Guest"),
        DocumentField("event", "Event"),
        DocumentField("host", "Host"),
        DocumentField("venue", "Venue"),
        DocumentField("date", "Date", format="date"),
        DocumentField("time", "Time"),
        DocumentField("dress_code", "Dress Code", required=False),
        DocumentField("rsvp_id", "RSVP #", auto_generate=True),
    ],
))
