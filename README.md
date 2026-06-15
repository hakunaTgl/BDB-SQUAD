# BDB-SQUAD — Generative Creative Studio

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) ![AI](https://img.shields.io/badge/AI-Generative-purple) ![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![License](https://img.shields.io/badge/License-Pending-yellow)

> **That new generative.** BDB-SQUAD is a modular AI-powered creative studio built around the `gengen` (generative engine) core — enabling automated content creation, AI-driven pipelines, and creative hub interfaces.

---

## Features

- **AetherosOS Interface** — Custom AI operating layer for creative workflows
- **Creator Hub API** — REST API for triggering and managing generative pipelines
- **Modular Source Architecture** — Plug-and-play `src/` modules for extensibility
- **Multi-launch Support** — Shell scripts for quick startup of all services
- **Comprehensive Docs** — Quickstart, roadmap, launch guides, and system build docs included

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AI Engine | Aetheros (custom) |
| API | Creator Hub REST API |
| Automation | Shell scripts (bash) |
| Package Mgmt | pip / requirements.txt |

---

## Project Structure

```
BDB-SQUAD/
├── .github/          # CI workflows and GitHub automation
└── gengen/           # Core generative engine
    ├── src/          # Core modules and AI pipelines
    ├── aetheros_interface.py
    ├── aetheros_minimal.py
    ├── creator_hub_api.py
    ├── launch_studio.py
    ├── run_aetheros.py
    ├── start_all.sh
    ├── requirements.txt
    └── README.md
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hakunaTgl/BDB-SQUAD.git
cd BDB-SQUAD/gengen

# Install dependencies
pip install -r requirements.txt

# Launch the full studio
bash start_all.sh

# Or run Aetheros directly
python run_aetheros.py
```

---

## Documentation

| File | Description |
|---|---|
| `QUICKSTART.md` | Get up and running in minutes |
| `LAUNCH_GUIDE.md` | Detailed launch instructions |
| `COMPLETE_GUIDE.md` | Full system documentation |
| `ROADMAP.md` | Planned features and milestones |
| `STATUS.md` | Current build status |
| `SYSTEM_BUILD_COMPLETE.md` | Build completion notes |

---

## Roadmap

- [x] Core Aetheros engine
- [x] Creator Hub API
- [x] Launch automation scripts
- [ ] Web-based studio UI
- [ ] Cloud deployment support
- [ ] Multi-model AI integration
- [ ] Public API endpoints

---

## Contributing

Pull requests are welcome. Check open issues and the roadmap before contributing.

---

*Built by [@hakunaTgl](https://github.com/hakunaTgl) — that new generative.*
