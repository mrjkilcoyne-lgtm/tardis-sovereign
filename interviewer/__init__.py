"""The Interviewer - Hears your problem. Routes to solutions.

British-voiced agentic conversation. Warm, direct, occasionally wry.
Like a good GP or a sharp friend who happens to know everything.
"""

from .conversation import Interview, InterviewResult, interview

__all__ = ["Interview", "InterviewResult", "interview"]
