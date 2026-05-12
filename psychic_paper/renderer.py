"""Renderer. Produces the visual output - HTML that morphs per document type.

Generates a complete self-contained HTML document that:
- Adapts its layout to the document type (card, ticket, badge, full)
- Uses the document's color scheme
- Includes QR code generation (via JS)
- Animates transitions when morphing between types
- Looks convincing on a phone screen
"""

from __future__ import annotations

import json
from pathlib import Path

from .engine import GeneratedDocument


def render_html(doc: GeneratedDocument) -> str:
    """Render a document as a self-contained HTML page."""
    d = doc.to_dict()
    return _TEMPLATE.replace("{{DOCUMENT_DATA}}", json.dumps(d, indent=2))


def render_multi_html(docs: list[GeneratedDocument]) -> str:
    """Render multiple documents as a swipeable collection."""
    data = [d.to_dict() for d in docs]
    return _MULTI_TEMPLATE.replace("{{DOCUMENTS_DATA}}", json.dumps(data, indent=2))


def serve(doc: GeneratedDocument, port: int = 0) -> str:
    """Serve the document on a local HTTP server. Returns the URL."""
    import http.server
    import threading

    html = render_html(doc)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

        def log_message(self, *args):
            pass  # quiet

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{actual_port}"


# ─── THE HTML TEMPLATE ───────────────────────────────────────────

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Psychic Paper</title>
<style>
  :root {
    --primary: #1a1a2e;
    --accent: #e94560;
    --bg: #ffffff;
    --text: #1a1a1a;
    --text-light: #666;
    --transition: 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0a;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    overflow: hidden;
  }

  .paper {
    position: relative;
    transition: all var(--transition);
    transform-style: preserve-3d;
    max-width: 420px;
    width: 100%;
  }

  /* ── Card Layout ── */
  .layout-card .document {
    background: var(--bg);
    border-radius: 12px;
    padding: 24px;
    aspect-ratio: 86/54;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
  }

  /* ── Ticket Layout ── */
  .layout-ticket .document {
    background: var(--bg);
    border-radius: 16px;
    padding: 0;
    display: flex;
    flex-direction: row;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    min-height: 180px;
  }

  .layout-ticket .ticket-main {
    flex: 1;
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .layout-ticket .ticket-stub {
    width: 100px;
    background: var(--primary);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px 8px;
    position: relative;
  }

  .layout-ticket .ticket-stub::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    background: #0a0a0a;
    border-radius: 50%;
  }

  .layout-ticket .ticket-perforation {
    position: absolute;
    left: calc(100% - 108px);
    top: 0;
    bottom: 0;
    width: 1px;
    background: repeating-linear-gradient(
      to bottom,
      transparent, transparent 4px,
      rgba(0,0,0,0.15) 4px, rgba(0,0,0,0.15) 8px
    );
  }

  /* ── Badge Layout ── */
  .layout-badge .document {
    background: var(--bg);
    border-radius: 12px 12px 24px 24px;
    padding: 0;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    min-height: 280px;
  }

  .layout-badge .badge-header {
    background: var(--primary);
    color: white;
    padding: 16px 24px;
    text-align: center;
  }

  .layout-badge .badge-body {
    padding: 20px 24px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .layout-badge .badge-lanyard {
    width: 30px;
    height: 20px;
    background: var(--primary);
    margin: 0 auto;
    border-radius: 0 0 4px 4px;
    position: relative;
  }

  .layout-badge .badge-lanyard::after {
    content: '';
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    height: 40px;
    background: linear-gradient(to bottom, transparent, var(--primary));
  }

  /* ── Full Layout (permits) ── */
  .layout-full .document {
    background: var(--bg);
    border-radius: 4px;
    padding: 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    min-height: 300px;
    border: 2px solid var(--primary);
  }

  .layout-full .document::before {
    content: '';
    position: absolute;
    top: 8px; left: 8px; right: 8px; bottom: 8px;
    border: 1px solid rgba(0,0,0,0.1);
    pointer-events: none;
  }

  /* ── Common Elements ── */
  .doc-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }

  .doc-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--primary);
    opacity: 0.7;
  }

  .doc-name {
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.5px;
  }

  .doc-field {
    margin-bottom: 8px;
  }

  .doc-field-label {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-light);
    margin-bottom: 2px;
  }

  .doc-field-value {
    font-size: 14px;
    color: var(--text);
    font-weight: 500;
  }

  .doc-fields-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 16px;
  }

  .doc-fields-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .doc-accent-bar {
    height: 4px;
    background: var(--accent);
    border-radius: 2px;
    margin: 12px 0;
  }

  /* ── Hologram Effect ── */
  .hologram {
    position: absolute;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: conic-gradient(
      from 0deg,
      rgba(255,0,0,0.15),
      rgba(0,255,0,0.15),
      rgba(0,0,255,0.15),
      rgba(255,0,0,0.15)
    );
    animation: holo-rotate 4s linear infinite;
    opacity: 0.6;
    mix-blend-mode: multiply;
  }

  @keyframes holo-rotate {
    to { transform: rotate(360deg); }
  }

  /* ── QR Code ── */
  .qr-container {
    width: 64px;
    height: 64px;
    background: white;
    padding: 4px;
    border-radius: 4px;
  }

  .qr-container canvas {
    width: 100% !important;
    height: 100% !important;
  }

  /* ── Barcode ── */
  .barcode {
    height: 32px;
    display: flex;
    gap: 1px;
    align-items: stretch;
  }

  .barcode .bar {
    background: var(--text);
    flex-shrink: 0;
  }

  /* ── Hash Verification ── */
  .doc-hash {
    font-family: 'Courier New', monospace;
    font-size: 8px;
    color: var(--text-light);
    opacity: 0.5;
    letter-spacing: 1px;
    margin-top: 8px;
  }

  /* ── Morph Animation ── */
  .morphing {
    animation: morph-pulse 0.6s ease-in-out;
  }

  @keyframes morph-pulse {
    0% { transform: scale(1) rotateY(0); opacity: 1; }
    50% { transform: scale(0.95) rotateY(90deg); opacity: 0.5; }
    100% { transform: scale(1) rotateY(0); opacity: 1; }
  }

  /* ── Ambient glow ── */
  .paper::after {
    content: '';
    position: absolute;
    inset: -20px;
    background: radial-gradient(ellipse at center, var(--accent), transparent 70%);
    opacity: 0.08;
    z-index: -1;
    filter: blur(40px);
  }

  /* ── Controls ── */
  .controls {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 8px;
    z-index: 100;
  }

  .controls button {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.7);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 11px;
    cursor: pointer;
    backdrop-filter: blur(10px);
    transition: all 0.2s;
    font-family: inherit;
    letter-spacing: 0.5px;
  }

  .controls button:hover {
    background: rgba(255,255,255,0.2);
    color: white;
  }
