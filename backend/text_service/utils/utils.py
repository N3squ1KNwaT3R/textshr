import secrets
import string
import hashlib
from passlib.hash import bcrypt


def generate_key(ttl: int) -> str:
    ttl_length_map = {600 : 4,
                      30 : 3,
                      3600 : 5,
                      28800 : 6,
                      86400: 7
                    }

    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(ttl_length_map.get(ttl)))




def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    sha = hashlib.sha256(password_bytes).digest()  # всегда 32 байта
    return bcrypt.hash(sha)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return bcrypt.verify(sha, hashed_password)

def text_size(text: str) -> int:
    return len(text.encode("utf-8"))