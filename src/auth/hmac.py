from fastapi import Request, HTTPException, status, Depends
import hashlib
import hmac

from auth.verify import get_client_from_key
from core.config import config
from core.logging import get_logger

log = get_logger()

def get_client_hmac_secret(client: str) -> bytes:

    """Fetches the client HMAC secret."""

    secret = config.APPLICATIONS[client].hmac_secret
    log.debug(f"Retrieved HMAC secret for client '{client}'")

    return secret


ALLOWED_ALGORITHMS = {"sha256"}
HMAC_SIGNATURE_HEADER = "X-Signature"
HMAC_ALGORITHM = "sha256"

assert HMAC_ALGORITHM in ALLOWED_ALGORITHMS, \
    f"Unsupported HMAC algorithm: {HMAC_ALGORITHM}"

async def verify_hmac_signature(
    request: Request,
    client: str = Depends(get_client_from_key)
) -> None:

    """Verifies HMAC Signature of an incoming request.

    Args:
        request: The FastAPI Request object.
        client: The client identifier resolved from the API key.

    Returns:
        None
    
    Raises:
        HTTPException if signature is missing or invalid."""

    user_signature = request.headers.get(HMAC_SIGNATURE_HEADER)
    if not user_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing Header: '{HMAC_SIGNATURE_HEADER}'"
        )

    if "=" in user_signature:
        prefix, sig_value = user_signature.split("=", 1)
        if prefix in ALLOWED_ALGORITHMS:
            if prefix != HMAC_ALGORITHM:
                log.warning(
                    f"Client '{client}' sent algorithm prefix '{prefix}' "
                    f"but expected '{HMAC_ALGORITHM}'"
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Algorithm mismatch"
                )
        user_signature = sig_value

    hmac_secret: bytes = get_client_hmac_secret(client=client)

    hash_func = getattr(hashlib, HMAC_ALGORITHM)

    body: bytes = await request.body()

    canonical_parts = []
    canonical_parts.append(request.method.encode('utf-8'))
    canonical_parts.append(request.url.path.encode('utf-8'))
    canonical_parts.append(client.encode('utf-8'))
    canonical_parts.append(body)
    canonical_string = b"\n".join(canonical_parts)

    expected_signature = hmac.new(
        key=hmac_secret,
        msg=canonical_string,
        digestmod=hash_func
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, user_signature):

        log.warning(f"HMAC verification failed for client '{client}'")

        # TODO: Remove below debug log later
        log.debug(f"Expected signature '{expected_signature}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid HMAC Signature"
        )

    log.debug(f"HMAC Signature verified for client '{client}'")

    return None