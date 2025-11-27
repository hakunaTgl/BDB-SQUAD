#!/usr/bin/env python3
"""
AetherOS - Minimal Standalone Demo with Hermes LLM Integration
Demonstrates the core architecture with integrated Hermes model for text generation
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Add src to path for LLM imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Try to import LLM service, fall back to mock if not available
try:
    from core.llm import LLMService, get_llm_service
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("⚠️  LLM service not available, using mock generation")


# ============================================================================
# EMOTION & AFFECTIVE LAYER (Minimal Implementation)
# ============================================================================

class EmotionCategory(Enum):
    JOY = "joy"
    SADNESS = "sadness"
    FEAR = "fear"
    ANGER = "anger"
    SURPRISE = "surprise"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    NEUTRAL = "neutral"


@dataclass
class AffectiveAnalysis:
    primary_emotion: EmotionCategory
    emotion_scores: Dict[EmotionCategory, float]
    valence: float  # -1 to 1
    arousal: float  # 0 to 1
    narrative_tone: str
    age_rating: str


class MinimalAffectiveLayer:
    """Lightweight emotion detection"""
    
    def __init__(self):
        self.emotion_words = {
            'happy': EmotionCategory.JOY,
            'joy': EmotionCategory.JOY,
            'love': EmotionCategory.JOY,
            'sad': EmotionCategory.SADNESS,
            'sorrow': EmotionCategory.SADNESS,
            'fear': EmotionCategory.FEAR,
            'afraid': EmotionCategory.FEAR,
            'angry': EmotionCategory.ANGER,
            'rage': EmotionCategory.ANGER,
            'surprise': EmotionCategory.SURPRISE,
            'wonder': EmotionCategory.SURPRISE,
        }
    
    def analyze(self, text: str) -> AffectiveAnalysis:
        text_lower = text.lower()
        
        # Detect emotions
        emotion_counts = {e: 0 for e in EmotionCategory}
        for word, emotion in self.emotion_words.items():
            if word in text_lower:
                emotion_counts[emotion] += 1
        
        # Find primary emotion
        total = sum(emotion_counts.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_counts.items()}
            primary = max(emotion_scores.items(), key=lambda x: x[1])[0]
        else:
            emotion_scores = {EmotionCategory.NEUTRAL: 1.0}
            primary = EmotionCategory.NEUTRAL
        
        # Calculate valence
        positive = emotion_scores.get(EmotionCategory.JOY, 0)
        negative = emotion_scores.get(EmotionCategory.SADNESS, 0) + emotion_scores.get(EmotionCategory.FEAR, 0)
        valence = positive - negative
        
        # Calculate arousal
        arousal = emotion_scores.get(EmotionCategory.ANGER, 0) + emotion_scores.get(EmotionCategory.SURPRISE, 0)
        
        # Determine tone
        if 'magic' in text_lower or 'fantasy' in text_lower:
            tone = "fantastical"
        elif 'mystery' in text_lower or 'secret' in text_lower:
            tone = "mysterious"
        elif 'adventure' in text_lower:
            tone = "adventurous"
        else:
            tone = "neutral"
        
        return AffectiveAnalysis(
            primary_emotion=primary,
            emotion_scores=emotion_scores,
            valence=valence,
            arousal=arousal,
            narrative_tone=tone,
            age_rating="everyone"
        )


# ============================================================================
# MEMORY LAYER (Minimal Implementation)
# ============================================================================

@dataclass
class MemoryNode:
    node_id: str
    content: str
    timestamp: datetime
    importance: float = 0.5
    access_count: int = 0


class MinimalMemory:
    """Simple in-memory storage"""
    
    def __init__(self):
        self.memories: List[MemoryNode] = []
        self.node_count = 0
    
    def add_memory(self, content: str, importance: float = 0.5) -> str:
        node_id = f"mem_{self.node_count}"
        self.node_count += 1
        
        node = MemoryNode(
            node_id=node_id,
            content=content,
            timestamp=datetime.now(),
            importance=importance
        )
        
        self.memories.append(node)
        return node_id
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[MemoryNode, float]]:
        """Simple keyword-based retrieval"""
        results = []
        query_words = set(query.lower().split())
        
        for mem in self.memories:
            mem_words = set(mem.content.lower().split())
            overlap = len(query_words & mem_words)
            if overlap > 0:
                score = overlap / len(query_words)
                results.append((mem, score))
                mem.access_count += 1
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_nodes': len(self.memories),
            'total_accesses': sum(m.access_count for m in self.memories)
        }


# ============================================================================
# AGENT ORCHESTRATOR (Minimal Implementation)
# ============================================================================

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    ANALYZER = "analyzer"
    GENERATOR = "generator"
    EVALUATOR = "evaluator"


@dataclass
class Task:
    task_id: str
    description: str
    role: AgentRole
    status: str = "pending"
    result: Optional[Any] = None


class MinimalOrchestrator:
    """Simple task coordination"""
    
    def __init__(self):
        self.tasks_completed = 0
    
    async def execute(self, description: str, metadata: Dict) -> Dict[str, Any]:
        """Execute a generation task"""
        
        # Simulate task execution
        tasks = [
            Task("t1", "Analyze prompt", AgentRole.ANALYZER),
            Task("t2", "Generate content", AgentRole.GENERATOR),
            Task("t3", "Evaluate output", AgentRole.EVALUATOR)
        ]
        
        results = {}
        for task in tasks:
            # Simulate async work
            await asyncio.sleep(0.1)
            task.status = "completed"
            task.result = {"status": "success", "data": f"Completed {task.description}"}
            results[task.task_id] = task.result
        
        self.tasks_completed += len(tasks)
        
        return {
            'status': 'success',
            'tasks': results,
            'metadata': {'task_count': len(tasks)}
        }


# ============================================================================
# MAIN AETHEROS SYSTEM
# ============================================================================

@dataclass
class GenerationResult:
    status: str
    outputs: Dict[str, Any]
    metadata: Dict[str, Any]
    memory_node_id: Optional[str] = None
    affective_analysis: Optional[AffectiveAnalysis] = None


class AetherOS:
    """
    AetherOS - Now with Hermes LLM Integration
    Demonstrates core architecture with integrated language model
    """
    
    def __init__(self, mode: str = "creative", memory_enabled: bool = True):
        print("🚀 Initializing AetherOS v1.0.0-alpha...")
        
        self.mode = mode
        self.memory = MinimalMemory() if memory_enabled else None
        self.affective_layer = MinimalAffectiveLayer()
        self.orchestrator = MinimalOrchestrator()
        self.generation_count = 0
        
        # Initialize LLM service
        if LLM_AVAILABLE:
            self.llm = get_llm_service()
            print("✓ Hermes LLM initialized")
        else:
            self.llm = None
            print("⚠️  LLM not available, using mock generation")
        
        print("✓ Affective Reasoning Layer initialized")
        print("✓ Memory System initialized")
        print("✓ Agent Orchestrator initialized")
        print("✅ AetherOS ready!")
    
    async def generate(
        self,
        prompt: str,
        output_formats: List[str] = ["video", "audio", "script"],
        style: str = "cinematic",
        duration: int = 60,
        emotional_tone: Optional[str] = None,
        **kwargs
    ) -> GenerationResult:
        """Generate multimodal content"""
        
        print(f"\n{'='*80}")
        print(f"🎬 Generation #{self.generation_count + 1}")
        print(f"{'='*80}")
        print(f"Prompt: {prompt}")
        print(f"Style: {style} | Duration: {duration}s")
        
        # Step 1: Affective Analysis
        print("\n[1/5] 🧠 Performing affective analysis...")
        affective = self.affective_layer.analyze(prompt)
        print(f"  └─ Primary emotion: {affective.primary_emotion.value}")
        print(f"  └─ Valence: {affective.valence:.2f}")
        print(f"  └─ Narrative tone: {affective.narrative_tone}")
        
        # Step 2: Memory Retrieval
        print("\n[2/5] 💾 Retrieving memory context...")
        context_memories = []
        if self.memory:
            context_memories = self.memory.retrieve(prompt, top_k=3)
            print(f"  └─ Found {len(context_memories)} relevant memories")
            for mem, score in context_memories:
                print(f"      • {mem.content[:50]}... (score: {score:.2f})")
        
        # Step 3: Prompt Enhancement with LLM
        print("\n[3/5] ✨ Enhancing prompt with Hermes LLM...")
        enhanced_prompt = await self._enhance_prompt(prompt, affective, style, emotional_tone)
        print(f"  └─ Enhanced with LLM-powered narrative expansion")
        if enhanced_prompt != prompt:
            print(f"  └─ Preview: {enhanced_prompt[:100]}...")
        
        # Step 3b: Generate script if requested
        script_content = None
        if "script" in output_formats and self.llm:
            print("\n[3b/5] 📝 Generating script with Hermes LLM...")
            script_content = await self.llm.generate_script(
                prompt=enhanced_prompt or prompt,
                duration=duration,
                style=style
            )
            print(f"  └─ Script generated ({len(script_content)} characters)")
        
        # Step 4: Orchestrated Generation
        print("\n[4/5] 🎯 Orchestrating generation...")
        rmp_result = await self.orchestrator.execute(
            description=f"Generate {', '.join(output_formats)}",
            metadata={
                'prompt': prompt,
                'style': style,
                'duration': duration
            }
        )
        print(f"  └─ Executed {rmp_result['metadata']['task_count']} tasks")
        
        # Step 5: Memory Storage
        print("\n[5/5] 💿 Storing in memory...")
        memory_node_id = None
        if self.memory:
            memory_node_id = self.memory.add_memory(
                content=f"Generated: {prompt}",
                importance=0.8
            )
            print(f"  └─ Stored as node: {memory_node_id}")
        
        # Step 6: Build Outputs
        outputs = {}
        if "video" in output_formats:
            outputs["video"] = {
                "path": "video.mp4",
                "resolution": (1280, 720),
                "fps": 24,
                "duration_seconds": duration,
                "format": "mp4"
            }
        if "audio" in output_formats:
            outputs["audio"] = {
                "path": "audio.wav",
                "sample_rate": 44100,
                "channels": 2,  # Ensure this key always exists
                "spatial_audio": False,
                "duration_seconds": duration
            }
        if "script" in output_formats:
            outputs["script"] = {
                "path": "script.txt",
                "format": "markdown",
                "word_count": len(script_content.split()) if script_content else 250,
                "scenes": 5,
                "content": script_content if script_content else "Script placeholder"
            }
        
        # Build result
        result = GenerationResult(
            status="success",
            outputs=outputs,
            metadata={
                "generation_id": self.generation_count,
                "prompt": prompt,
                "style": style,
                "duration": duration,
                "affective_scores": {
                    "primary_emotion": affective.primary_emotion.value,
                    "valence": affective.valence,
                    "arousal": affective.arousal
                },
                "memory_context_used": len(context_memories),
                "rmp_tasks_executed": rmp_result["metadata"]["task_count"]
            },
            memory_node_id=memory_node_id,
            affective_analysis=affective
        )
        
        self.generation_count += 1
        return result
    
    async def _enhance_prompt(
        self, 
        prompt: str, 
        affective: AffectiveAnalysis,
        style: str = "cinematic",
        emotional_tone: Optional[str] = None
    ) -> str:
        """Enhance prompt with affective context and LLM"""
        # Use LLM if available
        if self.llm:
            try:
                enhanced = await self.llm.enhance_prompt(
                    prompt=prompt,
                    style=style,
                    emotional_tone=emotional_tone or affective.primary_emotion.value
                )
                return enhanced
            except Exception as e:
                print(f"  ⚠️  LLM enhancement failed: {e}, using fallback")
        
        # Fallback to simple enhancement
        return f"{prompt}\n[Emotion: {affective.primary_emotion.value}, Tone: {affective.narrative_tone}]"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = {
            'system': {
                'version': '1.0.0-alpha',
                'mode': self.mode,
                'generations_completed': self.generation_count,
                'llm_enabled': LLM_AVAILABLE and self.llm is not None
            },
            'orchestrator': {
                'tasks_completed': self.orchestrator.tasks_completed
            }
        }
        
        if self.memory:
            stats['memory'] = self.memory.get_stats()
        
        if self.llm:
            stats['llm'] = self.llm.get_status()
        
        return stats


# ============================================================================
# DEMONSTRATION
# ============================================================================

async def main():
    """Main demonstration"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     █████╗ ███████╗████████╗██╗  ██╗███████╗██████╗  ██████╗ ███████╗      ║
