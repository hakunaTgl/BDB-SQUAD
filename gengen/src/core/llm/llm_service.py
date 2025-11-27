"""
LLM Service Layer for AetherOS
Provides high-level interface for all LLM operations
"""

from typing import Optional, Dict, Any, List
import asyncio

# Make loguru optional
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

from .llm_config import LLMConfig
from .hermes_provider import HermesProvider


class LLMService:
    """
    Unified LLM service for AetherOS
    Manages Hermes model integration for all text generation tasks
    """
    
    _instance = None
    _lock = asyncio.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize LLM service"""
        if hasattr(self, '_initialized'):
            return
        
        self.config = LLMConfig.from_env()
        self.provider = HermesProvider(self.config)
        self._initialized = False
        
        logger.info("LLM Service created")
    
    async def initialize(self):
        """Initialize the LLM provider"""
        if self._initialized:
            return
        
        async with self._lock:
            if self._initialized:
                return
            
            await self.provider.initialize()
            self._initialized = True
            logger.info("LLM Service initialized")
    
    async def enhance_prompt(
        self,
        prompt: str,
        style: Optional[str] = None,
        emotional_tone: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Enhance a creative prompt with additional context and detail
        
        Args:
            prompt: Original user prompt
            style: Visual/narrative style
            emotional_tone: Desired emotional tone
        
        Returns:
            Enhanced prompt
        """
        await self.initialize()
        
        enhancement_prompt = f"""Enhance this creative prompt for a multimedia content generation system.

Original Prompt: {prompt}

Style: {style or 'cinematic'}
Emotional Tone: {emotional_tone or 'balanced'}

Provide an enhanced version that:
1. Expands on the narrative concept
2. Adds visual and emotional detail
3. Suggests key story beats
4. Maintains the original vision
5. Keeps it concise (under 200 words)

Enhanced Prompt:"""
        
        system_prompt = "You are a creative director helping enhance story prompts. Provide rich, evocative enhancements that maintain the user's original vision."
        
        enhanced = await self.provider.generate(
            prompt=enhancement_prompt,
            system_prompt=system_prompt,
            temperature=0.8
        )
        
        return enhanced.strip()
    
    async def generate_script(
        self,
        prompt: str,
        duration: int = 60,
        style: str = "cinematic",
        **kwargs
    ) -> str:
        """
        Generate a script from a prompt
        
        Args:
            prompt: Story prompt
            duration: Target duration in seconds
            style: Narrative style
        
        Returns:
            Generated script
        """
        await self.initialize()
        
        script_prompt = f"""Generate a {duration}-second {style} script based on this concept:

{prompt}

Create a properly formatted script with:
- Scene headings (INT./EXT.)
- Action descriptions
- Character dialogue (if applicable)
- Camera directions
- Emotional beats

Keep it concise and suitable for a {duration}-second production.

Script:"""
        
        system_prompt = "You are an expert screenwriter. Create engaging, well-formatted scripts that are visually compelling and emotionally resonant."
        
        script = await self.provider.generate(
            prompt=script_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        )
        
        return script.strip()
    
    async def decompose_story(
        self,
        prompt: str,
        duration: int = 120,
        num_scenes: Optional[int] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Decompose a story into scenes for storyboard generation
        
        Args:
            prompt: Story prompt
            duration: Total duration in seconds
            num_scenes: Optional target number of scenes
        
        Returns:
            List of scene dictionaries
        """
        await self.initialize()
        
        if num_scenes is None:
            num_scenes = max(3, duration // 30)  # Roughly 30s per scene
        
        decomposition_prompt = f"""Break down this story concept into {num_scenes} distinct scenes for a {duration}-second production:

{prompt}

For each scene, provide:
1. Scene number and title
2. Duration (in seconds)
3. Setting/location
4. Action description
5. Mood/atmosphere
6. Key visual elements
7. Camera suggestions

Format as a numbered list with clear sections.

Scene Breakdown:"""
        
        system_prompt = "You are a storyboard artist and film director. Break down stories into clear, visually compelling scenes."
        
        breakdown = await self.provider.generate(
            prompt=decomposition_prompt,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=2000
        )
        
        # Parse into structured scenes (simplified parsing)
        scenes = []
        lines = breakdown.strip().split('\n')
        current_scene = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_scene:
                    scenes.append(current_scene)
                    current_scene = {}
                continue
            
            if line.lower().startswith('scene'):
                if current_scene:
                    scenes.append(current_scene)
                current_scene = {'title': line}
            elif current_scene:
                if 'description' not in current_scene:
                    current_scene['description'] = line
                else:
                    current_scene['description'] += ' ' + line
        
        if current_scene:
            scenes.append(current_scene)
        
        # Ensure we have at least some scenes
        if not scenes:
            scenes = [{
                'title': f'Scene 1',
                'description': prompt,
                'duration': duration
            }]
        
        return scenes
    
    async def generate_meta_prompt(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        Generate a meta-prompt for task execution
        
        Args:
            task_description: Description of the task
            context: Additional context
        
        Returns:
            Generated meta-prompt
        """
        await self.initialize()
        
        context_str = ""
        if context:
            context_str = f"\n\nContext:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
        
        meta_prompt_request = f"""Create a detailed meta-prompt for executing this creative task:

Task: {task_description}{context_str}

Generate a structured meta-prompt following the SPARC framework:
- SITUATION: Analyze the current task and requirements
- PROBLEM: Identify core challenges and constraints  
- ACTIONS: Define execution strategy step-by-step
- RESULT: Specify success criteria
- CRITIQUE: Evaluate approach and alternatives

Meta-Prompt:"""
        
        system_prompt = "You are an expert at meta-cognition and task planning. Create comprehensive meta-prompts that guide effective task execution."
        
        meta_prompt = await self.provider.generate(
            prompt=meta_prompt_request,
            system_prompt=system_prompt,
            temperature=0.6,
            max_tokens=1500
        )
        
        return meta_prompt.strip()
    
    async def refine_meta_prompt(
        self,
        original_prompt: str,
        performance_feedback: str,
        **kwargs
    ) -> str:
        """
        Refine a meta-prompt based on performance feedback
        
        Args:
            original_prompt: Original meta-prompt
            performance_feedback: Feedback on performance
        
        Returns:
            Refined meta-prompt
        """
        await self.initialize()
        
        refinement_request = f"""Refine this meta-prompt based on performance feedback:

Original Meta-Prompt:
{original_prompt}

Performance Feedback:
{performance_feedback}

Create an improved version that addresses the issues while maintaining the structure.

Refined Meta-Prompt:"""
        
        system_prompt = "You are an expert at iterative improvement. Refine meta-prompts to address weaknesses while preserving strengths."
        
        refined = await self.provider.generate(
            prompt=refinement_request,
            system_prompt=system_prompt,
            temperature=0.5
        )
        
        return refined.strip()
    
    async def analyze_content(
        self,
        content: str,
        analysis_type: str = "general",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze content for various purposes
        
        Args:
            content: Content to analyze
            analysis_type: Type of analysis (general, ethics, quality, emotion)
        
        Returns:
            Analysis results
        """
        await self.initialize()
        
        if analysis_type == "ethics":
            analysis_prompt = f"""Analyze this content for ethical considerations:

{content}

Provide:
1. Cultural sensitivity assessment
2. Potential bias detection
3. Age-appropriateness rating
4. Risk flags (if any)
5. Recommendations

Analysis:"""
        
        elif analysis_type == "quality":
            analysis_prompt = f"""Assess the quality of this content:

{content}

Evaluate:
1. Narrative coherence
2. Creative originality
3. Emotional impact
4. Technical execution
5. Overall quality score (0-10)

Assessment:"""
        
        else:  # general
            analysis_prompt = f"""Analyze this content:

{content}

Provide insights on:
1. Main themes
2. Tone and mood
3. Target audience
4. Strengths
5. Areas for improvement

Analysis:"""
        
        system_prompt = "You are an expert content analyst. Provide thorough, objective analysis with specific observations."
        
        analysis = await self.provider.generate(
            prompt=analysis_prompt,
            system_prompt=system_prompt,
            temperature=0.5
        )
        
        return {
            'analysis_type': analysis_type,
            'content': content,
            'analysis': analysis.strip()
        }
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """
        Chat completion for conversational interactions
        
        Args:
            messages: List of message dicts with 'role' and 'content'
        
        Returns:
            Response message
        """
        await self.initialize()
        return await self.provider.chat(messages, **kwargs)
    
    def get_config(self) -> Dict[str, Any]:
        """Get current LLM configuration"""
        return self.config.to_dict()
    
    def get_status(self) -> Dict[str, Any]:
        """Get LLM service status"""
        return {
            'initialized': self._initialized,
            'provider': self.config.provider,
            'model': self.config.model_name,
            'config': self.get_config()
        }


# Global instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get the global LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
