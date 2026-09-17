from cachetools import TTLCache, cached

from database.models import get_models_by_expertise
from database.session import get_db_session_ctx


class ModelConfig:

    @property
    @cached(cache=TTLCache(maxsize=10, ttl=600))
    def CHAT_COMPLETION_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="chat_completion"
            )


    @property
    @cached(cache=TTLCache(maxsize=10, ttl=600))
    def VECTOR_EMBEDDING_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="vector_embedding"
            )


    @property
    @cached(cache=TTLCache(maxsize=10, ttl=600))
    def TRANSLATION_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="translation"
            )


model_config = ModelConfig()