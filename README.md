# Pecko

**Pecko** is going to be a context-aware, CLI-based, autonomous, general-purpose AI agent designed to help you manage and interact with your local development environment intelligently.

<p align="center">
  <img src=".github/images/pecko_logo_.png" alt="Pecko Logo" width="100%">
</p>

## Features

- **Context-Aware**: Will understand your project structure and local files.
- **Autonomous**: Will perform tasks and make decisions based on your codebase.
- **CLI-First**: Built for the terminal, integrating seamlessly into your workflow.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites

- Python 3.13+
- `uv` installed (see [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/pecko.git
   cd pecko
   ```

2. **Install as a tool:**
   This allows you to run `pecko` directly from your terminal.
   ```bash
   uv tool install .
   ```

3. **(Optional) Development Setup:**
   If you want to develop Pecko itself:
   ```bash
   uv sync
   ```

## Usage

Initialize a new workspace:
```bash
pecko init
```

Check status:
```bash
pecko status
```

## Configuration

Pecko supports both **global** (user-level) and **local** (project-level) configurations. Local settings override global ones.

### Managing Profiles

Pecko uses **LLM Profiles** to manage different providers and models (e.g., OpenAI, Anthropic, Ollama).

**Interactive Configuration:**
```bash
# Configure global defaults (saved to ~/.pecko/config.json)
pecko config --global

# Configure local project settings (saved to .pecko/config.json)
pecko config --local
```

**List Profiles:**
```bash
pecko config --list
# or for global only
pecko config --global --list
```

**Switch Active Profile:**
```bash
pecko config --set-active <profile_name>
# Example:
pecko config --local --set-active ollama-local
```
