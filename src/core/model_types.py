from cachetools import TTLCache

from database.models import get_models_by_expertise
from database.session import get_db_session_ctx


class ModelConfig:

    def __init__(self):
        self._cache: TTLCache[str, list[str]] = TTLCache(maxsize=10, ttl=600)


    async def _get_models(self, expertise: str) -> list[str]:
        if expertise not in self._cache:
            async with get_db_session_ctx() as session:
                self._cache[expertise] = await get_models_by_expertise(
                    session=session,
                    expertise=expertise
                )
        return self._cache[expertise]


    async def chat_completion_models(self) -> list[str]:
        return await self._get_models("chat_completion")


    async def vector_embedding_models(self) -> list[str]:
        return await self._get_models("vector_embedding")


    async def translation_models(self) -> list[str]:
        return await self._get_models("translation")


model_config = ModelConfig()
