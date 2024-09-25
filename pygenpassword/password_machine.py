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
import random

class PasswordMachine():
    def __init__(self):
        self.character_classes={
            'digit': "0123456789",
            'digit_no_zero': "123456789",
            'hex': "0123456789abcdef",
            'alpha_lower': "abcdefghijklmnopqrstuvwxyz",
            'alpha_upper': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            'alpha_lower_no_l_o': "abcdefghijkmnpqrstuvwxyz",
            'alpha_upper_no_o': "ABCDEFGHIJKLMNPQRSTUVWXYZ",
            'symbol_1': "~!@#$%^&*()_+=-[]{},:,<.>?",
            'symbol_2': "~!@#$%^&*()_+=-[]{}\\|,:'\",<.>/?",
            'symbol_3': ".,!?,:",
            'symbol_4': "#$%*",
            'symbol_5': "!@#$%^&*",
            'symbol_6': "!*$@",
            'symbol_7': '!.',
            'symbol_8': '.',
        }
        self.use_character_classes=[
            'digit_no_zero',
            'alpha_lower_no_l_o',
            'alpha_upper_no_o',
            'symbol_7',
        ]
        self.debug=False
        self.password_length=12
        self.no_repeating_characters=True
        self.minimum_characters_per_class=1

    def log(self, *args):
        if not self.debug:
            return
        print(*args)

    def get_bucket(self):
        return ''.join([ self.character_classes[key] for key in self.use_character_classes ])

    def validate_minimum_characters_per_class(self, password) -> bool:
        for character_class in self.use_character_classes:
            class_set=set(self.character_classes[character_class])
            if not any((c in class_set) for c in password):
                return False
        return True

    def validate_no_repeating_characters(self, password) -> bool:
        if not self.no_repeating_characters:
            return True
        chars=[ *password ]
        table={}
        for char in chars:
            if char in table:
                return False
            table[char]=1
        return True

    def generate(self):
        self.log(
            'PasswordMachine.generate(): character classes:',
            self.use_character_classes,
            'length:',
            self.password_length,
            'NRC:',
            self.no_repeating_characters,
            'MCPC:',
            self.minimum_characters_per_class
        )
        bucket=self.get_bucket()
        self.log('bucket', bucket)
        fail_after_attempts=1000
        while(fail_after_attempts):
            self.log('Generating password, attempts left:', fail_after_attempts)
            fail_after_attempts-=1
            new_password=''.join([ random.choice(bucket) for x in range(self.password_length)])
            self.log('New Password', new_password)
            if not self.validate_minimum_characters_per_class(new_password):
                self.log(' Discarding minimum character per class not reached!')
                continue
            if not self.validate_no_repeating_characters(new_password):
                self.log(' Discarding has repeating characters!')
                continue
            break
        if not fail_after_attempts:
            self.log('Maximum number of attempts reached, please retry')
            return None
        self.log('New Password:', new_password)
        return new_password
