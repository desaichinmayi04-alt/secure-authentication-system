import re
from typing import Tuple


class PasswordValidator:
    def __init__(self, min_length=12, require_uppercase=True,
                 require_numbers=True, require_special=True):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_numbers = require_numbers
        self.require_special = require_special
        self.common_passwords = self.load_common_passwords()

    def load_common_passwords(self) -> set:
        try:
            with open('data/common_passwords.txt', 'r') as f:
                return set(line.strip().lower() for line in f)
        except FileNotFoundError:
            return {'password', '123456', 'qwerty', 'admin'}

    def validate(self, password: str) -> Tuple[bool, str]:
        if len(password) < self.min_length:
            return False, f"Password must be at least {self.min_length} characters"
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letters"
        if self.require_numbers and not re.search(r'[0-9]', password):
            return False, "Password must contain numbers"
        if self.require_special and not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            return False, "Password must contain special characters"
        if password.lower() in self.common_passwords:
            return False, "Password is too common. Choose a stronger password"
        return True, "Password is strong"
