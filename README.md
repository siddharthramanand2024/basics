#  UV Weather API Consumer

A modern, fast, and lightweight Python application that consumes the public Open-Meteo API to fetch live weather data. 

This project was built to demonstrate modern Python project management using `uv`, including dependency locking, virtual environment management, and configuring custom command-line interfaces (CLIs) via `pyproject.toml`.

##  Features

* **Modern Tooling:** Managed entirely by `uv` (no need for `pip`, `venv`, or `pyenv`).
* **Strict Python Versioning:** Enforces Python >= 3.12.
* **Locked Dependencies:** Uses `uv.lock` to guarantee exactly `requests==2.31.0` is used across all environments.
* **Custom CLI Command:** Configured to run as a native terminal command (`consumeapi`) rather than a standard script.
* **Argument Parsing:** Accepts command-line arguments to fetch weather for different locations dynamically.

##  Prerequisites

You do not need Python installed globally on your system. You only need `uv`.
If you don't have `uv` installed, install it via:

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

##  Installation & Setup

1. **Clone the repository:**
```bash
   git clone [https://github.com/siddharthramanand2024/basics.git](https://github.com/siddharthramanand2024/basics.git)
   cd basics
   ```

2. **Sync the project:**
   This command will automatically download Python 3.12, create the virtual environment, install `requests`, and build the custom terminal commands.
```bash
   uv sync
   ```

##  Usage

Because this project is configured as a package in `pyproject.toml`, you do not need to run `python main.py`. Instead, use the custom entry point we defined.

**Run with the default location (Hyderabad):**
```bash
uv run consumeapi
```

**Run with a specific location argument:**
```bash
uv run consumeapi "Tokyo"
```

##  Project Structure

* `main.py` - The core application code and API consumption logic.
* `pyproject.toml` - The blueprint for the project. Defines metadata, dependencies, and CLI script entry points.
* `uv.lock` - The automatically generated file that freezes exact dependency versions.
* `.python-version` - Tells `uv` which specific Python version to use for this environment.
* `.gitignore` - Ensures local cache and build files (`__pycache__`, `.venv`, etc.) are not pushed to GitHub.
