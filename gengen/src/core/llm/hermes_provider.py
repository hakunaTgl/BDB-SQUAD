"""
Hermes LLM Provider
Integrates Nous-Hermes model via Ollama or HuggingFace
"""

from typing import Optional, Dict, Any, List
import json
import asyncio
from loguru import logger


class HermesProvider:
    """
    Provider for Hermes LLM
    Supports both Ollama (recommended) and HuggingFace Transformers
    """
    
    def __init__(self, config):
        """Initialize Hermes provider with config"""
        self.config = config
        self.client = None
        self.model = None
        self.tokenizer = None
        self._initialized = False
        
        logger.info(f"Initializing Hermes provider with {config.provider}")
    
    async def initialize(self):
        """Initialize the LLM backend"""
        if self._initialized:
            return
        
        try:
            if self.config.provider == "ollama":
                await self._initialize_ollama()
            elif self.config.provider == "huggingface":
                await self._initialize_huggingface()
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
            
            self._initialized = True
            logger.info("Hermes provider initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Hermes provider: {e}")
            # Fall back to mock mode
            logger.warning("Falling back to mock LLM mode")
            self._initialized = True
    
    async def _initialize_ollama(self):
        """Initialize Ollama client"""
        try:
            # Try importing ollama
            try:
                import ollama
                self.client = ollama.AsyncClient(host=self.config.ollama_base_url)
                logger.info(f"Ollama client initialized at {self.config.ollama_base_url}")
                
                # Check if model exists, if not pull it
                try:
                    await self.client.show(self.config.model_name)
                    logger.info(f"Model {self.config.model_name} is available")
                except:
                    logger.info(f"Pulling model {self.config.model_name}...")
                    await self.client.pull(self.config.model_name)
                    logger.info(f"Model {self.config.model_name} pulled successfully")
                
            except ImportError:
                logger.warning("ollama package not installed, using mock mode")
                self.client = None
        except Exception as e:
            logger.warning(f"Ollama initialization failed: {e}, using mock mode")
            self.client = None
    
    async def _initialize_huggingface(self):
        """Initialize HuggingFace transformers"""
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            
            logger.info(f"Loading model {self.config.hf_model_id}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.hf_model_id,
                trust_remote_code=True
            )
            
            # Configure quantization if requested
            if self.config.hf_use_quantized:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True
                )
                logger.info("Using 4-bit quantization")
            else:
                quantization_config = None
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.hf_model_id,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.float16
            )
            
            logger.info("HuggingFace model loaded successfully")
        except Exception as e:
            logger.warning(f"HuggingFace initialization failed: {e}, using mock mode")
            self.model = None
            self.tokenizer = None
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate text using Hermes model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt override
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            **kwargs: Additional generation parameters
        
        Returns:
            Generated text
        """
        if not self._initialized:
            await self.initialize()
        
        # Use defaults if not specified
        system_prompt = system_prompt or self.config.system_prompt
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        if self.config.provider == "ollama":
            return await self._generate_ollama(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.config.provider == "huggingface":
            return await self._generate_huggingface(prompt, system_prompt, temperature, max_tokens, **kwargs)
        else:
            return await self._generate_mock(prompt, system_prompt)
    
    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using Ollama"""
        if not self.client:
            return await self._generate_mock(prompt, system_prompt)
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = await self.client.chat(
                model=self.config.model_name,
                messages=messages,
                options={
                    "temperature": temperature,
                    "top_p": self.config.top_p,
                    "top_k": self.config.top_k,
                    "num_predict": max_tokens
                }
            )
            
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return await self._generate_mock(prompt, system_prompt)
    
    async def _generate_huggingface(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Generate using HuggingFace transformers"""
        if not self.model or not self.tokenizer:
            return await self._generate_mock(prompt, system_prompt)
        
        try:
            # Format prompt for Hermes
            formatted_prompt = f"""<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
"""
            
            # Tokenize
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=self.config.top_p,
                    top_k=self.config.top_k,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant response
            if "<|im_start|>assistant" in response:
                response = response.split("<|im_start|>assistant")[-1].strip()
            
            return response
        except Exception as e:
            logger.error(f"HuggingFace generation failed: {e}")
            return await self._generate_mock(prompt, system_prompt)
    
    async def _generate_mock(self, prompt: str, system_prompt: str) -> str:
        """Mock generation for fallback"""
        logger.debug("Using mock LLM generation")
        
        # Simple rule-based responses for demo
        prompt_lower = prompt.lower()
        
        if "enhance" in prompt_lower and "prompt" in prompt_lower:
            return f"""Enhanced creative prompt:

{prompt}

This narrative explores themes of discovery, transformation, and wonder. 
The visual style should emphasize dramatic lighting and emotional depth.
Key emotional beats: curiosity -> discovery -> awe -> determination.
Character arc: Ordinary person -> Chosen one -> Hero's journey begins."""
        
        elif "script" in prompt_lower or "dialogue" in prompt_lower:
            return """SCENE 1: DISCOVERY

FADE IN:

INT. GRANDMOTHER'S ATTIC - DAY

Dust motes dance in shafts of golden light. Our protagonist explores old trunks and forgotten memories.

PROTAGONIST
(whispers)
What's this?

They discover a shimmering portal, pulsing with otherworldly energy.

FADE TO: Portal sequence..."""
        
        elif "scene" in prompt_lower or "storyboard" in prompt_lower:
            return """Scene Breakdown:

Scene 1: Opening - Ordinary World
Duration: 15s
Setting: Grandmother's attic, warm afternoon light
Mood: Curious, nostalgic

Scene 2: Discovery
Duration: 20s  
Setting: Same attic, portal appears
Mood: Mysterious, awe-inspiring

Scene 3: First Contact
Duration: 25s
Setting: Portal threshold
Mood: Wonder mixed with trepidation"""
        
        else:
            return f"""Based on the prompt: "{prompt}"

This is a compelling creative concept with strong narrative potential. 
The emotional resonance suggests a journey of self-discovery and transformation.
Visual style should balance realism with fantastical elements.
Pacing: Start slow to establish character, then build momentum.
Target audience: All ages, emphasis on wonder and adventure."""
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Chat completion with message history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
        
        Returns:
            Generated response
        """
        if not self._initialized:
            await self.initialize()
        
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        if self.config.provider == "ollama" and self.client:
            try:
                response = await self.client.chat(
                    model=self.config.model_name,
                    messages=messages,
                    options={
                        "temperature": temperature,
                        "top_p": self.config.top_p,
                        "top_k": self.config.top_k,
                        "num_predict": max_tokens
                    }
                )
                return response['message']['content']
            except Exception as e:
                logger.error(f"Ollama chat failed: {e}")
        
        # Fallback: convert to simple prompt
        user_message = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), "")
        system_message = next((m['content'] for m in messages if m['role'] == 'system'), self.config.system_prompt)
        
        return await self.generate(user_message, system_message, temperature, max_tokens, **kwargs)
