from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dep_verify_user import VerifiedUser, depends_verify_user
from core.logging import get_logger
from database.documents_users import store_user_document
from database.providers import get_all_provider_configurations, ProviderConfiguration, UserProviderRegistry
from database.session import get_db_session
from database.vector_store import get_vector_store_settings, VectorStoreConfig
from iom.vector_store import PayloadSaveDocuments, ResponseSavedDocuments, PayloadSearchDocuments
from vs.get_vs import get_vector_store
from vs.save_docs import save_docs
from vs.search import search_docs_similarity


router = APIRouter()


tags = ["Vector Store"]


log = get_logger()


@router.post(
    path="/vector_store/{scope}/add",
    tags=tags,
    description="Store (a) document(s) in the specified Vector Store based on scope.",
    response_model=ResponseSavedDocuments
)
def store_document(
    payload: PayloadSaveDocuments,
    scope: str,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session),
) -> ResponseSavedDocuments:

    if not scope in ["user_vs_docs", "user_vs_memories"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown scope: {scope}"
        )

    udids = []
    for metadata in payload.metadatas:
        udids.append(store_user_document(
            session=session,
            user_id=user.id,
            name=metadata.document_name,
            scope=scope
        ))

    vscf: VectorStoreConfig = get_vector_store_settings(
        session=session,
        scope=scope
    )

    p_reg: UserProviderRegistry = get_all_provider_configurations(
        session=session,
        user_id=user.id
    )

    prov: ProviderConfiguration = getattr(
        p_reg,
        vscf.e_provider
    )

    vs = get_vector_store(
        vs_collection_name=vscf.vs_collection_name,
        vs_vendor=vscf.vs_vendor,
        vs_port=vscf.vs_port,
        vs_base_url=vscf.vs_base_url,
        vs_encrypted_api_key=vscf.vs_encrypted_api_key,
        e_model=vscf.e_model,
        e_base_url=prov.base_url,
        e_encrypted_api_key=prov.encrypted_api_key,
        e_langchain_con=prov.langchain_con,
        e_dimensions=vscf.e_dimensions
    )

    metadatas = []
    for metadata, udid in zip(payload.metadatas, udids):
        meta_dict = metadata.model_dump()
        if 'scope' in vscf.required_filters:
            meta_dict['scope'] = scope
        if 'user-id' in vscf.required_filters:
            meta_dict['user-id'] = user.id
        if 'user-document-id' in vscf.required_filters:
            meta_dict['user-document-id'] = udid

        # NOTE: Changing keys to use dashes, required for Qdrant.
        meta_dict = {key.replace('_', '-'): value for key, value in meta_dict.items()}
        metadatas.append(meta_dict)

    doc_ids = save_docs(
        vector_store=vs,
        scope=scope,
        texts=payload.texts,
        metadatas=metadatas,
        required_metadata=vscf.required_filters
    )

    return ResponseSavedDocuments(
        added_documents=[did for did in doc_ids]
    )


@router.post(
    path="/vector_store/{scope}/search",
    tags=tags,
    description="Search (a) document(s) in the specified Vector Store scope."
)
def search_document(
    scope: str,
    payload: PayloadSearchDocuments,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session),
):

    vscf: VectorStoreConfig = get_vector_store_settings(
        scope=scope,
        session=session
    )

    p_reg: UserProviderRegistry = get_all_provider_configurations(
        session=session,
        user_id=user.id
    )
    
    prov: ProviderConfiguration = getattr(
        p_reg,
        vscf.e_provider
    )
    
    vs = get_vector_store(
        vs_collection_name=vscf.vs_collection_name,
        vs_vendor=vscf.vs_vendor,
        vs_port=vscf.vs_port,
        vs_base_url=vscf.vs_base_url,
        vs_encrypted_api_key=vscf.vs_encrypted_api_key,
        e_model=vscf.e_model,
        e_base_url=prov.base_url,
        e_encrypted_api_key=prov.encrypted_api_key,
        e_langchain_con=prov.langchain_con,
        e_dimensions=vscf.e_dimensions
    )

    results = search_docs_similarity(
        vector_store=vs,
        query=payload.query,
        filter={"user-id": user.id}
    )

    return {
        "query_results": results
    }