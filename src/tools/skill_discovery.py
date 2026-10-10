import uuid
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from database.providers import UserProviderRegistry
from database.vector_store import get_vector_store_settings, VectorStoreConfig
from vs.get_vs import get_vector_store
from vs.search import search_docs_similarity


log = get_logger()


class VSSkillSearchInput(BaseModel):
    query: str = Field(..., description="The search query to look up in the skills database.")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of relevant skills to return.")


async def get_user_skill_discovery_tool(
    session: AsyncSession,
    user_id: uuid.UUID,
    scope: str,
    pr: UserProviderRegistry
) -> StructuredTool:
    """Skill discovery search tool. Will return the most relevent skills set by the User."""
    log.debug(f"Creating User Skill Discovery tool for user '{user_id}'.")
    vscf: VectorStoreConfig = await get_vector_store_settings(
        scope=scope,
        session=session
    )

    def discover_skills(query: str, limit: int = 5) -> str:
        em = getattr(pr, vscf.e_provider)
        vs = get_vector_store(
            vs_collection_name=vscf.vs_collection_name,
            vs_vendor=vscf.vs_vendor,
            vs_port=vscf.vs_port,
            vs_base_url=vscf.vs_base_url,
            vs_encrypted_api_key=vscf.vs_encrypted_api_key,
            e_model=vscf.e_model,
            e_base_url=em.base_url,
            e_langchain_con=em.langchain_con,
            e_encrypted_api_key=em.encrypted_api_key,
            e_dimensions=vscf.e_dimensions
        )
        filter = {
            "user-id": str(user_id)
        }
        vsr = search_docs_similarity(
            vector_store=vs,
            query=query,
            filter=filter
        )
        log.debug(f"Found {len(vsr)} in Vector Store (User Skills).")
        if not vsr:
            return "No relevant results found"

        # TODO: Add reranker, increase vs limit to 20, reranker limit 5.
        
        return "\n\n".join(
            f"[{i}] Score: {score}\n"
            f"Content:\n{doc.page_content}\n"
            f"Metadata: {doc.metadata}"
            for i, (doc, score) in enumerate(vsr, start=1)
        )

    return StructuredTool.from_function(
        func=discover_skills,
        name="discover_skills",
        description=(
            "Search the user's skill database for relevant skills. "
            "Use this tool when answering questions/inquiries which may have a related skill stored."
        ),
        args_schema=VSSkillSearchInput
    )