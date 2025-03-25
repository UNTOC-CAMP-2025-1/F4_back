import random

email_auth_codes = {}

def generate_auth_code():
    return str(random.randint(100000, 999999))

def store_auth_code(user_email: str, code: str):
    email_auth_codes[user_email] = code

def verify_auth_code(user_email: str, code: str):
    return email_auth_codes.get(user_email) == code