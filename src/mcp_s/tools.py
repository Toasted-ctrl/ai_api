import uuid
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from sqlalchemy.orm import Session

from core.logging import get_logger
from database.mcps import get_mcp_by_id


log = get_logger()


async def get_mcp_tools(
    session: Session,
    mcp_ids: list[uuid.UUID]
) -> list[BaseTool]:

    conn = {}

    for mcp_id in mcp_ids:
        conf = get_mcp_by_id(session=session, mcp_id=mcp_id)
        conn[conf.name] = {
            "url": f"{conf.url}/mcp",
            "transport": conf.transport
        }

    client = MultiServerMCPClient(connections=conn)
    log.debug("Created MultiServerMCPClient")
    return await client.get_tools()