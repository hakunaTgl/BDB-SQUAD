# AetherOS Next-Gen Roadmap

## Recent Milestone ✅

**Hermes LLM Integration (Completed)**
- ✅ Integrated unfiltered Hermes-2-Pro-Mistral as primary language model
- ✅ LLM-powered prompt enhancement and narrative expansion
- ✅ Script generation with proper formatting and creative direction
- ✅ Story decomposition into structured scenes
- ✅ Intelligent meta-prompting for orchestrator
- ✅ Support for both Ollama (recommended) and HuggingFace backends
- ✅ Graceful fallback to mock mode when LLM unavailable
- ✅ Comprehensive setup documentation

## Guiding Objectives

- **LLM-Powered Intelligence**: Leverage unfiltered Hermes model for creative text generation, narrative structure, and intelligent task planning.
- **Audio-Driven Animation**: Convert spoken or uploaded speech into full-character performances with accurate lip-sync, emotional body language, and camera direction.
- **Storyboarded Video Generation**: Transform long-form narrative prompts into scene-by-scene video plans, render reference frames, and upscale into cohesive sequences.
- **Resource Efficiency**: Deliver high fidelity while staying GPU-friendly through quantization, diffusion-lite backbones, staged rendering, and aggressive caching.
- **Latency & Model Size Management**: Provide tunable presets (ultra, balanced, eco) to balance model footprint, runtime, and output quality.
- **Open & Free**: Keep the stack transparent and community-driven, with clear licensing, model provenance, and contribution guidelines.
- **Competitive Benchmark**: Surpass systems such as pollo.ai by supporting multi-hour productions, granular editing, and hybrid model orchestration without proprietary lock-in.

## Phase 1 – Foundation (Weeks 0-4) ✅ COMPLETE

- ✅ Minimal orchestration demo
- ✅ **Hermes LLM Integration**
- ✅ API contracts for animation/video pipelines (`src/pipelines`)
- ✅ LLM-powered narrative decomposition
- ✅ Comprehensive documentation (LLM_SETUP.md, README.md)
- **Deliverables**:
  - ✅ Define API contracts for animation/video pipelines (`src/pipelines`).
  - ✅ Integrate Hermes LLM for text generation tasks
  - 🔄 Implement plug-in registry in RMP orchestrator for media pipelines.
  - 🔄 Build GPU capability detector and runtime presets.
  - 🔄 Draft spec for real-time creator hub (web + websocket backplane).
  - 🔄 Document open-source governance (LICENSE confirmation, CONTRIBUTING).

## Phase 2 – Audio-Driven Animation Slice (Weeks 4-10)

1. **Speech Ingestion**
   - Whisper small/medium + diarization for transcripts.
   - Emotion estimator (lightweight transformer).
   - **NEW**: LLM-powered dialogue enhancement and emotion analysis
2. **Performance Planning**
   - Viseme mapping + phoneme timing.
   - Gesture & expression curve generator.
   - **NEW**: LLM generates performance notes and emotional beats
3. **Renderer Integration**
   - Modular backends (Did, EMO, SadTalker, bespoke NeRF).
   - Lip-sync refinement pass (Wav2Lip/SyncNet).
4. **Output Packaging**
   - Export MP4/WebM + JSON animation data.
   - Save to asset graph for iterative editing.

## Phase 3 – Storyboarded Video Slice (Weeks 6-14)

1. **Narrative Decomposition** ✅ LLM-POWERED
   - ✅ LLM-based long-form prompt partitioner
   - ✅ Scene metadata: mood, location, characters, transitions
   - Scene breakdown with intelligent pacing
2. **Storyboard Renderer**
   - ControlNet-based frame generation with depth/scribble guidance.
   - Camera and lighting pass.
   - **NEW**: LLM generates visual descriptions for each scene
3. **Sequence Assembly**
   - FPS-normalized shot stitching, cross-fade defaults.
   - Export timeline to creator hub.
4. **Optional Upscaling**
   - Background diffusion upscalers (Real-ESRGAN, StableSR).
   - Frame interpolation (RIFE).

## Phase 4 – Creator Hub & Editing (Weeks 8-18)

- React/Next.js + FastAPI gateway.
- Real-time job monitoring (Celery + Redis + WebSockets).
- Clip preview, keyframe editing, dialogue swap, timeline management.
- Upload panel for audio/video asset ingestion.
- **NEW**: Interactive LLM chat for creative direction and iteration

## Phase 5 – Optimization & Benchmarks (Weeks 12-20)

- Quantize large models (bitsandbytes, GGML) for low-power mode.
- Introduce diffusion distillation (LDM Turbo, Lightning).
- GPU scheduling (Ray Serve) and fallbacks for multi-GPU clusters.
- Benchmark vs pollo.ai on latency, cost, quality.
- **NEW**: Optimize LLM inference with quantization and caching

## Open-Source & Community

- Maintain developer docs in `docs/`.
- Publish model cards for each integrated checkpoint.
- Encourage community pipeline contributions via plugin API.
- **NEW**: Community prompt templates and LLM configurations

---

*This roadmap will evolve; contributions and adjustments are welcome via GitHub issues and pull requests.*
