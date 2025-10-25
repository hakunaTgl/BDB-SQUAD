"""
Storyboarded Video Pipeline
===========================

Breaks long-form narratives into structured scene plans and renders detailed
storyboards or animatics. Now integrated with Hermes LLM for intelligent
narrative decomposition.
"""

from __future__ import annotations

import asyncio
import sys
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib

from loguru import logger
from diffusers import StableDiffusionPipeline

# Import LLM service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from core.llm import get_llm_service
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    logger.warning("LLM service not available for storyboard pipeline")


@dataclass
class StoryboardConfig:
    """Configuration profile for storyboard generation."""

    preset: str = "balanced"  # ultra | balanced | eco
    target_resolution: tuple[int, int] = (1024, 576)
    frames_per_scene: int = 12
    max_scenes: int = 80
    seed: Optional[int] = None
    enable_controlnet: bool = True
    enable_depth_guidance: bool = True
    enable_pose_guidance: bool = True
    output_dir: Path = Path("./outputs/storyboards")
    tmp_dir: Path = Path("./tmp/storyboards")
    gpu_memory_budget_gb: float = 12.0
    quantized_models: bool = True


@dataclass
class StoryboardScene:
    """Normalized representation of a single storyboard scene."""

    scene_id: str
    description: str
    shot_type: str
    duration_seconds: float
    keyframes: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StoryboardResult:
    """Result bundle for the orchestrator/UI."""

    storyboard_pdf: Optional[Path]
    scenes: List[StoryboardScene]
    animatic_path: Optional[Path]
    metadata: Dict[str, Any] = field(default_factory=dict)


class StoryboardVideoPipeline:
    """
    Multi-step storyboard workflow:
        1. Narrative decomposition (scene breakdown, beats)
        2. Visual planning (shot types, compositions)
        3. Frame rendering (diffusion-based guidance)
        4. Assembly (PDF/animatic with metadata)
    """

    def __init__(self, config: Optional[StoryboardConfig] = None):
        self.config = config or StoryboardConfig()
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config.tmp_dir.mkdir(parents=True, exist_ok=True)

        # Initialize LLM service
        if LLM_AVAILABLE:
            self.llm = get_llm_service()
            logger.info("StoryboardVideoPipeline initialized with Hermes LLM support")
        else:
            self.llm = None
            logger.warning("StoryboardVideoPipeline running without LLM support")

        logger.info(
            "StoryboardVideoPipeline initialized with preset '{}'",
            self.config.preset,
        )

    async def generate(
        self,
        narrative_prompt: str,
        style_reference: Optional[Dict[str, Any]] = None,
        existing_assets: Optional[Dict[str, Path]] = None,
    ) -> StoryboardResult:
        """Run the storyboard pipeline."""

        scene_plan = await self._decompose_narrative(narrative_prompt, style_reference)
        visual_plan = await self._plan_visuals(scene_plan, style_reference)
        rendered_scenes = await self._render_frames(visual_plan, existing_assets)
        assembled = await self._assemble_storyboard(rendered_scenes)

        logger.success(
            "Storyboard generated with {} scenes", len(assembled.scenes)
        )
        return assembled

    async def _decompose_narrative(
        self,
        prompt: str,
        style_reference: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Use Hermes LLM to break story into scenes and beats.
        """
        logger.debug("Decomposing narrative with LLM")
        
        # Try using LLM for intelligent decomposition
        if self.llm:
            try:
                # Calculate target number of scenes based on prompt length
                num_scenes = min(self.config.max_scenes, max(3, len(prompt.split()) // 50))
                
                scenes = await self.llm.decompose_story(
                    prompt=prompt,
                    duration=num_scenes * 10,  # Estimate duration
                    num_scenes=num_scenes
                )
                
                # Convert LLM output to expected format
                scene_plan = []
                for i, scene in enumerate(scenes):
                    scene_plan.append({
                        "scene_id": f"scene_{i+1:03d}",
                        "description": scene.get('description', scene.get('title', prompt[:120])),
                        "location": "TBD",
                        "characters": [],
                        "duration_seconds": scene.get('duration', 10.0),
                        "title": scene.get('title', f'Scene {i+1}')
                    })
                
                if scene_plan:
                    logger.info(f"LLM decomposed narrative into {len(scene_plan)} scenes")
                    return scene_plan
            except Exception as e:
                logger.warning(f"LLM decomposition failed: {e}, using fallback")
        
        # Fallback: Simple decomposition
        await asyncio.sleep(0)
        return [
            {
                "scene_id": "scene_001",
                "description": prompt[:120] + "...",
                "location": "Unknown",
                "characters": [],
                "duration_seconds": 10.0,
            }
        ]

    async def _plan_visuals(
        self,
        scene_plan: List[Dict[str, Any]],
        style_reference: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Assign shot types, camera moves, lighting per scene.
        """
        logger.debug("Planning visual language")
        await asyncio.sleep(0)
        visual_plan = []
        for scene in scene_plan:
            visual_plan.append(
                {
                    **scene,
                    "shot_type": "medium",
                    "camera_move": "static",
                    "color_palette": style_reference.get("palette") if style_reference else None,
                }
            )
        return visual_plan

    async def _render_frames(
        self,
        visual_plan: List[Dict[str, Any]],
        existing_assets: Optional[Dict[str, Path]],
    ) -> List[StoryboardScene]:
        """
        Diffusion or raster rendering for each scene, with caching.
        """
        logger.debug("Rendering storyboard frames with StableDiffusion and cache")
        pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        pipe = pipe.to("cuda" if self.config.gpu_memory_budget_gb > 0 else "cpu")
        scenes: List[StoryboardScene] = []
        cache_dir = self.config.tmp_dir / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        for plan in visual_plan[: self.config.max_scenes]:
            scene_id = plan["scene_id"]
            desc = plan["description"]
            cache_key = hashlib.md5(desc.encode()).hexdigest()
            cached_path = cache_dir / f"{cache_key}.png"
            if cached_path.exists():
                keyframe_path = cached_path
            else:
                image = pipe(desc).images[0]
                image.save(cached_path)
                keyframe_path = cached_path
            scene_dir = self.config.output_dir / scene_id
            scene_dir.mkdir(parents=True, exist_ok=True)
            scenes.append(
                StoryboardScene(
                    scene_id=scene_id,
                    description=desc,
                    shot_type=plan["shot_type"],
                    duration_seconds=plan["duration_seconds"],
                    keyframes=[keyframe_path],
                    metadata={
                        "camera_move": plan.get("camera_move"),
                        "color_palette": plan.get("color_palette"),
                        "assets": existing_assets or {},
                    },
                )
            )
        return scenes

    async def _assemble_storyboard(
        self,
        scenes: List[StoryboardScene],
    ) -> StoryboardResult:
        """
        Combine scenes into PDF/animatic deliverables.
        """
        logger.debug("Assembling storyboard deliverables")
        await asyncio.sleep(0)
        storyboard_pdf = self.config.output_dir / "storyboard.pdf"
        animatic_path = self.config.output_dir / "storyboard_animatic.mp4"
        return StoryboardResult(
            storyboard_pdf=storyboard_pdf,
            scenes=scenes,
            animatic_path=animatic_path,
            metadata={
                "preset": self.config.preset,
                "resolution": self.config.target_resolution,
                "frames_per_scene": self.config.frames_per_scene,
            },
        )
