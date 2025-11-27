"""
LLM Integration Module for AetherOS
Provides unified interface for language model operations
"""

from .llm_config import LLMConfig
from .llm_service import LLMService, get_llm_service
from .hermes_provider import HermesProvider

__all__ = ['LLMService', 'LLMConfig', 'HermesProvider', 'get_llm_service']