</style>
</head>
<body>

<div class="paper" id="paper"></div>

<script>
// ── QR Code Generator (minimal, no deps) ──
const QR={generate:function(t){const s=t.length,e=s<=25?2:s<=47?3:s<=77?4:s<=114?5:6,n=17+4*e,r=Array.from({length:n},()=>Array(n).fill(0));function f(x,y,v){if(x>=0&&x<n&&y>=0&&y<n)r[y][x]=v?1:0}for(let i=0;i<7;i++)for(let j=0;j<7;j++){const v=i===0||i===6||j===0||j===6||(i>=2&&i<=4&&j>=2&&j<=4);f(i,j,v);f(n-7+i,j,v);f(i,n-7+j,v)}for(let y=0;y<n;y++)for(let x=0;x<n;x++){if(r[y][x]===0){const h=((x*7+y*13+x*y)^(t.charCodeAt((x+y)%s)||0))&1;r[y][x]=h}}return{modules:r,size:n}},toCanvas:function(c,d,sz){const ctx=c.getContext('2d');c.width=c.height=sz;const cs=sz/d.size;ctx.fillStyle='#fff';ctx.fillRect(0,0,sz,sz);ctx.fillStyle='#000';for(let y=0;y<d.size;y++)for(let x=0;x<d.size;x++)if(d.modules[y][x])ctx.fillRect(x*cs,y*cs,cs+0.5,cs+0.5)}};

