from argon2 import PasswordHasher
from dotenv import load_dotenv
import os

load_dotenv()

MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")
ph = PasswordHasher()
MASTER_PASSWORD_HASH = ph.hash(MASTER_PASSWORD)


def hash_password(password):
    return ph.hash(password)


def check_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except:
        return False
