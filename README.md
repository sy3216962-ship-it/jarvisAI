# Jarvis

Jarvis is a professional, modular desktop AI assistant project for Windows 11. The long-term goal is to build a personal AI operating-system assistant that can speak, listen, remember, automate tasks, and grow through plugins and future AI capabilities.

This repository currently contains the foundation for the project. The first milestone focuses on a clean project layout, configuration loading, logging, and a safe application entry point.

## Project Goals

Jarvis is designed to eventually support:

- Natural voice conversations
- Continuous listening and wake-word detection
- Short-term and long-term memory
- User preferences, goals, notes, and tasks
- Desktop command execution and application control
- File search and automation
- Vision, OCR, camera, and screen understanding
- Local and cloud AI model routing
- Plugins and future marketplace-style extensions
- GUI, animations, and desktop widgets
- Multi-agent planning and task execution

## Architecture Principles

The project follows these engineering principles:

- Modular code instead of a single large file
- Clear responsibilities for every file and folder
- Type hints, docstrings, comments, and logging
- Environment-based configuration for secrets and user settings
- Maintainable structure that can grow over time
- Safe defaults that do not require API keys to start

## Folder Structure

```text
Jarvis/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── config.py
├── settings.py
├── core/
├── skills/
├── vision/
├── speech/
├── llm/
├── memory/
├── gui/
├── assets/
├── logs/
├── plugins/
└── tests/
```

## Folder Purpose

| Folder | Purpose |
| --- | --- |
| `core/` | Main assistant orchestration, decision-making, personality, conversation, and scheduling modules. |
| `skills/` | User-facing capabilities such as system control, browser actions, calculator, notes, reminders, and integrations. |
| `vision/` | Camera access, image analysis, OCR, and future screen-understanding features. |
| `speech/` | Speech-to-text, text-to-speech, wake-word detection, and noise filtering. |
| `llm/` | Local and cloud model clients plus routing logic between providers. |
| `memory/` | Short-term memory, long-term memory, vector memory, and database persistence. |
| `gui/` | Desktop window, chat UI, widgets, and animations. |
| `assets/` | Static assets such as icons, sounds, images, and UI resources. |
| `logs/` | Runtime log files generated while Jarvis is running. |
| `plugins/` | Optional installable extensions that can add new assistant abilities. |
| `tests/` | Automated tests for project modules. |

## Requirements

- Windows 11
- Python latest stable release
- Visual Studio Code
- A terminal such as PowerShell or Windows Terminal

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local `.env` file if you want to override defaults:

```env
JARVIS_APP_NAME=Jarvis
JARVIS_ENVIRONMENT=development
JARVIS_LOG_LEVEL=INFO
JARVIS_DEBUG=true
```

Run the application foundation:

```powershell
python main.py
```

## Current Milestone

This first step creates the project foundation only. It does not implement the full assistant yet. Future steps will add modules one at a time, starting with the core assistant orchestration layer.
