from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import base64
import json

from auth.client import VerifiedClient, get_verified_frontend_client
from core.config import config
from core.logging import get_logger
from security.hmac import hash_hmac

log = get_logger()

router = APIRouter()

tags = ["Login"]

@router.get(
    "/auth/google/login",
    description=(
        "Warning!!!: This method will not work when called through the documentation. "
        "Please call this path through a browser directly.\n"
        "\nRedirect the user to Google's 0Auth2 consent screen. "
        
    ),
    response_class=RedirectResponse,
    tags=tags
)
async def google_login(
    client: VerifiedClient = Depends(get_verified_frontend_client)
) -> RedirectResponse:

    state_data = json.dumps({"client_id": str(client.id)})
    state = base64.urlsafe_b64encode(state_data.encode()).decode()
    state_signature = hash_hmac(content=state, key=config.GOOGLE_HMAC_SECRET)
    signed_state = f"{state}.{state_signature}"

    log.debug(f"Created signed state for Client '{client.id}'...")

    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": signed_state
    }

    url = f"{config.GOOGLE_AUTH_URL}?{urlencode(params)}"

    log.debug(f"Redirecting User for Client '{client.id}' to Google's consent screen...")

    return RedirectResponse(url=url)

# TODO: Implement callback path