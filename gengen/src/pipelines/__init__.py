"""
Pipeline interfaces for advanced media generation workflows.

Each pipeline exposes a light, async-friendly API so the orchestrator can
compose and schedule long-running jobs while keeping resource usage bounded.
"""

from .audio_animation import AudioAnimationPipeline
from .storyboard_video import StoryboardVideoPipeline

__all__ = [
    "AudioAnimationPipeline",
    "StoryboardVideoPipeline",
]
