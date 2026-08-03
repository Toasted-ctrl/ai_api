from dataclasses import dataclass
from joserfc import jwt
from joserfc.jwk import OctKey
from joserfc.jwt import JWTClaimsRegistry
import time
import uuid

from core.config import config
from core.logging import get_logger

log = get_logger()

def create_jwt(
    client_id: uuid.UUID,
    user_id: uuid.UUID,
    exp_seconds: int = 86_400
) -> str:

    """Creates a JWT string that may be added to a cookie stored client-side."""

    log.debug(f"Creating new JWT for user: '{user_id}'...")

    key = OctKey.import_key(config.JWT_SECRET)
    header = {"alg": "HS256"}
    claims = {
        "iss": "AIA",                           # Issuer
        "sub": str(user_id),                    # User ID
        "iat": int(time.time()),                # Issue time in unix format
        "exp": int(time.time()) + exp_seconds,  # Expiration time in unix format
        "aud": str(client_id)                   # Client ID
    }

    token = jwt.encode(
        header=header,
        claims=claims,
        key=key
    )

    log.debug(f"Created new JWT for user: '{user_id}'...")

    return token


@dataclass(frozen=True)
class DecodedJWT:
    iss: str
    sub: uuid.UUID
    iat: int
    exp: int
    aud: uuid.UUID


def decode_jwt(
    token: str
) -> DecodedJWT:

    """Decodes and returns a DecodedJWT object."""

    key = OctKey.import_key(config.JWT_SECRET)
    token = jwt.decode(value=token, key=key)
    
    claims_registry = JWTClaimsRegistry(
        iss={"essential": True, "value": "AIA"},
        aud={"essential": True},
        iat={"essential": True},
        exp={"essential": True},
        sub={"essential": True}
    )

    log.debug("Validating JWT claims...")

    claims_registry.validate(token.claims)

    return DecodedJWT(
        iss=token.claims["iss"],
        sub=uuid.UUID(token.claims["sub"]),
        iat=token.claims["iat"],
        exp=token.claims["exp"],
        aud=uuid.UUID(token.claims["aud"])
    )