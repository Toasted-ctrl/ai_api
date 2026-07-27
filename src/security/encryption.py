from cryptography.fernet import Fernet

from core.config import config

def encrypt(content: str) -> str:

    if not isinstance(content, str):
        raise TypeError("Content must be a string")

    if content == "":
        raise ValueError("Empty string")

    """Returns an encrypted string"""

    key = config.ENCRYPTION_KEY
    f = Fernet(key)
    return f.encrypt(content.encode(encoding='utf-8')).decode(encoding='utf-8')


def decrypt(content: str) -> str:

    if not isinstance(content, str):
        raise TypeError("Content must be a string")

    if content == "":
        raise ValueError("Empty string")

    """Returns a decrypted string"""

    key = config.ENCRYPTION_KEY
    f = Fernet(key)
    return f.decrypt(content).decode(encoding='utf-8')