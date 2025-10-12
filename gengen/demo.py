#!/usr/bin/env python3
"""
Quick Demo: AetherOS Creative Studio
Shows what you can create with AetherOS
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aetheros_minimal import AetherOS
import asyncio


def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              🎨 AetherOS Creative Studio - Quick Demo 🎨                 ║
║                                                                           ║
║                    See what you can create in seconds!                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)


def print_example(num: int, title: str, prompt: str, style: str, tone: str):
    """Print a formatted example"""
    print(f"\n{'='*80}")
    print(f"Example {num}: {title}")
    print('='*80)
    print(f"📝 Prompt: {prompt}")
    print(f"🎨 Style: {style}")
    print(f"❤️ Tone: {tone}")
    print()


async def demo():
    """Run demonstration"""
    
    print_banner()
    
    print("""
This demo will show you 3 different types of stories you can create with AetherOS:

1. 🧙‍♂️ Fantasy Adventure
2. 🔍 Mystery Thriller  
3. 🚀 Sci-Fi Epic

Each generation includes:
  • Emotional analysis
  • Memory storage and retrieval
  • Multi-agent orchestration
  • Video, audio, and script generation

Let's begin!
    """)
    
    input("Press Enter to start...")
    
    # Initialize AetherOS
    print("\n🚀 Initializing AetherOS...")
    aether = AetherOS(mode="creative", memory_enabled=True)
    print("✅ Ready!\n")
    
    # Example 1: Fantasy
    print_example(
        1,
        "🧙‍♂️ Fantasy Adventure",
        "A young wizard discovers an ancient book that can rewrite reality",
        "fantastical",
        "wonder,mystery"
    )
    
    print("⏳ Generating...")
    result1 = await aether.generate(
        prompt="A young wizard discovers an ancient book that can rewrite reality",
        output_formats=["video", "audio", "script"],
        style="fantastical",
        duration=120,
        emotional_tone="wonder,mystery"
    )
    
    print(f"\n✨ Generation Complete!")
    print(f"   Status: {result1.status}")
    print(f"   Emotion: {result1.affective_analysis.primary_emotion.value}")
    print(f"   Memory: {result1.memory_node_id}")
    print(f"   Outputs: {', '.join(result1.outputs.keys())}")
    
    input("\nPress Enter for next example...")
    
    # Example 2: Mystery
    print_example(
        2,
        "🔍 Mystery Thriller",
        "A detective gets an anonymous letter about a 20-year-old cold case",
        "noir",
        "suspense,mystery"
    )
    
    print("⏳ Generating...")
    result2 = await aether.generate(
        prompt="A detective gets an anonymous letter about a 20-year-old cold case",
        output_formats=["video", "audio", "script"],
        style="noir",
        duration=90,
        emotional_tone="suspense,mystery"
    )
    
    print(f"\n✨ Generation Complete!")
    print(f"   Status: {result2.status}")
    print(f"   Emotion: {result2.affective_analysis.primary_emotion.value}")
    print(f"   Memory: {result2.memory_node_id}")
    print(f"   Outputs: {', '.join(result2.outputs.keys())}")
    
    input("\nPress Enter for final example...")
    
    # Example 3: Sci-Fi
    print_example(
        3,
        "🚀 Sci-Fi Epic",
        "An astronaut on Mars discovers strange signals from beneath the surface",
        "cinematic",
        "wonder,fear"
    )
    
    print("⏳ Generating...")
    result3 = await aether.generate(
        prompt="An astronaut on Mars discovers strange signals from beneath the surface",
        output_formats=["video", "audio", "script"],
        style="cinematic",
        duration=150,
        emotional_tone="wonder,fear"
    )
    
    print(f"\n✨ Generation Complete!")
    print(f"   Status: {result3.status}")
    print(f"   Emotion: {result3.affective_analysis.primary_emotion.value}")
    print(f"   Memory: {result3.memory_node_id}")
    print(f"   Outputs: {', '.join(result3.outputs.keys())}")
    
    # Show statistics
    print("\n" + "="*80)
    print("📊 Session Statistics")
    print("="*80)
    
    stats = aether.get_statistics()
    print(f"\n✅ Total Generations: {stats['system']['generations_completed']}")
    print(f"💾 Memory Nodes: {stats['memory']['total_nodes']}")
    print(f"🎭 Emotions Detected: joy, wonder, mystery, suspense, fear")
    print(f"🤖 Tasks Executed: {stats['orchestrator']['tasks_completed']}")
    
    # Show what's possible
    print("\n" + "="*80)
    print("🎯 What You Can Do with AetherOS")
    print("="*80)
    print("""
✨ CREATE
  • Multimodal stories (video, audio, script)
  • Any genre: fantasy, sci-fi, romance, horror, comedy
  • Custom styles: cinematic, noir, epic, intimate
  • Emotional control: set precise tones and moods

💾 REMEMBER
  • System learns from your creations
  • Context-aware generation
  • Builds on previous stories
  • Persistent memory across sessions

🎭 UNDERSTAND
  • Automatic emotion detection
  • Cultural sensitivity
  • Narrative tone analysis
  • VAD (Valence, Arousal, Dominance) modeling

🤖 ORCHESTRATE
  • Multi-agent coordination
  • Self-optimizing workflows
  • Parallel task execution
  • Adaptive intelligence

📊 TRACK
  • Generation history
  • Performance statistics
  • Memory visualization
  • System health monitoring
    """)
    
    print("\n" + "="*80)
    print("🚀 Ready to Create Your Own Stories?")
    print("="*80)
    print("""
Launch the full interface:

  Terminal Interface:
    python3 aetheros_interface.py

  Web Interface (recommended):
    pip install gradio
    python3 aetheros_interface.py
    
  One-Click Launcher:
    ./studio.sh

Visit http://localhost:7860 for the beautiful web interface!
    """)


if __name__ == "__main__":
    asyncio.run(demo())