// ── Barcode Generator ──
function generateBarcode(text) {
  const bars = [];
  for (let i = 0; i < text.length * 3; i++) {
    const charCode = text.charCodeAt(i % text.length) || 0;
    const w = ((charCode * (i + 1) * 7) % 4) + 1;
    const isBar = i % 2 === 0;
    bars.push({ width: w, filled: isBar });
  }
  return bars;
}

// ── Document Data ──
const DOC = {{DOCUMENT_DATA}};

// ── Render Functions ──
function setColors(colors) {
  document.documentElement.style.setProperty('--primary', colors.primary);
  document.documentElement.style.setProperty('--accent', colors.accent);
  document.documentElement.style.setProperty('--bg', colors.bg);
}

function fieldHTML(label, value) {
  return `<div class="doc-field">
    <div class="doc-field-label">${label}</div>
    <div class="doc-field-value">${value}</div>
  </div>`;
}

function renderCard(doc) {
  const fields = doc.fields;
  const nameField = fields.name || fields.holder || fields.surname || fields.passenger || fields.guest || '';
  const topFields = Object.entries(fields).filter(([k]) =>
    !['name','holder','surname','passenger','guest','photo','forenames'].includes(k)
  ).slice(0, 6);

  let subtitle = '';
  if (fields.forenames) subtitle = fields.forenames + ' ';

  return `<div class="layout-card">
    <div class="document">
      <div>
        <div class="doc-title">${doc.type_name}</div>
        <div class="doc-accent-bar"></div>
        <div class="doc-name">${subtitle}${nameField}</div>
      </div>
      <div class="doc-fields-grid">
        ${topFields.map(([k, v]) => {
          const label = k.replace(/_/g, ' ');
          return fieldHTML(label, v);
        }).join('')}
      </div>
      <div style="display:flex;justify-content:space-between;align-items:flex-end">
        <div class="doc-hash">${doc.document_hash}</div>
        ${doc.has_qr ? '<div class="qr-container"><canvas id="qr"></canvas></div>' : ''}
      </div>
      ${doc.has_hologram ? '<div class="hologram" style="position:absolute;top:12px;right:12px"></div>' : ''}
    </div>
  </div>`;
}

function renderTicket(doc) {
  const fields = doc.fields;
  const mainName = fields.event_name || fields.event || fields.passenger || '';
  const topFields = Object.entries(fields).filter(([k]) =>
    !['event_name','event','ticket_id','booking_ref'].includes(k)
  ).slice(0, 6);
  const stubId = fields.ticket_id || fields.booking_ref || doc.document_hash;

  return `<div class="layout-ticket">
    <div class="document">
      <div class="ticket-main">
        <div>
          <div class="doc-title">${doc.type_name}</div>
          <div class="doc-accent-bar"></div>
          <div class="doc-name">${mainName}</div>
        </div>
        <div class="doc-fields-row">
          ${topFields.map(([k, v]) => fieldHTML(k.replace(/_/g, ' '), v)).join('')}
        </div>
        <div class="doc-hash">${doc.document_hash}</div>
      </div>
      <div class="ticket-perforation"></div>
      <div class="ticket-stub">
        ${doc.has_qr ? '<div class="qr-container" style="margin-bottom:8px"><canvas id="qr"></canvas></div>' : ''}
        <div style="color:rgba(255,255,255,0.7);font-size:9px;letter-spacing:1px;text-align:center;word-break:break-all">${stubId}</div>
      </div>
    </div>
  </div>`;
}

