import secrets
import string

from passlib.hash import bcrypt


def generate_key(ttl: int) -> str:
    ttl_length_map = {600 : 4,
                      3600 : 5,
                      28800 : 6,
                      86400: 7
                    }

    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(ttl_length_map.get(ttl)))



def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)