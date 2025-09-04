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
import sys
from argparse import ArgumentParser, BooleanOptionalAction

from pygenpassword import ArgumentEnableFeature, PasswordMachine

def print_machine_settings(password_machine):
    print('Using Character Classes:', *tuple(password_machine.use_character_classes))
    print('Password Length:', password_machine.password_length)
    print('No Repeating Characters?', password_machine.no_repeating_characters)
    print('Minimum characters per class:', password_machine.minimum_characters_per_class)
    if password_machine.debug:
        print('Debugging Enabled.')

def print_all_classes(password_machine):
    print('Available character classes')
    for class_name in password_machine.character_classes:
        spaces=' ' * (22 - len(class_name))
        print(class_name, spaces, password_machine.character_classes[class_name])
    exit()

def main():
    pm=PasswordMachine()

    parser = ArgumentParser(description='A simple random password generator with cli tool and library.')
    parser.add_argument(
        '-l',
        '--length',
        metavar='<length>',
        help=f'Password Length (Default: {pm.password_length})'
    )
    parser.add_argument(
        '-r',
        '--allow-repeat',
        action=ArgumentEnableFeature,
        help=f'Allow repeating characters? (Default: {not pm.no_repeating_characters})'
    )
    parser.add_argument(
        '-m',
        '--min-chars-per',
        metavar='<number>',
        type=int,
        help=f'Minimum number of characters per class (Default: {pm.minimum_characters_per_class})'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action=ArgumentEnableFeature,
        help='Display extra output?'
    )
    parser.add_argument(
        '-d',
        '--debug',
        action=ArgumentEnableFeature,
        help='Enable debugging?'
    )
    parser.add_argument(
        '--use-class',
        metavar='<class_name>',
        choices=['help'] + list(pm.character_classes.keys()),
        nargs='+',
        help=f'List of character classes to use. Not compatiable with "add-class" and "remove-class". Use "help" to list all the character classes available. (Default: {", ".join(pm.use_character_classes)})'
    )
    parser.add_argument(
        '--add-class',
        metavar='<class_name>',
        choices=['help'] + list(pm.character_classes.keys()),
        nargs='+',
        help='List of character classes to use. Not compatiable with "add-class" and "remove-class". Use "help" to list all the character classes available.'
    )
    parser.add_argument(
        '--remove-class',
        metavar='<class_name>',
        choices=['help'] + list(pm.character_classes.keys()),
        nargs='+',
        help='List of character classes to use. Not compatiable with "add-class" and "remove-class". Use "help" to list all the character classes available.'
    )

    args=parser.parse_args()

    if args.length:
        pm.password_length=int(args.length)

    if args.allow_repeat:
        pm.no_repeating_characters=False
    if args.min_chars_per:
        pm.minimum_characters_per_class=args.min_chars_per

    if args.use_class and 'help' in args.use_class:
        print_all_classes(pm)
    if args.add_class and 'help' in args.add_class:
        print_all_classes(pm)
    if args.remove_class and 'help' in args.remove_class:
        print_all_classes(pm)

    if args.use_class and (args.add_class or args.remove_class):
        print('Option use error! "use-class" is not compatiable with "add-class" and "remove-class"')
        exit(1)

    if args.use_class:
        pm.use_character_classes=args.use_class
    else:
        if args.add_class:
            # TODO check if the added classes already exists.
            pm.use_character_classes=pm.use_character_classes + args.add_class
        if args.remove_class:
            # TODO check if the removed classes are in the list.
            pm.use_character_classes=[ class_name for class_name in pm.use_character_classes if class_name not in args.remove_class ]

    if args.use_class:
        print('use_class', args.use_class)
    if args.debug:
        pm.debug=True
    if args.verbose or args.debug:
        print_machine_settings(pm)
    print(pm.generate())
