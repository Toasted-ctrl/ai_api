from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dep_verify_user import VerifiedUser, depends_verify_user
from core.logging import get_logger
from database.providers import get_all_provider_configurations, ProviderConfiguration, UserProviderRegistry
from database.session import get_db_session
from database.vector_store import get_vector_store_settings, VectorStoreConfig
from iom.vector_store import PayloadSaveDocuments, ResponseSavedDocuments
from vs.get_vs import get_vector_store
from vs.save_docs import save_docs

router = APIRouter()

tags = ["Vector Store"]

log = get_logger()


@router.post(
    path="/vector_store/store",
    tags=tags,
    description="Store (a) document(s) in the specified Vector Store collection."
)
def store_document(
    payload: PayloadSaveDocuments,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session),
) -> ResponseSavedDocuments:

    vscf: VectorStoreConfig = get_vector_store_settings(
        session=session,
        collection_name=payload.collection_name
    )

    # TODO: Probably we should not name the collection, just what type of data:
    # - User Memory
    # - User Personal
    # - Agent Documentation
    # - etc.

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
    _metadatas = payload.metadata
    if 'user_id' in vscf.required_filters:
        for metadata in _metadatas:
            meta_dict = metadata.model_dump()
            meta_dict['user_id'] = user.id
            metadatas.append(meta_dict)

    else:
        metadatas = [metadata.model_dump() for metadata in metadatas]

    doc_ids = save_docs(
        vector_store=vs,
        doctype='personal',
        texts=payload.texts,
        metadatas=metadatas,
        required_metadata=vscf.required_filters
    )

    return ResponseSavedDocuments(
        added_docs=[did for did in doc_ids]
    )