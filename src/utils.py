import hashlib
import random


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


def is_password_strong(password):
    if len(password) < 5:
        return False, "Пароль должен содержать не менее 5 символов."
    if not any(char.isdigit() for char in password):
        return False, "Пароль должен содержать хотя бы одну цифру."
    if not any(char.isalpha() for char in password):
        return False, "Пароль должен содержать хотя бы одну букву."
    if not any(not char.isalnum() for char in password):
        return False, "Пароль должен содержать хотя бы один специальный символ."
    return True, None


def generate_unique_module_id():
    while True:
        new_id = random.randint(100000000000000, 999999999999999)
        return new_id