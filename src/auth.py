import sqlite3
import bcrypt
import os
from datetime import datetime
from typing import Tuple

from src.password_validator import PasswordValidator
from src.brute_force import BruteForceProtection
from src.audit_log import AuditLog


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class AuthenticationSystem:
    def __init__(self):
        self.validator = PasswordValidator()
        self.brute_force = BruteForceProtection(max_attempts=5, lockout_time=300)
        self.audit = AuditLog()
        self.db = self.init_database()

    def init_database(self):
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect('data/users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP,
                password_changed_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        return conn

    def register(self, username: str, password: str) -> Tuple[bool, str]:
        is_valid, message = self.validator.validate(password)
        if not is_valid:
            return False, message
        password_hash = hash_password(password)
        try:
            cursor = self.db.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)',
                (username, password_hash, datetime.now())
            )
            self.db.commit()
            self.audit.log_event('REGISTRATION', username, 'SUCCESS', 'User registered')
            return True, f"User {username} registered successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        if self.brute_force.is_account_locked(username):
            self.audit.log_event('LOGIN', username, 'LOCKED', 'Account locked')
            return False, "Account is locked. Try again later."

        cursor = self.db.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if not result or not verify_password(password, result[0]):
            self.brute_force.record_failed_attempt(username)
            self.audit.log_event('LOGIN', username, 'FAILED', 'Invalid credentials')
            return False, "Invalid username or password"

        self.brute_force.reset_failed_attempts(username)
        self.audit.log_event('LOGIN', username, 'SUCCESS', 'User logged in')
        return True, f"Welcome {username}!"
