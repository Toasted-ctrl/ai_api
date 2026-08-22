from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dep_verify_user import VerifiedUser, depends_verify_user
from core.config import config
from core.logging import get_logger
from database.providers import get_all_provider_configurations, ProviderConfiguration
from database.session import get_db_session
from iom.vector_embedding import PayloadSingleVectorEmbedding, ResponseSingleVectorEmbedding
from providers.vector_embedding import get_embedding

router = APIRouter()

tags = ["Vector Embedding"]

log = get_logger()


@router.post(
    path="/vector_embedding/test",
    tags=tags,
    description=(
        "Test endpoint to verify what vector embeddings will look like for the indicated Provider and model."
    ),
    response_model=ResponseSingleVectorEmbedding
)
async def post_test_vector_embedding(
    payload: PayloadSingleVectorEmbedding,
    user: VerifiedUser = Depends(depends_verify_user),
    session: Session = Depends(get_db_session)
) -> ResponseSingleVectorEmbedding:

    try:

        if payload.model not in config.VECTOR_EMBEDDING_MODELS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{payload.model}' is not a valid embedding model"
            )

        p_reg = get_all_provider_configurations(
            session=session,
            user_id=user.id
        )

        if payload.provider not in p_reg.names or payload.provider in p_reg.not_configured:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provider '{payload.provider}' is not supported or not configured"
            )

        prov: ProviderConfiguration = getattr(p_reg, payload.provider)

        embedding = await get_embedding(
            langchain_con=prov.langchain_con,
            model=payload.model,
            base_url=prov.base_url,
            prompt=payload.prompt,
            dimensions=payload.dimensions,
            encrypted_api_key=prov.encrypted_api_key
        )

        return {
            "prompt": payload.prompt,
            "provider": payload.provider,
            "model": payload.model,
            "dimensions": len(embedding),
            "embedding": embedding
        }

    except ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to connect to Provider '{payload.provider}'"
        )