function renderBadge(doc) {
  const fields = doc.fields;
  const name = fields.name || fields.holder || '';
  const role = fields.role || fields.clearance_level || fields.title || '';
  const org = fields.org || fields.event_name || fields.department || '';
  const otherFields = Object.entries(fields).filter(([k]) =>
    !['name','holder','role','clearance_level','title','org','event_name','department','photo','badge_id'].includes(k)
  ).slice(0, 4);

  return `<div class="layout-badge">
    <div class="badge-lanyard"></div>
    <div class="document">
      <div class="badge-header">
        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;opacity:0.7;margin-bottom:4px">${doc.type_name}</div>
        <div style="font-size:13px;font-weight:600">${org}</div>
      </div>
      <div class="badge-body">
        <div style="text-align:center;margin:16px 0">
          <div class="doc-name" style="font-size:26px">${name}</div>
          ${role ? `<div style="font-size:14px;color:var(--accent);font-weight:600;margin-top:4px;letter-spacing:1px">${role}</div>` : ''}
        </div>
        <div class="doc-fields-grid">
          ${otherFields.map(([k, v]) => fieldHTML(k.replace(/_/g, ' '), v)).join('')}
        </div>
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:12px">
          <div>
            <div class="doc-hash">${doc.document_hash}</div>
            ${fields.badge_id ? `<div style="font-family:monospace;font-size:11px;color:var(--text-light)">${fields.badge_id}</div>` : ''}
          </div>
          ${doc.has_qr ? '<div class="qr-container"><canvas id="qr"></canvas></div>' : ''}
        </div>
      </div>
      ${doc.has_hologram ? '<div class="hologram" style="position:absolute;bottom:60px;right:20px"></div>' : ''}
    </div>
  </div>`;
}

function renderFull(doc) {
  const fields = doc.fields;
  const allFields = Object.entries(fields).filter(([k]) => k !== 'photo');

  return `<div class="layout-full">
    <div class="document">
      <div style="text-align:center;margin-bottom:20px">
        <div class="doc-title" style="font-size:13px;margin-bottom:8px">${doc.type_name}</div>
        <div class="doc-accent-bar" style="width:60px;margin:0 auto"></div>
      </div>
      <div class="doc-fields-grid" style="grid-template-columns:1fr 1fr;gap:12px 24px">
        ${allFields.map(([k, v]) => fieldHTML(k.replace(/_/g, ' '), v)).join('')}
      </div>
      <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:20px;padding-top:12px;border-top:1px solid rgba(0,0,0,0.1)">
        <div class="doc-hash">${doc.document_hash}</div>
        ${doc.has_qr ? '<div class="qr-container"><canvas id="qr"></canvas></div>' : ''}
      </div>
      ${doc.has_hologram ? '<div class="hologram" style="position:absolute;top:20px;right:20px"></div>' : ''}
    </div>
  </div>`;
}

// ── Main Render ──
function render(doc) {
  setColors(doc.colors);
  const paper = document.getElementById('paper');

  const renderers = { card: renderCard, ticket: renderTicket, badge: renderBadge, full: renderFull };
  const renderFn = renderers[doc.layout] || renderCard;

  paper.innerHTML = renderFn(doc);

  // Generate QR
  if (doc.has_qr) {
    setTimeout(() => {
      const canvas = document.getElementById('qr');
      if (canvas && doc.qr_data) {
        const qrData = QR.generate(doc.qr_data);
        QR.toCanvas(canvas, qrData, 200);
      }
    }, 50);
  }
}

// ── Init ──
render(DOC);
</script>
</body>
</html>"""


# Multi-document template for swipeable collection
_MULTI_TEMPLATE = _TEMPLATE  # TODO: Add swipe support
