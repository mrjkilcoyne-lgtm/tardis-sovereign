"""The Interviewer -- agentic conversation system.

Hears your problem with a British sensibility, then routes to solutions.
The evolved Brunel Engine: warm, direct, occasionally wry.

Public API::

    from interviewer import interview, Interview, InterviewResult

    # Quick start -- interactive loop
    iv = interview()
    print(iv.start())
    while not iv.is_complete:
        user_input = input("> ")
        print(iv.respond(user_input))
    result = iv.result

    # Or use the class directly
    iv = Interview()
    greeting = iv.start()
    response = iv.respond("My server keeps crashing at 3am")
    # ... continue conversation ...

    # Output in various formats
    from interviewer.templates import to_markdown, to_json, to_one_page
    print(to_markdown(result))

    # Web interface
    from interviewer.web import serve
    serve(port=8080)
"""

from __future__ import annotations

from .conversation import Interview, InterviewResult, interview

__all__ = ["interview", "Interview", "InterviewResult"]
__version__ = "0.1.0"
