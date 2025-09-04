# Python Password Generator

A simple random password generator with cli tool and library.

## Installation

### Install directly from github to your local environment:
   ```bash
   pip install git+https://github.com/magister990/pygenpassword.git
   ```

## Development Setup

This project uses `poetry`. Please see [python-poetry.org](https://python-poetry.org/docs/#installation)
for installation instructions.

1. Clone the repository:
   ```bash
   git clone https://github.com/magister990/pygenpassword.git
   cd pygenpassword
   ```
   Preferably fork this repository and clone the fork.

2. Install dependencies and activate virtual environment:
   ```bash
   poetry install
   poetry shell
   ```
   Depending on the version of poetry it may require installing the `poetry-plugin-shell` plugin.

3. Run the CLI in development:
   ```bash
   poetry run genpassword --help
   ```
