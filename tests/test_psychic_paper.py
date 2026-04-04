"""Tests for the Psychic Paper."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from psychic_paper import PsychicPaper, DOCUMENT_TYPES
from psychic_paper.context import detect_document_type, read_context
from psychic_paper.renderer import render_html


# ── Schema Tests ──

def test_document_types_loaded():
    assert len(DOCUMENT_TYPES) >= 10
    assert "press_pass" in DOCUMENT_TYPES
    assert "event_ticket" in DOCUMENT_TYPES
    assert "boarding_pass" in DOCUMENT_TYPES
    assert "driving_licence" in DOCUMENT_TYPES


def test_all_types_have_fields():
    for type_id, dt in DOCUMENT_TYPES.items():
        assert len(dt.fields) >= 3, f"{type_id} has too few fields"
        assert dt.name, f"{type_id} has no name"
        assert dt.context_keywords, f"{type_id} has no context keywords"


# ── Context Detection Tests ──

def test_detect_press():
    ctx = read_context("I need press access to the conference")
    dt = detect_document_type(ctx)
    assert dt.type_id == "press_pass"


def test_detect_event():
    ctx = read_context("going to a concert tonight")
    dt = detect_document_type(ctx)
    assert dt.type_id == "event_ticket"


def test_detect_flight():
    ctx = read_context("boarding my flight at the airport")
    dt = detect_document_type(ctx)
    assert dt.type_id == "boarding_pass"


def test_detect_security():
    ctx = read_context("need security clearance for restricted area")
    dt = detect_document_type(ctx)
    assert dt.type_id == "security_badge"


def test_detect_transport():
    ctx = read_context("getting the tube to work")
    dt = detect_document_type(ctx)
    assert dt.type_id == "transport_pass"


def test_detect_with_data_hint():
    ctx = read_context("need credentials", data={"passenger": "Smith", "flight": "BA123"})
    dt = detect_document_type(ctx)
    assert dt.type_id == "boarding_pass"


# ── Engine Tests ──

def test_generate_basic():
    paper = PsychicPaper(identity={"name": "John Smith"})
    doc = paper.generate("attending a delegate summit")
    assert doc.doc_type.type_id == "conference_badge"
    assert doc.fields.get("name") == "John Smith"
    assert doc.document_hash
    assert doc.qr_data


def test_generate_forced_type():
    paper = PsychicPaper(identity={"name": "The Doctor"})
    doc = paper.generate(doc_type="press_pass")
    assert doc.doc_type.type_id == "press_pass"
    assert "The Doctor" in doc.fields.get("name", "")


def test_generate_with_data():
    paper = PsychicPaper()
    doc = paper.generate(
        "flight",
        data={"passenger": "Rose Tyler", "flight": "TX-42", "from_city": "London", "to_city": "Barcelona"},
    )
    assert doc.fields["passenger"] == "Rose Tyler"
    assert doc.fields["flight"] == "TX-42"


def test_morph():
    paper = PsychicPaper(identity={"name": "The Doctor"})
    doc1 = paper.generate("delegate at a summit")
    assert doc1.doc_type.type_id == "conference_badge"

    doc2 = paper.morph(doc1, "need journalist media credentials")
    assert doc2.doc_type.type_id == "press_pass"
    # Name should carry over
    assert "The Doctor" in doc2.fields.get("name", "")


def test_auto_generate_ids():
    paper = PsychicPaper(identity={"name": "Martha Jones"})
    doc = paper.generate(doc_type="press_pass")
    assert doc.fields.get("press_id", "").startswith("PR-")


def test_to_dict():
    paper = PsychicPaper(identity={"name": "Test"})
    doc = paper.generate(doc_type="membership")
    d = doc.to_dict()
    assert d["type"] == "membership"
    assert "colors" in d
    assert "fields" in d
    assert "qr_data" in d


# ── Renderer Tests ──

def test_render_html():
    paper = PsychicPaper(identity={"name": "The Doctor"})
    doc = paper.generate(doc_type="press_pass")
    html = render_html(doc)
    assert "<!DOCTYPE html>" in html
    assert "press_pass" in html
    assert "The Doctor" in html


def test_render_all_layouts():
    paper = PsychicPaper(identity={"name": "Test"})
    layouts_tested = set()
    for type_id in DOCUMENT_TYPES:
        doc = paper.generate(doc_type=type_id)
        html = render_html(doc)
        assert "<!DOCTYPE html>" in html
        layouts_tested.add(doc.doc_type.layout)
    # Should have tested all layout types
    assert layouts_tested >= {"card", "ticket", "badge", "full"}
