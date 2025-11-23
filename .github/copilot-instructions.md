# AetherOS Copilot Instructions

## Project Overview

AetherOS is an open-source, multimodal creative AI system designed to democratize imagination without requiring coding knowledge. The project includes neural graph memory, affective reasoning, agent orchestration, and multimodal generation capabilities.

**Main Directory:** All code is located in the `gengen/` directory.

## Architecture

- **Core Modules** (`src/core/`):
  - Neural Graph Memory (NGM): `src/core/ngm/graph_memory.py`
  - Affective Processing Unit (APU): `src/core/apu/affective_layer.py`
- **Agent Orchestration** (`src/agents/`, `src/orchestrator/`)
- **Pipelines** (`src/pipelines/`):
  - Audio-driven animation
  - Storyboarded video generation
- **Entry Points**:
  - `aetheros_interface.py` - Web interface with Gradio
  - `aetheros_minimal.py` - Minimal demo without external dependencies
  - `launch_studio.py` - Guided launcher
  - `run_aetheros.py` - Quick start script

## Development Workflow

### Environment Setup

```bash
cd gengen/
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

```bash
# Web interface (recommended)
python3 aetheros_interface.py

# Minimal demo (no dependencies)
python3 aetheros_minimal.py

# Guided launcher
./studio.sh
# or
python3 launch_studio.py
```

### Testing

```bash
cd gengen/
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest --cov=src          # With coverage report for src/ directory
pytest tests/test_file.py # Run specific test file
```

### Linting and Formatting

```bash
cd gengen/
black .                   # Format code with Black
ruff check .              # Lint with Ruff
ruff check --fix .        # Auto-fix Ruff issues
```

## Code Style and Conventions

### Python Standards

- **Python Version:** 3.8+ compatible
- **Type Hints:** Always use type hints for function parameters and return values
- **Docstrings:** Use triple-quoted docstrings for modules, classes, and functions
- **Imports:** Group imports (standard library, third-party, local) with blank lines between groups

### Code Formatting

- **Formatter:** Black (line length: 88 characters, default)
- **Linter:** Ruff for fast linting and auto-fixes
- **Style Guide:** Follow PEP 8 conventions

### Patterns and Best Practices

- Use `dataclasses` for data containers (see `aetheros_minimal.py` for examples)
- Use `Enum` for categorical values (e.g., `EmotionCategory`)
- Prefer `async/await` for I/O-bound operations
- Use descriptive variable names; avoid single-letter variables except in loops
- Include type hints with `from typing import Dict, List, Optional, Any, Tuple`

### Example Code Style

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class StatusType(Enum):
    """Status enumeration for processing states."""
    PENDING = "pending"
    COMPLETE = "complete"


@dataclass
class ProcessResult:
    """Result container for processing operations."""
    status: StatusType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, str]] = None


async def process_data(input_data: Dict[str, Any]) -> ProcessResult:
    """
    Process input data and return results.
    
    Args:
        input_data: Dictionary containing processing parameters
        
    Returns:
        ProcessResult with status and processed data
    """
    # Implementation here
    pass
```

## Testing Guidelines

### Test Structure

- Place tests in `gengen/tests/` directory (create if it doesn't exist)
- Name test files with `test_` prefix (e.g., `test_graph_memory.py`)
- Use descriptive test function names: `test_<what>_<condition>_<expected>`

### Test Example

```python
import pytest
from aetheros_minimal import MinimalAffectiveLayer, EmotionCategory


def test_affective_analysis_detects_joy():
    """Test that affective layer correctly identifies joyful content."""
    # Arrange
    affective_layer = MinimalAffectiveLayer()
    text = "I am so happy and full of joy!"
    
    # Act
    result = affective_layer.analyze(text)
    
    # Assert
    assert result.primary_emotion == EmotionCategory.JOY
```

### Running Tests Before PR

Always run tests before submitting changes:
```bash
pytest -v
```

## Documentation

### README Updates

- Update `README.md` for major feature changes
- Update `LAUNCH_GUIDE.md` for new launch options or setup steps
- Keep `ROADMAP.md` in sync with planned features

### Code Documentation

- Every public function and class should have a docstring
- Use docstrings to explain "why" not just "what"
- Include parameter descriptions and return value explanations
- Example usages are helpful for complex functions

## Dependencies

### Adding New Dependencies

1. Add to `requirements.txt` with version constraints
2. Group with related dependencies (use comments as section headers)
3. Test installation in a clean virtual environment
4. Document any system-level dependencies (ffmpeg, etc.)

### Core Dependencies

- **ML Frameworks:** PyTorch, Transformers, Diffusers
- **Graph & Memory:** NetworkX, Neo4j, FAISS, Graphiti
- **Multimodal:** Whisper, Pillow, OpenCV, Librosa
- **Orchestration:** CrewAI, LangChain
- **Web Interface:** Gradio, FastAPI, Streamlit

## Common Tasks

### Adding a New Pipeline

1. Create file in `src/pipelines/`
2. Implement pipeline class with consistent interface
3. Register pipeline in orchestrator
4. Add documentation and examples
5. Write tests for the pipeline

### Modifying Core Systems

- **Graph Memory (NGM):** Changes to `src/core/ngm/`
- **Affective Layer (APU):** Changes to `src/core/apu/`
- **Agent System:** Changes to `src/agents/` or `src/orchestrator/`

### UI Changes

- Web interface code is in `aetheros_interface.py`
- Uses Gradio components and blocks
- Test locally before committing: `python3 aetheros_interface.py`

## Security and Ethics

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Follow ethical AI practices (see project's ethical guidelines)
- Validate and sanitize user inputs in web interfaces
- Be mindful of content generation safety

## License

- **Note:** License files are pending (see ROADMAP.md Phase 1 for LICENSE confirmation)
- Planned licenses: Apache 2.0 for code, CC BY-SA 4.0 for content/documentation
- Check project status before adding license headers to new files

## Getting Help

- Review `LAUNCH_GUIDE.md` for detailed setup instructions
- Check `README.md` for project overview
- Refer to `ROADMAP.md` for planned features and architecture
