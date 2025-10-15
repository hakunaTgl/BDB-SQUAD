#!/usr/bin/env python3
"""
AetherOS Quick Start Script
Minimal, production-ready demo for creative storytelling
"""

import asyncio
import sys
import os
from aetheros_minimal import AetherOS

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def quick_start():
    print("\nAetherOS: Open-Source Generative Supremacy System v1.0.0-alpha\n")
    print("Initializing...")
    
    # Initialize system
    aether = AetherOS(
        mode="creative",
        memory_enabled=True
    )
    
    print("✅ Ready!")
    print("\nGenerating cinematic story...")
    
    # Generate content
    result = await aether.generate(
        prompt="A child discovers a hidden portal in their grandmother's attic",
        output_formats=["video", "audio", "script"],
        style="cinematic",
        duration=120,
        emotional_tone="wonder,mystery"
    )
    
    print("\n--- Generation Complete ---")
    print(f"Status: {result.status}")
    print(f"Outputs: {', '.join(result.outputs.keys())}")
    print(f"Primary Emotion: {result.metadata['affective_scores']['primary_emotion']}")
    print(f"Memory Node: {result.memory_node_id}")
    print(f"Tasks Executed: {result.metadata['rmp_tasks_executed']}")
    
    stats = aether.get_statistics()
    print(f"Generations: {stats['system']['generations_completed']}")
    print(f"Memory Nodes: {stats['memory']['total_nodes']}")
    print("\nAetherOS demo complete.\n")


if __name__ == "__main__":
    asyncio.run(quick_start())
