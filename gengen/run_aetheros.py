#!/usr/bin/env python3
"""
AetherOS Quick Start Script
Initialize and run the complete system (Standalone Version)
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def quick_start():
    """Quick start demo"""
    
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
║               Open-Source Generative Supremacy System v1.0.0-alpha          ║
║                                                                              ║
║    "Democratizing imagination, one story at a time"                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Initializing AetherOS...\n")
    
    # Initialize system
    aether = AetherOS(
        mode="creative",
        memory_enabled=True,
        physics_grounded=True
    )
    
    print("\n✅ System ready!\n")
    print("=" * 80)
    print("GENERATING: Cinematic Story")
    print("=" * 80)
    
    # Generate content
    result = await aether.generate(
        prompt="A child discovers a hidden portal in their grandmother's attic",
        output_formats=["video", "audio", "script"],
        style="cinematic",
        duration=120,
        emotional_tone="wonder,mystery"
    )
    
    print("\n" + "=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nStatus: {result.status}")
    print(f"\nOutputs Generated:")
    for output_type, details in result.outputs.items():
        print(f"  ✓ {output_type.upper()}: {details.get('path', 'N/A')}")
    
    print(f"\nEmotional Analysis:")
    print(f"  Valence: {result.metadata['affective_scores']['valence']:.2f}")
    print(f"  Arousal: {result.metadata['affective_scores']['arousal']:.2f}")
    print(f"  Primary Emotion: {result.metadata['affective_scores']['primary_emotion']}")
    
    print(f"\nMemory:")
    print(f"  Node ID: {result.memory_node_id}")
    print(f"  Context Used: {result.metadata['memory_context_used']} memories")
    
    print(f"\nOrchestration:")
    print(f"  RMP Tasks: {result.metadata['rmp_tasks_executed']}")
    
    print("\n" + "=" * 80)
    print("System Statistics:")
    print("=" * 80)
    
    stats = aether.get_statistics()
    print(f"  Generations: {stats['system']['generations_completed']}")
    print(f"  Memory Nodes: {stats['memory']['total_nodes']}")
    print(f"  Graph Density: {stats['memory']['graph_density']:.4f}")
    
    print("\n✨ AetherOS demonstration complete!")
    print("\nNext steps:")
    print("  1. Explore examples/ directory for more use cases")
    print("  2. Read docs/architecture/ for technical details")
    print("  3. Join community at discord.gg/aetheros")
    print("\n")


if __name__ == "__main__":
    asyncio.run(quick_start())
