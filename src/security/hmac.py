import hashlib
import hmac

from core.logging import get_logger

log = get_logger()

HMAC_ALGORITHM = "sha256"

def hash_hmac(content: str, key: bytes) -> str:

    """Creates and returns an hmac encoded string."""

    canonical_string = content.encode('utf-8')

    hash_func = getattr(hashlib, HMAC_ALGORITHM)

    return hmac.new(
        key=key,
        msg=canonical_string,
        digestmod=hash_func
    ).hexdigest()


def is_valid_hmac(provided_hmac: str, expected_hmac: str) -> bool:

    """Compares two hmac signatures.
    Returns False if the hmac digests are not the same."""

    if not hmac.compare_digest(provided_hmac, expected_hmac):
        log.warning(f"Invalid hmac signature detected: Provided='{provided_hmac}' vs. Expected='{expected_hmac}'")
        return False
    return True