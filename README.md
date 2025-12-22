# Pecko

**Pecko** is going to be a context-aware, CLI-based, autonomous, general-purpose AI agent designed to help you manage and interact with your local development environment intelligently.

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
