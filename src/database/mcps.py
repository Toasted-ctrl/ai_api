import uuid
from dataclasses import dataclass
from sqlalchemy.orm import Session

from core.logging import get_logger
from .schemas.mcp import MCPsT


log = get_logger()


@dataclass(frozen=True)
class MCP:
    id: uuid.UUID
    name: str


def get_mcps(session: Session) -> list[MCP]:
    """Returns a list of available MCPs."""
    mcps = (
        session.query(MCPsT)
        .all()
    )
    log.debug(f"Found {len(mcps)} MCP configurations.")
    return [
        MCP(
            id=mcp.id,
            name=mcp.name
        )
        for mcp in mcps
    ]