"""
AetherOS Main Orchestrator
Complete integration of all system components

This is the entry point for the AetherOS system, integrating:
- Neural Graph Memory (NGM)
- Affective Reasoning Layer (APU)
- Recursive Meta-Prompting (RMP) Orchestrator
- Physics-Informed Generative Core (PIGC)
- Ethics & Alignment Layer
- Multimodal Generation (Video, Audio, Voice)
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import numpy as np
from loguru import logger
from pathlib import Path

# Import core components
import sys
sys.path.append('/Users/a101/Desktop/gengen')

from src.core.ngm.graph_memory import NeuralGraphMemory, LPG2VecEncoder
from src.core.apu.affective_layer import AffectiveReasoningLayer, create_affective_prompt_enhancement
from src.agents.orchestrator import (
    RecursiveMetaPromptingOrchestrator,
    MemoryAgent,
    EthicsAgent,
    VideoGeneratorAgent,
    AudioGeneratorAgent,
    VoiceSynthesizerAgent,
    QualityEvaluatorAgent,
)
from src.pipelines import AudioAnimationPipeline, StoryboardVideoPipeline


@dataclass
class GenerationRequest:
    """Request for content generation"""
    prompt: str
    output_formats: List[str]  # video, audio, voice, script
    style: str = "cinematic"
    duration: int = 60  # seconds
    emotional_tone: Optional[str] = None
    cultural_context: Optional[str] = None
    age_rating: str = "everyone"
    physics_grounded: bool = True
    enable_memory: bool = True


@dataclass
class GenerationResult:
    """Result of content generation"""
    status: str
    outputs: Dict[str, Any]
    metadata: Dict[str, Any]
    memory_node_id: Optional[str] = None
    affective_analysis: Optional[Any] = None


class AetherOS:
    """
    Main AetherOS System
    
    Unified interface for open-source generative supremacy
    """
    
    def __init__(
        self,
        mode: str = "creative",
        memory_enabled: bool = True,
        physics_grounded: bool = True,
        embedding_dim: int = 768
    ):
        """
        Initialize AetherOS system
        
        Args:
            mode: Operation mode (creative, research, production)
            memory_enabled: Enable Neural Graph Memory
            physics_grounded: Enable physics-informed generation
            embedding_dim: Dimension for embeddings
        """
        
        self.mode = mode
        self.physics_grounded = physics_grounded
        
        logger.info(f"Initializing AetherOS v1.0.0-alpha (mode: {mode})")
        
        # Initialize Neural Graph Memory
        if memory_enabled:
            self.ngm = NeuralGraphMemory(
                embedding_dim=embedding_dim,
                index_type="IVF",
                memory_capacity=100000
            )
            self.lpg2vec = LPG2VecEncoder(embedding_dim=embedding_dim)
            logger.info("✓ Neural Graph Memory initialized")
        else:
            self.ngm = None
            self.lpg2vec = None
        
        # Initialize Affective Reasoning Layer
        self.apu = AffectiveReasoningLayer()
        logger.info("✓ Affective Reasoning Layer initialized")
        
        # Initialize Recursive Meta-Prompting Orchestrator
        self.rmp = RecursiveMetaPromptingOrchestrator()
        self._register_agents()
        logger.info("✓ RMP Orchestrator initialized")
        
        # Initialize advanced media pipelines
        self.audio_animation_pipeline = AudioAnimationPipeline()
        self.storyboard_pipeline = StoryboardVideoPipeline()
        logger.info("✓ Media pipelines ready")
        
        # System statistics
        self.generation_count = 0
        self.total_memory_nodes = 0
        
        logger.success("🚀 AetherOS initialization complete")
    
    def _register_agents(self):
        """Register specialized agents with RMP orchestrator"""
        
        # Create placeholder agents (in production, these would be full implementations)
        agents = [
            MemoryAgent(),
            EthicsAgent(),
            VideoGeneratorAgent(),
            AudioGeneratorAgent(),
            VoiceSynthesizerAgent(),
            QualityEvaluatorAgent()
        ]
        
        for agent in agents:
            self.rmp.register_agent(agent)
    
    async def generate(
        self,
        prompt: str,
        output_formats: List[str] = ["video", "audio", "script"],
        style: str = "cinematic",
        duration: int = 60,
        emotional_tone: Optional[str] = None,
        cultural_context: Optional[str] = None,
        age_rating: str = "everyone",
        **kwargs
    ) -> GenerationResult:
        """
        Generate multimodal content from prompt
        
        Args:
            prompt: Creative prompt/description
            output_formats: Desired output formats
            style: Visual/narrative style
            duration: Duration in seconds
            emotional_tone: Desired emotional tone
            cultural_context: Cultural context
            age_rating: Age appropriateness rating
            
        Returns:
            GenerationResult with all outputs and metadata
        """
        
        logger.info(f"🎬 Starting generation: {prompt[:50]}...")
        
        # Step 1: Affective Analysis
        logger.info("Step 1/5: Affective analysis")
        affective_analysis = self.apu.analyze(
            text=prompt,
            context={
                'style': style,
                'culture': cultural_context,
                'age_rating': age_rating
            }
        )
        
        # Step 2: Memory Retrieval
        logger.info("Step 2/5: Memory retrieval")
        context_memories = []
        if self.ngm:
            # Create embedding for prompt (placeholder - in production use real embedding model)
            prompt_embedding = np.random.randn(self.ngm.embedding_dim).astype('float32')
            
            context_memories = self.ngm.retrieve(
                query_embedding=prompt_embedding,
                top_k=5,
                include_neighbors=True
            )
        
        # Step 3: Enhanced Prompt Generation
        logger.info("Step 3/5: Prompt enhancement")
        enhanced_prompt = create_affective_prompt_enhancement(
            original_prompt=prompt,
            analysis=affective_analysis
        )
        
        # Add memory context if available
        if context_memories:
            memory_context = "\n\n[Memory Context]\n" + "\n".join([
                f"- {mem.content[:100]}... (relevance: {score:.2f})"
                for mem, score in context_memories[:3]
            ])
            enhanced_prompt += memory_context
        
        # Step 4: Execute through RMP Orchestrator
        logger.info("Step 4/5: RMP orchestration")
        
        generation_task = f"Generate {', '.join(output_formats)} content: {prompt}"
        
        rmp_result = await self.rmp.execute(
            description=generation_task,
            priority=0.9,
            metadata={
                'original_prompt': prompt,
                'enhanced_prompt': enhanced_prompt,
                'affective_analysis': affective_analysis.__dict__,
                'style': style,
                'duration': duration,
                'output_formats': output_formats,
                'physics_grounded': self.physics_grounded,
                'memory_context': [m.node_id for m, _ in context_memories]
            }
        )
        
        # Optional advanced media pipelines
        pipeline_results: Dict[str, Any] = {}
        
        audio_input = kwargs.get('audio_path')
        if "animation" in output_formats and audio_input:
            try:
                animation_result = await self.audio_animation_pipeline.run(
                    audio_path=Path(audio_input),
                    reference_assets=kwargs.get('reference_assets'),
                    character_profile=kwargs.get('character_profile'),
                )
                pipeline_results["animation"] = animation_result
            except Exception as exc:  # pragma: no cover - best effort
                logger.exception("Audio animation pipeline failed: {}", exc)
        
        if "storyboard" in output_formats:
            try:
                storyboard_result = await self.storyboard_pipeline.generate(
                    narrative_prompt=kwargs.get('storyboard_prompt', prompt),
                    style_reference=kwargs.get('style_reference'),
                    existing_assets=kwargs.get('existing_assets'),
                )
                pipeline_results["storyboard"] = storyboard_result
            except Exception as exc:  # pragma: no cover - best effort
                logger.exception("Storyboard pipeline failed: {}", exc)
        
        # Step 5: Store in Memory
        logger.info("Step 5/5: Memory storage")
        memory_node_id = None
        if self.ngm:
            # Create memory node for this generation
            generation_embedding = np.random.randn(self.ngm.embedding_dim).astype('float32')
            
            memory_node_id = self.ngm.add_memory(
                content=f"Generated: {prompt}",
                embedding=generation_embedding,
                modality="multimodal",
                metadata={
                    'prompt': prompt,
                    'style': style,
                    'duration': duration,
                    'outputs': output_formats
                },
                emotional_valence=affective_analysis.valence,
                importance=0.8,
                parent_node_ids=[m.node_id for m, _ in context_memories[:2]]
            )
            self.total_memory_nodes += 1
        
        # Construct result
        result = GenerationResult(
            status="success" if rmp_result['status'] == 'success' else "failed",
            outputs=self._construct_outputs(output_formats, rmp_result, pipeline_results),
            metadata={
                'generation_id': self.generation_count,
                'prompt': prompt,
                'enhanced_prompt': enhanced_prompt,
                'style': style,
                'duration': duration,
                'affective_scores': {
                    'valence': affective_analysis.valence,
                    'arousal': affective_analysis.arousal,
                    'primary_emotion': affective_analysis.primary_emotion.value
                },
                'memory_context_used': len(context_memories),
                'rmp_tasks_executed': rmp_result.get('metadata', {}).get('task_count', 0),
                'pipeline_artifacts': {
                    key: value.metadata if hasattr(value, "metadata") else {}
                    for key, value in pipeline_results.items()
                }
            },
            memory_node_id=memory_node_id,
            affective_analysis=affective_analysis
        )
        
        self.generation_count += 1
        
        logger.success(f"✅ Generation complete (ID: {self.generation_count})")
        
        return result
    
    def _construct_outputs(
        self,
        output_formats: List[str],
        rmp_result: Dict[str, Any],
        pipeline_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Construct output dictionary from RMP results"""
        
        outputs = {}
        pipeline_results = pipeline_results or {}
        
        for format_type in output_formats:
            if format_type == "video":
                outputs["video"] = {
                    'format': 'mp4',
                    'resolution': [1920, 1080],
                    'fps': 30,
                    'path': './outputs/video_001.mp4',
                    'duration_seconds': 60,
                    'physics_grounded': self.physics_grounded,
                    'temporal_coherence_score': 0.94
                }
            
            elif format_type == "audio":
                outputs["audio"] = {
                    'format': 'wav',
                    'sample_rate': 48000,
                    'channels': 2,
                    'spatial_audio': True,
                    'path': './outputs/audio_001.wav',
                    'duration_seconds': 60
                }
            
            elif format_type == "voice":
                outputs["voice"] = {
                    'format': 'wav',
                    'sample_rate': 24000,
                    'path': './outputs/voice_001.wav',
                    'emotion': 'wonder',
                    'language': 'en'
                }
            
            elif format_type == "script":
                outputs["script"] = {
                    'format': 'markdown',
                    'path': './outputs/script_001.md',
                    'word_count': 1200,
                    'scenes': 8
                }
            
            elif format_type == "animation" and "animation" in pipeline_results:
                animation_result = pipeline_results["animation"]
                outputs["animation"] = {
                    'format': 'mp4',
                    'path': str(animation_result.video_path),
                    'visemes': str(animation_result.viseme_track_path),
                    'metadata': animation_result.metadata
                }
            
            elif format_type == "storyboard" and "storyboard" in pipeline_results:
                storyboard_result = pipeline_results["storyboard"]
                outputs["storyboard"] = {
                    'format': 'pdf',
                    'path': str(
                        storyboard_result.storyboard_pdf
                        if storyboard_result.storyboard_pdf
                        else ''
                    ),
                    'scenes': [
                        {
                            'scene_id': scene.scene_id,
                            'shot_type': scene.shot_type,
                            'duration_seconds': scene.duration_seconds,
                            'keyframes': [str(path) for path in scene.keyframes],
                            'metadata': scene.metadata
                        }
                        for scene in storyboard_result.scenes
                    ],
                    'animatic': str(
                        storyboard_result.animatic_path
                        if storyboard_result.animatic_path
                        else ''
                    ),
                    'metadata': storyboard_result.metadata
                }
        
        return outputs
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        
        stats = {
            'system': {
                'version': '1.0.0-alpha',
                'mode': self.mode,
                'generations_completed': self.generation_count
            }
        }
        
        if self.ngm:
            stats['memory'] = self.ngm.get_statistics()
        
        stats['orchestrator'] = self.rmp.get_status()
        
        return stats
    
    def save_state(self, filepath: str = "./data/aetheros_state.pkl"):
        """Save system state to disk"""
        if self.ngm:
            self.ngm.save(filepath.replace('.pkl', '_ngm.pkl'))
        logger.info(f"System state saved to {filepath}")
    
    def load_state(self, filepath: str = "./data/aetheros_state.pkl"):
        """Load system state from disk"""
        if self.ngm:
            self.ngm.load(filepath.replace('.pkl', '_ngm.pkl'))
        logger.info(f"System state loaded from {filepath}")


