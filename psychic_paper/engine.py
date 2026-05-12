"""The Psychic Paper engine. Generates documents that match the moment.

Takes a context, picks the right document type, fills in fields,
generates identifiers, and produces a complete document ready to render.
"""

from __future__ import annotations

import hashlib
import random
import string
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .context import Context, detect_document_type, read_context
from .schemas import DOCUMENT_TYPES, DocumentField, DocumentType


@dataclass
class GeneratedDocument:
    """A complete document ready to render."""
    doc_type: DocumentType
    fields: dict[str, str]     # field_name -> value
    generated_at: datetime = field(default_factory=datetime.now)
    document_hash: str = ""    # verification hash
    qr_data: str = ""          # what the QR encodes

    def to_dict(self) -> dict:
        return {
            "type": self.doc_type.type_id,
            "type_name": self.doc_type.name,
            "layout": self.doc_type.layout,
            "colors": {
                "primary": self.doc_type.color_primary,
                "accent": self.doc_type.color_accent,
                "bg": self.doc_type.color_bg,
            },
            "fields": self.fields,
            "has_photo": self.doc_type.has_photo,
            "has_barcode": self.doc_type.has_barcode,
            "has_qr": self.doc_type.has_qr,
            "has_hologram": self.doc_type.has_hologram,
            "document_hash": self.document_hash,
            "qr_data": self.qr_data,
            "generated_at": self.generated_at.isoformat(),
            "dimensions": {
                "width_mm": self.doc_type.width_mm,
                "height_mm": self.doc_type.height_mm,
            },
        }


