import uuid
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from database.documents_users import store_user_document
from database.providers import get_all_provider_configurations, UserProviderRegistry, ProviderConfiguration
from database.schemas.user_skills import UserSkillsT
from database.vector_store import get_vector_store_settings, VectorStoreConfig
from vs.get_vs import get_vector_store
from vs.save_docs import save_docs, VectorStoreScope


log = get_logger()


async def post_user_skill(
    session: AsyncSession,
    user_id: uuid.UUID,
    name: str,
    description: str,
    skill_text: str,
    scope: str,
    parameters_schema: dict | None = None
) -> uuid.UUID:
    """Creates a user skill record, stores it in the UserSkillsT table, and saves the description to the Vector Store.
    
    Args:
        session: Async database session
        user_id: The user's UUID
        name: Name of the skill
        description: Description of the skill
        skill_text: The actual skill implementation/content
        parameters_schema: Optional JSON schema for skill parameters
        
    Returns:
        The ID of the created UserSkillsT record
    """
    
    # Step 1: Create document record with scope user_vs_skills
    document_id = await store_user_document(
        session=session,
        user_id=user_id,
        name=name,
        scope="user_vs_skills"
    )
    
    log.debug(f"Created user document with ID '{document_id}' for skill '{name}'")
    
    # Step 2: Create UserSkillsT entry
    user_skill = UserSkillsT(
        id=document_id,
        user_id=user_id,
        name=name,
        description=description,
        skill_text=skill_text,
        parameters_schema=parameters_schema or {}
    )
    
    session.add(user_skill)
    await session.flush()
    
    skill_id = user_skill.id
    log.debug(f"Created UserSkillsT record with ID '{skill_id}'")
    
    # Step 3: Store description in Vector Store
    try:
        vscf: VectorStoreConfig = await get_vector_store_settings(
            session=session,
            scope=scope
        )

        p_reg: UserProviderRegistry = await get_all_provider_configurations(
            session=session,
            user_id=user_id
        )

        prov: ProviderConfiguration = getattr(
            p_reg,
            vscf.e_provider
        )

        vs = await run_in_threadpool(
            get_vector_store,
            vs_collection_name=vscf.vs_collection_name,
            vs_vendor=vscf.vs_vendor,
            vs_port=vscf.vs_port,
            vs_base_url=vscf.vs_base_url,
            vs_encrypted_api_key=vscf.vs_encrypted_api_key,
            e_model=vscf.e_model,
            e_base_url=prov.base_url,
            e_encrypted_api_key=vscf.e_api_key,
            e_langchain_con=prov.langchain_con,
            e_dimensions=vscf.e_dimensions
        )

        metadata = {
            "document-name": name,
            "user-id": str(user_id),
            "user-document-id": str(document_id),
            "scope": scope
        }

        doc_ids = await run_in_threadpool(
            save_docs,
            vector_store=vs,
            scope=VectorStoreScope.USER_SKILLS,
            texts=[description],
            metadatas=[metadata],
            required_metadata=vscf.required_filters
        )

        log.debug(f"Stored skill description in Vector Store with document IDs: {doc_ids}")

    except Exception as e:
        log.error(f"Failed to store skill in Vector Store: {e}")
        raise

    return skill_id