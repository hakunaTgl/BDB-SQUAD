#!/usr/bin/env python3
"""
AetherOS Web Interface
Beautiful GUI for creating, editing, and viewing AI-generated content
No coding required!
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check if gradio is available, if not use built-in interface
try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False
    print("⚠️  Gradio not installed. Using minimal interface.")
    print("💡 Install with: pip install gradio")


# Import our minimal AetherOS system
from aetheros_minimal import AetherOS, GenerationResult


class AetherOSInterface:
    """Web interface for AetherOS"""
    
    def __init__(self):
        self.aether = AetherOS(mode="creative", memory_enabled=True)
        self.generation_history = []
        self.current_generation = None
        
        print("🎨 AetherOS Interface initialized!")
    
    def generate_content(
        self,
        prompt: str,
        style: str,
        duration: int,
        emotional_tone: str,
        output_video: bool,
        output_audio: bool,
        output_script: bool
    ) -> tuple:
        """Generate content from prompt"""
        
        if not prompt:
            return "❌ Please enter a prompt!", "", "", ""
        
        # Build output formats
        output_formats = []
        if output_video:
            output_formats.append("video")
        if output_audio:
            output_formats.append("audio")
        if output_script:
            output_formats.append("script")
        
        if not output_formats:
            return "❌ Please select at least one output format!", "", "", ""
        
        # Generate
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.aether.generate(
                    prompt=prompt,
                    output_formats=output_formats,
                    style=style,
                    duration=duration,
                    emotional_tone=emotional_tone
                )
            )
            loop.close()
            
            # Store in history
            self.generation_history.append(result)
            self.current_generation = result
            
            # Build output display
            status_text = f"""
✅ **Generation Complete!**

**ID:** {result.metadata['generation_id']}
**Status:** {result.status}
**Prompt:** {prompt}

---

### 🎭 Emotional Analysis
- **Primary Emotion:** {result.metadata['affective_scores']['primary_emotion']}
- **Valence:** {result.metadata['affective_scores']['valence']:.2f}
- **Arousal:** {result.metadata['affective_scores']['arousal']:.2f}

### 💾 Memory
- **Node ID:** {result.memory_node_id}
- **Context Used:** {result.metadata['memory_context_used']} previous memories

### 🎯 Orchestration
- **Tasks Executed:** {result.metadata['rmp_tasks_executed']}

---
"""
            
            # Build outputs display
            outputs_display = "### 📦 Generated Outputs\n\n"
            for output_type, details in result.outputs.items():
                outputs_display += f"**{output_type.upper()}:**\n"
                for key, value in details.items():
                    outputs_display += f"  - {key}: `{value}`\n"
                outputs_display += "\n"
            
            # Build preview
            preview_text = self._build_preview(result)
            
            # Build metadata JSON
            metadata_json = json.dumps(result.metadata, indent=2, default=str)
            
            return status_text, outputs_display, preview_text, metadata_json
            
        except Exception as e:
            return f"❌ Error: {str(e)}", "", "", ""
    
    def _build_preview(self, result: GenerationResult) -> str:
        """Build a text preview of the generation"""
        
        preview = f"""
# 🎬 Generation Preview

## Story Concept
{result.metadata['prompt']}

## Style & Mood
- **Visual Style:** {result.metadata['style']}
- **Duration:** {result.metadata['duration']} seconds
- **Emotional Tone:** {result.affective_analysis.primary_emotion.value}
- **Narrative Style:** {result.affective_analysis.narrative_tone}

## Generated Content

### 📹 Video
"""
        
        if 'video' in result.outputs:
            video = result.outputs['video']
            preview += f"""
- Resolution: {video['resolution'][0]}x{video['resolution'][1]}
- Frame Rate: {video['fps']} fps
- Duration: {video['duration_seconds']}s
- Format: {video['format']}
"""
        
        if 'audio' in result.outputs:
            audio = result.outputs['audio']
            preview += f"""

