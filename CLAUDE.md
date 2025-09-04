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
- `python genpassword.py` - Generate password with default settings
- `python genpassword.py --help` - Show all available options
- Key options: `-l/--length`, `--use-class`, `--add-class`, `--remove-class`, `-v/--verbose`, `-d/--debug`

## Architecture
The project follows a simple modular structure:

- **PasswordMachine** (`password_machine.py`) - Core password generation logic with configurable character classes, length constraints, and validation rules
- **CLI** (`cli.py`) - Command-line interface using argparse, handles all user input and configuration
- **ArgumentEnableFeature** (`argument_enable_feature.py`) - Custom argparse Action for boolean flags
- **Entry Points** - Both `genpassword.py` standalone script and installed `genpassword` command via pyproject.toml

The PasswordMachine class manages character classes (digits, letters, symbols) and enforces constraints like no repeating characters and minimum characters per class. The CLI layer translates command-line arguments into PasswordMachine configuration.