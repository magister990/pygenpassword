#!/usr/bin/env python
#
#   Copyright 2024 Alexander Scott
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from typing import Optional

import typer

from pygenpassword.password_machine import PasswordMachine

app = typer.Typer()


def main():
    app()


def print_machine_settings(pm: PasswordMachine):
    typer.echo(f'Using Character Classes: {" ".join(pm.use_character_classes)}')
    typer.echo(f'Password Length: {pm.password_length}')
    typer.echo(f'No Repeating Characters? {pm.no_repeating_characters}')
    typer.echo(f'Minimum characters per class: {pm.minimum_characters_per_class}')
    if pm.debug:
        typer.echo('Debugging Enabled.')


@app.command()
def generate(
    length: Optional[int] = typer.Option(
        None, '-l', '--length',
        metavar='LENGTH',
        help='Password length (default: 12)',
    ),
    allow_repeat: bool = typer.Option(
        False, '-r', '--allow-repeat',
        is_flag=True,
        help='Allow repeating characters',
    ),
    min_chars_per: Optional[int] = typer.Option(
        None, '-m', '--min-chars-per',
        metavar='NUMBER',
        help='Minimum characters per class (default: 1)',
    ),
    use_class: Optional[list[str]] = typer.Option(
        None, '--use-class',
        metavar='CLASS',
        help='Replace active classes entirely (repeat for multiple). Incompatible with --add-class / --remove-class.',
    ),
    add_class: Optional[list[str]] = typer.Option(
        None, '--add-class',
        metavar='CLASS',
        help='Add a class to the active set (repeat for multiple)',
    ),
    remove_class: Optional[list[str]] = typer.Option(
        None, '--remove-class',
        metavar='CLASS',
        help='Remove a class from the active set (repeat for multiple)',
    ),
    list_classes: bool = typer.Option(
        False, '--list-classes',
        is_flag=True,
        help='List all available character classes and exit',
    ),
    verbose: bool = typer.Option(
        False, '-v', '--verbose',
        is_flag=True,
        help='Display machine settings before generating',
    ),
    debug: bool = typer.Option(
        False, '-d', '--debug',
        is_flag=True,
        help='Enable debug output (implies verbose)',
    ),
):
    pm = PasswordMachine()

    if list_classes:
        typer.echo('Available character classes (* = default):')
        for class_name, chars in pm.character_classes.items():
            marker = '*' if class_name in pm.use_character_classes else ' '
            spaces = ' ' * (22 - len(class_name))
            typer.echo(f' {marker} {class_name}{spaces}{chars}')
        raise typer.Exit()

    valid_classes = set(pm.character_classes.keys())
    for cls in (use_class or []) + (add_class or []) + (remove_class or []):
        if cls not in valid_classes:
            typer.echo(
                f'Error: unknown class "{cls}". Run with --list-classes to see available classes.',
                err=True,
            )
            raise typer.Exit(1)

    if use_class and (add_class or remove_class):
        typer.echo(
            'Error: --use-class is not compatible with --add-class / --remove-class.',
            err=True,
        )
        raise typer.Exit(1)

    if length is not None:
        pm.password_length = length
    if allow_repeat:
        pm.no_repeating_characters = False
    if min_chars_per is not None:
        pm.minimum_characters_per_class = min_chars_per

    if use_class:
        pm.use_character_classes = use_class
    else:
        if add_class:
            pm.use_character_classes = pm.use_character_classes + add_class
        if remove_class:
            pm.use_character_classes = [c for c in pm.use_character_classes if c not in remove_class]

    if debug:
        pm.debug = True
    if verbose or debug:
        print_machine_settings(pm)

    result = pm.generate()
    if result is None:
        typer.echo('Failed to generate password after maximum attempts. Please retry.', err=True)
        raise typer.Exit(1)
    typer.echo(result)
