import time
from typing import Dict


class BruteForceProtection:
    def __init__(self, max_attempts=5, lockout_time=300):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time
        self.failed_attempts: Dict[str, dict] = {}

    def is_account_locked(self, username: str) -> bool:
        if username not in self.failed_attempts:
            return False
        user_data = self.failed_attempts[username]
        if user_data['locked_until'] > time.time():
            return True
        user_data['attempts'] = 0
        user_data['locked_until'] = 0
        return False

    def record_failed_attempt(self, username: str):
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {'attempts': 0, 'locked_until': 0}
        self.failed_attempts[username]['attempts'] += 1
        if self.failed_attempts[username]['attempts'] >= self.max_attempts:
            self.failed_attempts[username]['locked_until'] = time.time() + self.lockout_time
            print(f"ALERT: Account {username} locked for {self.lockout_time}s")

    def reset_failed_attempts(self, username: str):
        if username in self.failed_attempts:
            self.failed_attempts[username]['attempts'] = 0
