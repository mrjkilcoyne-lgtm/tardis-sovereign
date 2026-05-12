"""Simple web interface for The Interviewer.

Pure stdlib http.server -- no Flask, no dependencies.
Dark theme, TARDIS aesthetic (the vibe, not the brand).
Mobile-first, conversational flow.
"""

from __future__ import annotations

import html
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import ClassVar

from .conversation import Interview
from .templates import to_html_report


# ---------------------------------------------------------------------------
# In-memory session store (fine for single-user / demo use)
# ---------------------------------------------------------------------------

_sessions: dict[str, Interview] = {}
_session_counter = 0


def _new_session() -> tuple[str, Interview]:
    global _session_counter
    _session_counter += 1
    sid = f"s{_session_counter}"
    iv = Interview()
    _sessions[sid] = iv
    return sid, iv


# ---------------------------------------------------------------------------
# HTML / CSS / JS -- all inline, no external deps
# ---------------------------------------------------------------------------

PAGE_CSS = """
:root {
    --bg-deep: #0a0e1a;
    --bg-surface: #111827;
    --bg-card: #1a2234;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #3b82f6;
    --accent-glow: rgba(59, 130, 246, 0.15);
    --accent-warm: #f59e0b;
    --border: #1e293b;
    --success: #10b981;
    --warning: #f59e0b;
    --radius: 12px;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    --font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: var(--font);
    background: var(--bg-deep);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.header h1 {
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: var(--accent);
}

.header .subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
    font-family: var(--font-mono);
}

.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    max-width: 680px;
    margin: 0 auto;
    width: 100%;
}

.message {
    margin-bottom: 1rem;
    display: flex;
    gap: 0.75rem;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.interviewer {
    justify-content: flex-start;
}

.message.user {
    justify-content: flex-end;
}

.message .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 4px;
}

.message.interviewer .avatar {
    background: var(--accent);
    color: white;
}

.message.user .avatar {
    background: var(--bg-card);
    color: var(--text-secondary);
    border: 1px solid var(--border);
}

.bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: var(--radius);
    line-height: 1.5;
    font-size: 0.95rem;
}

.message.interviewer .bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

.message.user .bubble {
    background: var(--accent);
    color: white;
    border-bottom-right-radius: 4px;
}

.input-area {
    padding: 1rem;
    border-top: 1px solid var(--border);
    background: var(--bg-surface);
}

.input-area form {
    max-width: 680px;
    margin: 0 auto;
    display: flex;
    gap: 0.5rem;
}

.input-area textarea {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text-primary);
    padding: 0.75rem 1rem;
    font-family: var(--font);
    font-size: 0.95rem;
    resize: none;
    outline: none;
    min-height: 44px;
    max-height: 120px;
    line-height: 1.4;
}

.input-area textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-glow);
}

.input-area button {
    background: var(--accent);
    color: white;
    border: none;
    border-radius: var(--radius);
    padding: 0 1.25rem;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
    white-space: nowrap;
}

.input-area button:hover {
    background: #2563eb;
}

.input-area button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Report styles */
.interview-report {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin: 1rem 0;
}

.interview-report h2 {
    color: var(--accent);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}

.interview-report h3 {
    color: var(--text-primary);
    font-size: 1rem;
    margin: 1rem 0 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
}

.interview-report h3:first-child {
    border-top: none;
    padding-top: 0;
}

.interview-report p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 0.5rem;
}

.meta-bar {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
}

.domain-tag {
    background: var(--accent-glow);
    color: var(--accent);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
}

.confidence {
    color: var(--text-muted);
    font-size: 0.8rem;
    font-family: var(--font-mono);
}

.solution-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.75rem 0;
}

.solution-card h4 {
    color: var(--accent-warm);
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.solution-card ol, .solution-card ul {
    padding-left: 1.25rem;
    margin: 0.5rem 0;
}

.solution-card li {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin: 0.25rem 0;
}

.solution-card .meta {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
    flex-wrap: wrap;
}

.tag {
    background: var(--bg-deep);
    color: var(--text-muted);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-family: var(--font-mono);
}

.specialist-note {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: var(--accent-warm);
    font-size: 0.9rem;
}

.actions ul {
    list-style: none;
    padding: 0;
}

.actions li {
    padding: 0.4rem 0;
    padding-left: 1.5rem;
    position: relative;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.actions li::before {
    content: "\\25A1";
    position: absolute;
    left: 0;
    color: var(--accent);
}

.report-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid var(--border);
    font-family: var(--font-mono);
}

.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--success);
    margin-right: 0.5rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 0.5rem 0;
}

.typing-indicator span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
    animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-4px); }
}

/* New interview button */
.new-interview-btn {
    display: block;
    margin: 1rem auto;
    background: transparent;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: var(--radius);
    padding: 0.5rem 1.5rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}

.new-interview-btn:hover {
    background: var(--accent-glow);
}

/* Mobile */
@media (max-width: 600px) {
    .bubble { max-width: 90%; }
    .header h1 { font-size: 1.1rem; }
}
"""

