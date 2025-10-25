"""
LLM Configuration for AetherOS
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os


@dataclass
class LLMConfig:
    """Configuration for LLM integration"""
    
    # Model settings
    model_name: str = "hermes2-pro-mistral:latest"  # Nous-Hermes-2-Pro-Mistral
    provider: str = "ollama"  # ollama, huggingface, or openai-compatible
    
    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"
    
    # HuggingFace settings
    hf_model_id: Optional[str] = "NousResearch/Hermes-2-Pro-Mistral-7B"
    hf_use_quantized: bool = True  # Use 4-bit quantization
    
    # Generation settings
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    max_tokens: int = 2048
    
    # System behavior
    system_prompt: str = """You are Hermes, an advanced AI assistant integrated into AetherOS, 
a creative content generation system. You excel at understanding creative prompts, 
generating engaging narratives, and providing thoughtful analysis. You are unfiltered 
but ethical, creative but grounded, and always aim to enhance the user's creative vision."""
    
    # Timeout settings
    request_timeout: int = 120  # seconds
    
    @classmethod
    def from_env(cls) -> 'LLMConfig':
        """Create configuration from environment variables"""
        return cls(
            model_name=os.getenv('LLM_MODEL_NAME', cls.model_name),
            provider=os.getenv('LLM_PROVIDER', cls.provider),
            ollama_base_url=os.getenv('OLLAMA_BASE_URL', cls.ollama_base_url),
            hf_model_id=os.getenv('HF_MODEL_ID', cls.hf_model_id),
            temperature=float(os.getenv('LLM_TEMPERATURE', cls.temperature)),
            max_tokens=int(os.getenv('LLM_MAX_TOKENS', cls.max_tokens))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'model_name': self.model_name,
            'provider': self.provider,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'max_tokens': self.max_tokens
        }