### 🎵 Audio
- Sample Rate: {audio['sample_rate']} Hz
- Channels: {audio['channels']}
- Spatial Audio: {'Yes' if audio['spatial_audio'] else 'No'}
- Duration: {audio['duration_seconds']}s
"""
        
        if 'script' in result.outputs:
            script = result.outputs['script']
            preview += f"""

### 📝 Script
- Format: {script['format']}
- Word Count: ~{script['word_count']} words
- Scenes: {script.get('scenes', 'N/A')}
"""
        
        preview += f"""

---

*Generated by AetherOS v1.0.0-alpha*
*Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return preview
    
    def get_history(self) -> str:
        """Get generation history"""
        
        if not self.generation_history:
            return "No generations yet. Create your first story!"
        
        history_text = "# 📚 Generation History\n\n"
        
        for i, result in enumerate(reversed(self.generation_history)):
            history_text += f"""
## Generation #{result.metadata['generation_id']}
- **Prompt:** {result.metadata['prompt'][:100]}...
- **Status:** {result.status}
- **Emotion:** {result.metadata['affective_scores']['primary_emotion']}
- **Outputs:** {', '.join(result.outputs.keys())}
- **Memory Node:** {result.memory_node_id}

---
"""
        
        return history_text
    
    def get_statistics(self) -> str:
        """Get system statistics"""
        
        stats = self.aether.get_statistics()
        
        stats_text = f"""
# 📊 System Statistics

## System
- **Version:** {stats['system']['version']}
- **Mode:** {stats['system']['mode']}
- **Total Generations:** {stats['system']['generations_completed']}

## Memory
- **Total Nodes:** {stats['memory']['total_nodes']}
- **Total Accesses:** {stats['memory']['total_accesses']}

## Orchestrator
- **Tasks Completed:** {stats['orchestrator']['tasks_completed']}

---

*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return stats_text


def create_gradio_interface():
    """Create Gradio web interface"""
    
    interface = AetherOSInterface()
    
    # Custom CSS
    custom_css = """
    .gradio-container {
        font-family: 'Inter', sans-serif;
    }
    .output-markdown {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    """
    
    with gr.Blocks(
        theme=gr.themes.Soft(primary_hue="purple", secondary_hue="blue"),
        css=custom_css,
        title="AetherOS - Creative AI Studio"
    ) as demo:
        
        # Header
        gr.Markdown("""
# 🎨 AetherOS Creative Studio
### *Democratizing imagination, one story at a time*

Create stunning multimodal content with AI-powered storytelling.
No coding required—just your imagination!
        """)
        
        with gr.Tabs():
            
            # ============= CREATE TAB =============
            with gr.Tab("✨ Create"):
                gr.Markdown("## Generate Your Story")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        prompt_input = gr.Textbox(
                            label="Story Prompt",
                            placeholder="A child discovers a hidden portal in their grandmother's attic...",
                            lines=4
                        )
                        
                        with gr.Row():
                            style_input = gr.Dropdown(
                                choices=[
                                    "cinematic",
                                    "fantastical",
                                    "noir",
                                    "epic",
                                    "intimate",
                                    "comedic",
                                    "horror",
                                    "documentary"
                                ],
                                value="cinematic",
                                label="Visual Style"
                            )
                            
                            duration_input = gr.Slider(
                                minimum=30,
                                maximum=300,
                                value=120,
                                step=30,
                                label="Duration (seconds)"
                            )
                        
                        emotional_tone_input = gr.Textbox(
                            label="Emotional Tone (comma-separated)",
                            placeholder="wonder,mystery,adventure",
                            value="wonder"
                        )
                        
                        gr.Markdown("### Output Formats")
                        with gr.Row():
                            video_checkbox = gr.Checkbox(label="📹 Video", value=True)
                            audio_checkbox = gr.Checkbox(label="🎵 Audio", value=True)
                            script_checkbox = gr.Checkbox(label="📝 Script", value=True)
                        
                        generate_btn = gr.Button("🚀 Generate Content", variant="primary", size="lg")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("""
### 💡 Quick Tips

**Style Options:**
- **Cinematic**: Hollywood movie style
- **Fantastical**: Magical, dreamlike
- **Noir**: Dark, mysterious
- **Epic**: Grand, heroic scale
- **Intimate**: Personal, quiet
- **Comedic**: Funny, lighthearted
- **Horror**: Scary, suspenseful
- **Documentary**: Realistic, factual

**Emotional Tones:**
- joy, sadness, fear
- wonder, mystery
- adventure, epic
- romance, comedy
- suspense, horror
                        """)
                
                gr.Markdown("---")
                
                # Output section
                with gr.Row():
                    with gr.Column():
                        status_output = gr.Markdown(label="Status")
                    
                with gr.Row():
                    with gr.Column():
                        outputs_output = gr.Markdown(label="Generated Outputs")
                    with gr.Column():
                        preview_output = gr.Markdown(label="Preview")
                
                with gr.Accordion("🔍 Technical Metadata", open=False):
                    metadata_output = gr.Code(label="Metadata JSON", language="json")
                
                # Connect generate button
                generate_btn.click(
                    fn=interface.generate_content,
                    inputs=[
                        prompt_input,
                        style_input,
                        duration_input,
                        emotional_tone_input,
                        video_checkbox,
                        audio_checkbox,
                        script_checkbox
                    ],
                    outputs=[status_output, outputs_output, preview_output, metadata_output]
                )
            
            # ============= HISTORY TAB =============
            with gr.Tab("📚 History"):
                gr.Markdown("## Your Creations")
                
                history_display = gr.Markdown()
                refresh_history_btn = gr.Button("🔄 Refresh History", variant="secondary")
                
                refresh_history_btn.click(
                    fn=interface.get_history,
                    inputs=[],
                    outputs=[history_display]
                )
                
                # Auto-load history
                demo.load(fn=interface.get_history, outputs=[history_display])
            
            # ============= STATISTICS TAB =============
            with gr.Tab("📊 Statistics"):
                gr.Markdown("## System Performance")
                
                stats_display = gr.Markdown()
                refresh_stats_btn = gr.Button("🔄 Refresh Statistics", variant="secondary")
                
                refresh_stats_btn.click(
                    fn=interface.get_statistics,
                    inputs=[],
                    outputs=[stats_display]
                )
                
                # Auto-load stats
                demo.load(fn=interface.get_statistics, outputs=[stats_display])
            
            # ============= EXAMPLES TAB =============
            with gr.Tab("💡 Examples"):
                gr.Markdown("""
## Story Examples

Try these prompts to get started!

### 🧙‍♂️ Fantasy
```
A young wizard discovers an ancient book that can rewrite reality, but every change comes with unexpected consequences.
```
**Style:** fantastical | **Tone:** wonder,mystery | **Duration:** 120s

### 🔍 Mystery
```
A detective receives an anonymous letter leading to a cold case from 20 years ago, but the sender seems to know too much.
```
**Style:** noir | **Tone:** suspense,mystery | **Duration:** 90s

### 🚀 Sci-Fi
```
An astronaut on Mars discovers signals coming from beneath the surface, suggesting life that shouldn't exist.
```
**Style:** cinematic | **Tone:** wonder,fear | **Duration:** 150s

### 💕 Romance
```
Two strangers keep meeting at the same coffee shop every morning, but neither knows the other is a time traveler.
```
**Style:** intimate | **Tone:** joy,mystery | **Duration:** 120s

### 😂 Comedy
```
A superhero with the lamest power (perfect parallel parking) must save the city from a villain who can only commit parking violations.
```
**Style:** comedic | **Tone:** joy,absurd | **Duration:** 90s

### 👻 Horror
```
A family moves into a smart home that seems helpful at first, but slowly starts making disturbing decisions on its own.
```
**Style:** horror | **Tone:** fear,suspense | **Duration:** 180s

### 🌍 Adventure
```
A mapmaker finds an uncharted island on an ancient globe that appears in different locations every night.
```
**Style:** epic | **Tone:** adventure,wonder | **Duration:** 150s

---

**Pro Tip:** Mix emotional tones for complex narratives!
Examples: `joy,sadness`, `wonder,fear`, `mystery,adventure`
                """)
            
            # ============= ABOUT TAB =============
            with gr.Tab("ℹ️ About"):
                gr.Markdown("""
# About AetherOS

## 🌟 What is AetherOS?

AetherOS is the first fully open-source, AI-powered creative studio that democratizes
multimedia content creation. It combines:

- **🧠 Neural Graph Memory** - Persistent context and learning
- **❤️ Affective Reasoning** - Emotion and cultural understanding
- **🤖 Agent Orchestration** - Self-optimizing AI coordination
- **🎬 Multimodal Generation** - Video, audio, script creation

## 🎯 Key Features

✅ **Zero Cost** - Fully free and open source  
✅ **No Coding** - Intuitive visual interface  
✅ **Ethical AI** - Cultural sensitivity built-in  
✅ **Memory System** - Learns from your creations  
✅ **Self-Improving** - Gets better with use  

## 🚀 How It Works

1. **Enter Your Prompt** - Describe your story in plain language
2. **Choose Style & Tone** - Select visual style and emotional mood
3. **Generate** - AI creates video, audio, and script specifications
4. **Review & Iterate** - View results and refine your creation

## 🧪 Technology Stack

- **Memory:** Graph-based episodic memory with associative recall
- **Emotion:** VAD model (Valence, Arousal, Dominance)
- **Agents:** Recursive meta-prompting with utility-based reflexes
- **Architecture:** Modular, production-ready Python

## 📚 Learn More

- [GitHub Repository](#) (coming soon)
- [Documentation](#) (coming soon)
- [Community Discord](#) (coming soon)

---

**Version:** 1.0.0-alpha  
**Status:** ✅ Operational  
**License:** Apache 2.0 + CC BY-SA 4.0

*"Democratizing imagination, one story at a time."*
                """)
        
        # Footer
        gr.Markdown("""
---
<div style="text-align: center; opacity: 0.7;">
    AetherOS v1.0.0-alpha | Open-Source Generative Supremacy | Made with ❤️
</div>
        """)
    
    return demo


def create_simple_interface():
    """Fallback: Simple terminal interface if Gradio not available"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                   🎨 AetherOS Creative Studio 🎨                            ║
║                                                                              ║
║                 Simple Terminal Interface (Gradio not available)             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    interface = AetherOSInterface()
    
    while True:
        print("\n" + "="*80)
        print("MAIN MENU")
        print("="*80)
        print("1. Create New Story")
        print("2. View History")
        print("3. View Statistics")
        print("4. Exit")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            print("\n--- CREATE NEW STORY ---")
            prompt = input("Story Prompt: ")
            style = input("Style (cinematic/fantastical/noir/epic) [cinematic]: ") or "cinematic"
            duration = int(input("Duration in seconds [120]: ") or "120")
            tone = input("Emotional Tone [wonder]: ") or "wonder"
            
            print("\nOutput Formats:")
            video = input("Generate Video? (y/n) [y]: ").lower() != 'n'
            audio = input("Generate Audio? (y/n) [y]: ").lower() != 'n'
            script = input("Generate Script? (y/n) [y]: ").lower() != 'n'
            
            print("\n⏳ Generating...")
            
            status, outputs, preview, metadata = interface.generate_content(
                prompt, style, duration, tone, video, audio, script
            )
            
            print("\n" + status)
            print("\n" + outputs)
            print("\n" + preview)
            
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\n" + interface.get_history())
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            print("\n" + interface.get_statistics())
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")


if __name__ == "__main__":
    print("\n🚀 Starting AetherOS Creative Studio...\n")
    
    if GRADIO_AVAILABLE:
        print("✅ Gradio detected - launching web interface!")
        print("🌐 Opening in your browser...\n")
        
        demo = create_gradio_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    else:
        print("⚠️  Gradio not installed - using terminal interface")
        print("💡 For the full web experience, install: pip install gradio\n")
        
        create_simple_interface()
