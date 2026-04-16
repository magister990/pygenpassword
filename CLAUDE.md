# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Package Management
This project uses Poetry for dependency management:
- `poetry install` - Install dependencies
- `poetry shell` - Activate virtual environment
- `poetry run <command>` - Run command in virtual environment
- `poetry add <package>` - Add dependency
- `poetry add --group dev <package>` - Add development dependency

## CLI Usage
The main entry point is the `genpassword` command (installed via `pyproject.toml`):
- `poetry run genpassword` - Generate password with default settings
- `poetry run genpassword --help` - Show all available options
- `python genpassword.py` - Run directly via the standalone script

Key options:
- `-l/--length <n>` - Password length (default: 12)
- `-r/--allow-repeat` - Allow repeating characters (default: not allowed)
- `-m/--min-chars-per <n>` - Minimum characters per class (default: 1)
- `--use-class <class>...` - Replace active classes entirely (incompatible with add/remove)
- `--add-class <class>...` - Add class(es) to the active set
- `--remove-class <class>...` - Remove class(es) from the active set
- `-v/--verbose` - Display machine settings before generating
- `-d/--debug` - Enable debug output (implies verbose)

Pass `help` as a class name to any class argument (e.g. `--use-class help`) to list all available character classes and exit.

Default active character classes: `digit_no_zero`, `alpha_lower_no_l_o`, `alpha_upper_no_o`, `symbol_7`

## Architecture
The project follows a simple modular structure:

- **PasswordMachine** (`pygenpassword/password_machine.py`) - Core password generation logic with configurable character classes, length constraints, and validation rules. Defaults: length=12, no repeating characters, minimum 1 char per class, retries up to 1000 times.
- **CLI** (`pygenpassword/cli.py`) - Command-line interface using Typer, handles all user input and configuration. `app` is the Typer instance; `main()` wraps `app()` as the entry point; `generate()` is the single `@app.command()`.
- **Package init** (`pygenpassword/__init__.py`) - Exports `PasswordMachine` and `main`
- **Entry Points** - Both `genpassword.py` standalone script (top-level) and installed `genpassword` command via `pyproject.toml` → `pygenpassword.cli:main`

The PasswordMachine class manages character classes (digits, letters, symbols) and enforces constraints like no repeating characters and minimum characters per class. The CLI layer translates command-line arguments into PasswordMachine configuration.