import hashlib

def get_hash_sha356(input: str) -> str:

    """Hashes provided string."""

    if input == "":
        raise ValueError("Input must not be empty string")

    if not isinstance(input, str):
        raise ValueError("Input must be of type string")

    enc = input.encode(encoding='utf-8')
    hash = hashlib.sha256()
    hash.update(enc)
    return hash.hexdigest()