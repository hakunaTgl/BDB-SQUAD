#!/usr/bin/env python3
"""
Test script for Hermes LLM integration
Tests both mock mode and LLM availability detection
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*80)
print("AetherOS Hermes LLM Integration Test")
print("="*80)

# Test 1: Import LLM modules
print("\n[Test 1] Importing LLM modules...")
try:
    from core.llm import LLMConfig, LLMService, get_llm_service
    print("✓ LLM modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test 2: Create configuration
print("\n[Test 2] Creating LLM configuration...")
try:
    config = LLMConfig()
    print(f"✓ Configuration created:")
    print(f"  - Provider: {config.provider}")
    print(f"  - Model: {config.model_name}")
    print(f"  - Temperature: {config.temperature}")
    print(f"  - Max Tokens: {config.max_tokens}")
except Exception as e:
    print(f"✗ Failed to create config: {e}")
    sys.exit(1)

# Test 3: Initialize LLM service
print("\n[Test 3] Initializing LLM service...")
try:
    llm = get_llm_service()
    print("✓ LLM service created")
    
    # Get status
    status = llm.get_status()
    print(f"  - Initialized: {status['initialized']}")
    print(f"  - Provider: {status['provider']}")
    print(f"  - Model: {status['model']}")
except Exception as e:
    print(f"✗ Failed to initialize service: {e}")
    sys.exit(1)

# Test 4: Test async initialization and generation
print("\n[Test 4] Testing LLM generation (mock mode expected)...")
async def test_generation():
    try:
        await llm.initialize()
        print("✓ LLM initialized")
        
        # Test prompt enhancement
        enhanced = await llm.enhance_prompt(
            prompt="A wizard discovers a magical portal",
            style="fantasy",
            emotional_tone="wonder"
        )
        print("✓ Prompt enhancement works:")
        print(f"  Preview: {enhanced[:150]}...")
        
        # Test script generation
        script = await llm.generate_script(
            prompt="A child finds a secret door",
            duration=30,
            style="adventure"
        )
        print("✓ Script generation works:")
        print(f"  Preview: {script[:150]}...")
        
        # Test story decomposition
        scenes = await llm.decompose_story(
            prompt="An astronaut discovers life on Mars",
            duration=60,
            num_scenes=3
        )
        print(f"✓ Story decomposition works: {len(scenes)} scenes generated")
        
        return True
    except Exception as e:
        print(f"✗ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

success = asyncio.run(test_generation())

# Test 5: Integration with aetheros_minimal
print("\n[Test 5] Testing integration with AetherOS...")
try:
    # Import should work even without dependencies
    import aetheros_minimal
    print("✓ aetheros_minimal imports successfully")
    print(f"  - LLM available in module: {aetheros_minimal.LLM_AVAILABLE}")
except Exception as e:
    print(f"✗ Failed to import aetheros_minimal: {e}")
    success = False

# Summary
print("\n" + "="*80)
if success:
    print("✅ All tests passed!")
    print("\nThe Hermes LLM integration is working correctly in mock mode.")
    print("\nTo use actual LLM:")
    print("  1. Install Ollama: https://ollama.ai")
    print("  2. Pull Hermes model: ollama pull hermes2-pro-mistral:latest")
    print("  3. Run AetherOS: python3 aetheros_minimal.py")
    print("\nSee LLM_SETUP.md for detailed instructions.")
else:
    print("❌ Some tests failed - please review errors above")
    sys.exit(1)
print("="*80)