class PsychicPaper:
    """The Paper itself. Give it a situation, it becomes what's needed."""

    def __init__(self, identity: dict | None = None):
        """
        Args:
            identity: Default identity fields (name, org, etc.)
                      Used to auto-fill documents consistently.
        """
        self.identity = identity or {}

    def generate(
        self,
        situation: str = "",
        doc_type: str | None = None,
        location: str = "",
        audience: str = "",
        formality: str = "standard",
        data: dict | None = None,
    ) -> GeneratedDocument:
        """Generate a document for the situation.

        Args:
            situation: What's happening ("attending a conference", "need press access")
            doc_type: Force a specific document type (bypasses detection)
            location: Where this is happening
            audience: Who's looking at it
            formality: casual / standard / formal / official
            data: Specific field values to use

        Returns:
            A complete GeneratedDocument ready for rendering.
        """
        # Merge identity defaults with provided data
        merged_data = {**self.identity, **(data or {})}

        if doc_type and doc_type in DOCUMENT_TYPES:
            dtype = DOCUMENT_TYPES[doc_type]
        else:
            ctx = read_context(
                situation=situation,
                location=location,
                audience=audience,
                formality=formality,
                data=merged_data,
            )
            dtype = detect_document_type(ctx)

        # Fill fields
        filled = self._fill_fields(dtype, merged_data)

        # Generate verification hash
        doc_hash = self._generate_hash(dtype, filled)

        # Generate QR data
        qr_data = self._generate_qr_data(dtype, filled, doc_hash)

        return GeneratedDocument(
            doc_type=dtype,
            fields=filled,
            document_hash=doc_hash,
            qr_data=qr_data,
        )

    def morph(self, doc: GeneratedDocument, new_situation: str = "", new_data: dict | None = None) -> GeneratedDocument:
        """Morph an existing document into something new.

        The paper shifts. Same surface, different face.
        """
        merged = {**doc.fields, **(new_data or {})}
        return self.generate(
            situation=new_situation,
            data=merged,
        )

    def _fill_fields(self, dtype: DocumentType, data: dict) -> dict[str, str]:
        """Fill document fields from data, identity, or auto-generation."""
        filled = {}
        for f in dtype.fields:
            if f.name in data:
                filled[f.name] = str(data[f.name])
            elif f.auto_generate:
                filled[f.name] = self._auto_generate(f, dtype)
            elif f.format == "photo":
                continue  # photos handled separately
            elif f.format == "date":
                filled[f.name] = self._auto_date(f)
            elif self._identity_match(f):
                filled[f.name] = str(self.identity[self._identity_match(f)])
            elif f.required:
                filled[f.name] = self._sensible_default(f, dtype)
        return filled

    def _auto_generate(self, f: DocumentField, dtype: DocumentType) -> str:
        """Generate realistic-looking IDs, numbers, references."""
        ts = int(time.time() * 1000) % 10000000
        prefix_map = {
            "press_id": "PR",
            "ticket_id": "TK",
            "booking_ref": "",
            "licence_number": "KILCO",
            "member_id": "MEM",
            "badge_id": "SC",
            "pass_id": "TP",
            "permit_number": "PMT",
            "rsvp_id": "RSV",
        }
        prefix = prefix_map.get(f.name, "ID")

        if f.name == "booking_ref":
            # Airline-style: 6 alphanumeric
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        elif f.name == "licence_number":
            # UK style: SURNAME + digits
            name_part = self.identity.get("surname", self.identity.get("name", "SMITH"))[:5].upper()
            return f"{name_part:<5s}{random.randint(600000, 999999):06d}{''.join(random.choices(string.ascii_uppercase, k=2))}"

        return f"{prefix}-{ts:07d}"

    def _auto_date(self, f: DocumentField) -> str:
        """Generate sensible dates based on field semantics."""
        now = datetime.now()
        if "expiry" in f.name or "valid_to" in f.name or f.name == "expiry":
            d = now + timedelta(days=random.randint(180, 365 * 3))
        elif "issue" in f.name or "since" in f.name or "valid_from" in f.name:
            d = now - timedelta(days=random.randint(30, 365 * 2))
        elif f.name == "dob":
            d = now - timedelta(days=random.randint(365 * 25, 365 * 45))
        else:
            d = now  # today
        return d.strftime("%d/%m/%Y")

    def _identity_match(self, f: DocumentField) -> str | None:
        """Try to match a field to identity data with fuzzy key matching."""
        direct = {
            "name": ["name", "full_name"],
            "surname": ["surname", "last_name"],
            "forenames": ["forenames", "first_name", "given_name"],
            "holder": ["name", "full_name"],
            "passenger": ["name", "full_name"],
            "guest": ["name", "full_name"],
            "org": ["org", "organisation", "organization", "company"],
            "title": ["title", "job_title"],
            "address": ["address"],
        }
        candidates = direct.get(f.name, [])
        for key in candidates:
            if key in self.identity:
                return key
        return None

    def _sensible_default(self, f: DocumentField, dtype: DocumentType) -> str:
        """Last resort: generate something plausible."""
        defaults = {
            "zone": "All Areas",
            "seat": "General Admission",
            "class_type": "Standard",
            "tier": "Standard",
            "role": "Delegate",
            "categories": "B",
            "ticket_type": "Standard",
            "zones": "1-6",
            "pass_type": "Annual",
            "clearance_level": "Authorised",
            "department": "General",
            "dress_code": "Smart Casual",
            "conditions": "Standard terms apply",
            "time": "19:00",
            "boarding_time": "17:30",
            "gate": str(random.randint(1, 60)),
        }
        return defaults.get(f.name, "—")

    def _generate_hash(self, dtype: DocumentType, fields: dict) -> str:
        """Generate a verification hash for the document."""
        content = f"{dtype.type_id}:{sorted(fields.items())}:{time.time()}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def _generate_qr_data(self, dtype: DocumentType, fields: dict, doc_hash: str) -> str:
        """Generate QR code content. Compact but verifiable."""
        # Minimal format: TYPE|HASH|KEY_FIELDS
        key_field = next(
            (fields.get(f.name, "") for f in dtype.fields if not f.auto_generate and f.required),
            "",
        )
        return f"TARDIS|{dtype.type_id}|{doc_hash}|{key_field[:30]}"