PAGE_JS = """
let sessionId = null;
let isComplete = false;

async function startInterview() {
    const resp = await fetch('/api/start', { method: 'POST' });
    const data = await resp.json();
    sessionId = data.session_id;
    isComplete = false;
    addMessage('interviewer', data.greeting);
    document.getElementById('user-input').focus();
    document.getElementById('send-btn').disabled = false;
}

async function sendMessage(event) {
    event.preventDefault();
    if (isComplete) return;

    const input = document.getElementById('user-input');
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    addMessage('user', text);

    // Show typing indicator
    const typing = document.createElement('div');
    typing.className = 'message interviewer';
    typing.id = 'typing';
    typing.innerHTML = '<div class="avatar">I</div><div class="bubble"><div class="typing-indicator"><span></span><span></span><span></span></div></div>';
    document.getElementById('messages').appendChild(typing);
    scrollToBottom();

    const resp = await fetch('/api/respond', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ session_id: sessionId, message: text }),
    });
    const data = await resp.json();

    // Remove typing indicator
    document.getElementById('typing')?.remove();

    addMessage('interviewer', data.response);

    if (data.complete && data.report_html) {
        isComplete = true;
        const reportDiv = document.createElement('div');
        reportDiv.innerHTML = data.report_html;
        document.getElementById('messages').appendChild(reportDiv);

        const btn = document.createElement('button');
        btn.className = 'new-interview-btn';
        btn.textContent = 'Start a new conversation';
        btn.onclick = () => { document.getElementById('messages').innerHTML = ''; startInterview(); };
        document.getElementById('messages').appendChild(btn);

        document.getElementById('send-btn').disabled = true;
        scrollToBottom();
    }
}

function addMessage(role, text) {
    const messages = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'message ' + role;

    const avatar = role === 'interviewer' ? 'I' : 'Y';
    // Preserve newlines in response
    const escaped = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\\n/g, '<br>');

    if (role === 'interviewer') {
        div.innerHTML = '<div class="avatar">' + avatar + '</div><div class="bubble">' + escaped + '</div>';
    } else {
        div.innerHTML = '<div class="bubble">' + escaped + '</div><div class="avatar">' + avatar + '</div>';
    }

    messages.appendChild(div);
    scrollToBottom();
}

function scrollToBottom() {
    const container = document.querySelector('.chat-container');
    container.scrollTop = container.scrollHeight;
}

// Handle Enter to send (Shift+Enter for newline)
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('user-input');
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.getElementById('chat-form').dispatchEvent(new Event('submit'));
        }
    });
    // Auto-resize textarea
    input.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    });
    startInterview();
});
"""


def _build_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>The Interviewer</title>
    <style>{PAGE_CSS}</style>
</head>
<body>
    <div class="header">
        <h1><span class="status-indicator"></span>The Interviewer</h1>
        <div class="subtitle">problem diagnosis &amp; solution routing</div>
    </div>

    <div class="chat-container">
        <div id="messages"></div>
    </div>

    <div class="input-area">
        <form id="chat-form" onsubmit="sendMessage(event)">
            <textarea id="user-input" placeholder="Tell me what's going on..." rows="1"></textarea>
            <button type="submit" id="send-btn">Send</button>
        </form>
    </div>

    <script>{PAGE_JS}</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class InterviewHandler(BaseHTTPRequestHandler):
    """Handles the web interface and API endpoints."""

    server_version: ClassVar[str] = "TheInterviewer/1.0"

    def log_message(self, format: str, *args: object) -> None:
        # Quieter logging
        pass

    def _send_response(self, code: int, content_type: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self._send_response(200, "application/json", body)

    def do_GET(self) -> None:
        if self.path == "/" or self.path == "/index.html":
            body = _build_page().encode("utf-8")
            self._send_response(200, "text/html; charset=utf-8", body)
        else:
            self._send_response(404, "text/plain", b"Not found")

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""

        if self.path == "/api/start":
            sid, iv = _new_session()
            greeting = iv.start()
            self._send_json({"session_id": sid, "greeting": greeting})

        elif self.path == "/api/respond":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self._send_response(400, "text/plain", b"Invalid JSON")
                return

            sid = data.get("session_id", "")
            message = data.get("message", "")

            iv = _sessions.get(sid)
            if not iv:
                self._send_json({"error": "Session not found. Please start a new interview."})
                return

            response = iv.respond(message)

            result_data: dict = {
                "response": response,
                "complete": iv.is_complete,
                "state": iv.state.value,
            }

            if iv.is_complete and iv.result:
                result_data["report_html"] = to_html_report(iv.result)
                result_data["result"] = iv.result.to_dict()

            self._send_json(result_data)

        else:
            self._send_response(404, "text/plain", b"Not found")


def serve(host: str = "0.0.0.0", port: int = 8080) -> None:
    """Start the web server."""
    server = HTTPServer((host, port), InterviewHandler)
    print(f"The Interviewer is listening on http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    serve()
