from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import base64
import json
import uuid

from auth.client import VerifiedClient, get_verified_frontend_client
from core.config import config
from core.logging import get_logger
from database.session import get_db_session
from security.google import (
    verify_google_token,
    VerifiedGoogleUser,
    exchange_google_code,
    ExchangedGoogleCode
)
from security.hmac import hash_hmac, is_valid_hmac
from security.jwt import create_jwt
from setup.application_user import (
    VerifiedApplicationUser,
    get_or_create_application_user
)

log = get_logger()

router = APIRouter()

tags = ["Login"]

@router.get(
    "/auth/google/login",
    description=(
        "WARNING!!! This method will not work when called through the documentation. "
        "Please call this path through a browser directly.\n"
        "\nRedirect the user to Google's OAuth2 consent screen."
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


@router.get(
    "/auth/google/callback",
    description=(
        "WARNING!!! This is a callback method for Google's Login, "
        "and will not work when called directly through the browser.\n"
        "\nNOTE: This method will store a cookie on the user's browser."
    ),
    tags=tags
)
async def google_callback(
    code: str,
    state: str,
    session: Session = Depends(get_db_session)
):

    log.debug("Receiving Callback from Google's OAuth service...")
    try:
        state_data, state_signature = state.rsplit(".", 1)
        log.debug("Received valid state format from Google...")
    except ValueError:
        log.warning(f"Received invalid state format: '{state}'...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid State format"
        )

    if not is_valid_hmac(
        provided_hmac=state_signature,
        expected_hmac=hash_hmac(
            content=state_data,
            key=config.GOOGLE_HMAC_SECRET
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid State"
        )

    decoded_state = json.loads(base64.urlsafe_b64decode(state_data))
    raw_client_id = decoded_state.get("client_id")
    if not raw_client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing client_id"
        )
    
    client_id = uuid.UUID(raw_client_id) # TODO: Implement function to check if the client_id exists in our db.
    g_jwt: ExchangedGoogleCode = await exchange_google_code(code=code)
    g_user: VerifiedGoogleUser = verify_google_token(token=g_jwt.id_token)
    s_user: VerifiedApplicationUser = get_or_create_application_user(
        first_name=g_user.first_name,
        last_name=g_user.last_name,
        email=g_user.email,
        client_id=client_id,
        login_provider="Google",
        external_id=g_user.sub,
        session=session
    )

    user_jwt = create_jwt(
        client_id=s_user.client_id,
        user_id=s_user.user_id
    )

    redirect_uri = "http://localhost:8501" # TODO: Remove hardcoded redirect.

    response = RedirectResponse(
        url=redirect_uri,
        status_code=status.HTTP_302_FOUND
    )

    log.debug(f"Created cookie for Client '{s_user.client_id}' for User '{s_user.user_id}'...")

    response.set_cookie(
        key="session_token",
        value=user_jwt,
        httponly=True,
        secure=False, # Set to True in production.
        samesite="lax",
        max_age=86_400,
        path="/"
    )

    log.debug(f"User '{s_user.user_id}' authenticated for Client '{s_user.client_id}' via Google, redirecting >> '{redirect_uri}'...")

    return response