import asyncio
import uuid
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import config
from core.logging import get_logger
from database.mcps import get_mcp_by_id


log = get_logger()


async def get_mcp_tools(
    session: AsyncSession,
    mcp_ids: list[uuid.UUID],
    web_search: bool = False
) -> list[BaseTool]:
    """Creates MCP tools for an AI agent to use. Also enables the Web Search functionality if enabled."""

    conn = {}

    # TODO: Replace with one function that can find all MCP ids in one turn.

    if mcp_ids:
        confs = await asyncio.gather(
            *[get_mcp_by_id(session=session, mcp_id=mcp_id) for mcp_id in mcp_ids]
        )
        for conf in confs:
            conn[conf.name] = {
                "url": f"{conf.url}/mcp",
                "transport": conf.transport
            }

    if web_search:
        conn['Web Search'] = {
            "url": config.WEB_SEARCH_URL,
            "transport": config.WEB_SEARCH_TRANSPORT
        }

    client = MultiServerMCPClient(connections=conn)
    log.debug(f"Created MultiServerMCPClient with {len(conn)} connections")
    return await client.get_tools()
