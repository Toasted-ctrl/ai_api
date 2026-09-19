from dataclasses import asdict
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from auth.dep_verify_user import depends_verify_user, VerifiedUser
from core.cache import cache_key_builder
from database.mcps import get_mcps
from database.session import get_db_session
from iom.mcps import ResponseMCP


router = APIRouter()


@router.get(
    "/tools/mcp",
    tags=["MCP"],
    description="Retrieves a list of currently configured MCP servers.",
    response_model=ResponseMCP
)
@cache(
    expire=300,
    key_builder=cache_key_builder
)
def get_tools_mcp(
    session: Session = Depends(get_db_session),
    user: VerifiedUser = Depends(depends_verify_user)
) -> ResponseMCP:
    mcps = get_mcps(session=session)
    if not mcps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No MCP servers found"
        )
    return ResponseMCP(
        mcps=[asdict(mcp) for mcp in mcps]
    )