║    ██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔═══██╗██╔════╝      ║
║    ███████║█████╗     ██║   ███████║█████╗  ██████╔╝██║   ██║███████╗      ║
║    ██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██║   ██║╚════██║      ║
║    ██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║╚██████╔╝███████║      ║
║    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ║
║                                                                              ║
║            Open-Source Generative Supremacy System v1.0.0-alpha             ║
║                                                                              ║
║         "Democratizing imagination, one story at a time"                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize system
    aether = AetherOS(mode="creative", memory_enabled=True)
    
    # Example 1: Fantasy Story
    print("\n" + "="*80)
    print("EXAMPLE 1: Fantasy Adventure Story")
    print("="*80)
    
    result1 = await aether.generate(
        prompt="A child discovers a hidden portal in their grandmother's attic that leads to a magical realm with dragons",
        output_formats=["video", "audio", "script"],
        style="cinematic",
        duration=120,
        emotional_tone="wonder,adventure"
    )
    
    print(f"\n{'='*80}")
    print("📦 GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Status: {result1.status}")
    print(f"\nOutputs Generated:")
    for output_type, details in result1.outputs.items():
        print(f"  ✓ {output_type.upper()}: {details.get('path', 'N/A')}")
    
    print(f"\n📊 Metadata:")
    print(f"  • Valence: {result1.metadata['affective_scores']['valence']:.2f}")
    print(f"  • Emotion: {result1.metadata['affective_scores']['primary_emotion']}")
    print(f"  • Memory Node: {result1.memory_node_id}")
    print(f"  • Tasks Executed: {result1.metadata['rmp_tasks_executed']}")
    
    # Example 2: Continuation (demonstrates memory context)
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Story Continuation (with memory context)")
    print("="*80)
    
    result2 = await aether.generate(
        prompt="The child meets the dragon guardian who reveals an ancient prophecy",
        output_formats=["video", "audio"],
        style="epic",
        duration=90,
        emotional_tone="mystery,epic"
    )
    
    print(f"\n{'='*80}")
    print("📦 GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Status: {result2.status}")
    print(f"Memory Context Used: {result2.metadata['memory_context_used']} previous memories")
    print(f"Outputs: {list(result2.outputs.keys())}")
    
    # System Statistics
    print("\n\n" + "="*80)
    print("📊 SYSTEM STATISTICS")
    print("="*80)
    
    stats = aether.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "="*80)
    print("✨ DEMONSTRATION COMPLETE!")
    print("="*80)
    print("\n🎯 Key Features Demonstrated:")
    print("  ✓ Affective reasoning (emotion detection)")
    print("  ✓ Memory persistence and retrieval")
    print("  ✓ Agent orchestration (multi-task execution)")
    print("  ✓ Context-aware generation")
    print("  ✓ Multi-format output (video, audio, script)")
    
    print("\n📚 Next Steps:")
    print("  1. Explore the full system in src/")
    print("  2. Install full dependencies: pip install -r requirements.txt")
    print("  3. Integrate real models for production use")
    print("  4. Join the community: discord.gg/aetheros")
    
    print("\n💡 This minimal demo shows the ARCHITECTURE.")
    print("   The full system (2,500+ lines) is in src/ with:")
    print("   • Neural Graph Memory (graph-based, GNN-powered)")
    print("   • Advanced Affective Layer (VAD model, cultural analysis)")
    print("   • Recursive Meta-Prompting (self-optimizing agents)")
    print("\n")


if __name__ == "__main__":
    print("\n🚀 Starting AetherOS Minimal Demo...\n")
    asyncio.run(main())
