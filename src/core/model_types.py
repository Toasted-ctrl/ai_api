from database.models import get_models_by_expertise
from database.session import get_db_session_ctx


class ModelConfig:

    # TODO: Cache below functions for some time otherwise we'll keep calling.
    # TODO: Cache may be freed up after 10 minutes or so.

    @property
    def CHAT_COMPLETION_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="chat_completion"
            )


    @property
    def VECTOR_EMBEDDING_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="vector_embedding"
            )


    @property
    def TRANSLATION_MODELS(self):
        with get_db_session_ctx() as session:
            return get_models_by_expertise(
                session=session,
                expertise="translation"
            )


model_config = ModelConfig()