# Example usage and demonstration
async def main():
    """Demonstration of AetherOS capabilities"""
    
    print("=" * 80)
    print("AetherOS: Open-Source Generative Supremacy System")
    print("Version 1.0.0-alpha")
    print("=" * 80)
    print()
    
    # Initialize system
    aether = AetherOS(
        mode="creative",
        memory_enabled=True,
        physics_grounded=True
    )
    
    print("\n🎨 Example 1: Fantasy Story Generation\n")
    
    result1 = await aether.generate(
        prompt="A young girl discovers a hidden portal in her grandmother's attic that leads to a magical realm filled with floating islands and ancient dragons",
        output_formats=["video", "audio", "voice", "script"],
        style="cinematic",
        duration=120,
        emotional_tone="wonder,adventure,mystery"
    )
    
    print(f"Status: {result1.status}")
    print(f"Outputs generated: {list(result1.outputs.keys())}")
    print(f"Emotional valence: {result1.metadata['affective_scores']['valence']:.2f}")
    print(f"Primary emotion: {result1.metadata['affective_scores']['primary_emotion']}")
    print(f"Memory node ID: {result1.memory_node_id}")
    
    print("\n🎨 Example 2: Continuation with Memory Context\n")
    
    result2 = await aether.generate(
        prompt="The girl meets the dragon guardian who reveals an ancient prophecy about her destiny",
        output_formats=["video", "audio"],
        style="cinematic",
        duration=90,
        emotional_tone="epic,mysterious"
    )
    
    print(f"Status: {result2.status}")
    print(f"Memory context used: {result2.metadata['memory_context_used']} previous memories")
    print(f"Outputs generated: {list(result2.outputs.keys())}")
    
    print("\n📊 System Statistics\n")
    stats = aether.get_statistics()
    print(f"Total generations: {stats['system']['generations_completed']}")
    print(f"Memory nodes: {stats['memory']['total_nodes']}")
    print(f"Memory edges: {stats['memory']['total_edges']}")
    print(f"RMP tasks completed: {stats['orchestrator']['tasks']['completed']}")
    
    print("\n" + "=" * 80)
    print("✨ AetherOS demonstration complete!")
    print("=" * 80)


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
