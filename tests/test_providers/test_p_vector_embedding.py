from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from providers.vector_embedding import (
    LangChainCon,
    _build_embedding_model,
    get_embedding,
)
from security.encryption import encrypt


class TestBuildEmbeddingModel:
    """Tests for the _build_embedding_model factory."""

    @patch("providers.vector_embedding.OllamaEmbeddings")
    def test_ollama_returns_ollama_embeddings(self, mock_ollama_cls):
        """Should instantiate OllamaEmbeddings with model and base_url."""
        sentinel = MagicMock()
        mock_ollama_cls.return_value = sentinel

        result = _build_embedding_model(
            langchain_con=LangChainCon.OLLAMA,
            model="nomic-embed-text",
            base_url="http://localhost:11434",
        )

        mock_ollama_cls.assert_called_once_with(
            model="nomic-embed-text",
            base_url="http://localhost:11434",
            dimensions=None
        )

        assert result is sentinel


    @patch("providers.vector_embedding.OllamaEmbeddings")
    def test_ollama_ignores_api_key(self, mock_ollama_cls):
        """encrypted_api_key is accepted but not forwarded to Ollama."""
        _build_embedding_model(
            langchain_con=LangChainCon.OLLAMA,
            model="nomic-embed-text",
            base_url="http://localhost:11434",
            encrypted_api_key="secret",
        )

        # api key should NOT appear in the call kwargs
        call_kwargs = mock_ollama_cls.call_args.kwargs
        assert "encrypted_api_key" not in call_kwargs
        assert "api_key" not in call_kwargs


    @patch("providers.vector_embedding.OpenAIEmbeddings")
    def test_openai_returns_openai_embeddings(self, mock_openai_cls):
        """Should instantiate OpenAIEmbeddings with model, base_url, dimensions and api key."""
        sentinel = MagicMock()
        mock_openai_cls.return_value = sentinel

        result = _build_embedding_model(
            langchain_con=LangChainCon.OPENAI,
            model="openai-embed-random",
            base_url="http://openai.randomlink",
            dimensions=None,
            encrypted_api_key=encrypt("api-key")
        )

        mock_openai_cls.assert_called_once_with(
            model="openai-embed-random",
            base_url="http://openai.randomlink",
            dimensions=None,
            api_key="api-key",
            check_embedding_ctx_length=True
        )

        assert result == sentinel


    def test_unsupported_provider_raises_not_implemented(self):
        """Providers without embedding support should raise NotImplementedError."""
        with pytest.raises(NotImplementedError, match="not supported"):
            _build_embedding_model(
                langchain_con=LangChainCon.ANTHROPIC,
                model="some-model",
                base_url="http://localhost",
                dimensions=None
            )


class TestGetEmbedding:
    """Tests for the async get_embedding function."""

    VALID_MODEL = "mxbai-embed-large:latest"
    BASE_URL = "http://localhost:11434"
    FAKE_VECTOR = [0.1, 0.2, 0.3, 0.4]


    @pytest.fixture(autouse=True)
    def _allow_model(self):
        """Patch config so our test model is always recognised."""
        with patch(
            "providers.vector_embedding.config"
        ) as mock_config:
            mock_config.VECTOR_EMBEDDING_MODELS = [self.VALID_MODEL]
            yield mock_config


    @pytest.fixture
    def mock_embeddings(self):
        """Patch the factory to return a mock with async aembed_query."""
        mock_model = AsyncMock()
        mock_model.aembed_query.return_value = self.FAKE_VECTOR
        with patch(
            "providers.vector_embedding._build_embedding_model",
            return_value=mock_model,
        ) as mock_factory:
            yield mock_factory, mock_model


    @pytest.mark.asyncio
    async def test_returns_embedding_vector(self, mock_embeddings):
        """Happy path — should return the vector from aembed_query."""
        _, mock_model = mock_embeddings

        result = await get_embedding(
            langchain_con=LangChainCon.OLLAMA,
            model=self.VALID_MODEL,
            prompt="hello world",
            base_url=self.BASE_URL,
        )

        assert result == self.FAKE_VECTOR
        mock_model.aembed_query.assert_awaited_once_with("hello world")


    @pytest.mark.asyncio
    async def test_passes_args_to_factory(self, mock_embeddings):
        """Should forward all args to _build_embedding_model."""
        mock_factory, _ = mock_embeddings

        await get_embedding(
            langchain_con=LangChainCon.OLLAMA,
            model=self.VALID_MODEL,
            prompt="test",
            base_url=self.BASE_URL,
            encrypted_api_key="key123",
        )

        mock_factory.assert_called_once_with(
            langchain_con=LangChainCon.OLLAMA,
            model=self.VALID_MODEL,
            base_url=self.BASE_URL,
            dimensions=None,
            encrypted_api_key="key123",
        )


    @pytest.mark.asyncio
    async def test_invalid_model_raises_value_error(self):
        """A model not in VECTOR_EMBEDDING_MODELS should raise ValueError."""
        with pytest.raises(ValueError, match="not recognized"):
            await get_embedding(
                langchain_con=LangChainCon.OLLAMA,
                model="totally-fake-model",
                prompt="hello",
                base_url=self.BASE_URL,
            )


    @pytest.mark.asyncio
    async def test_invalid_model_skips_factory(self):
        """ValueError should fire before the factory is ever called."""
        with patch(
            "providers.vector_embedding._build_embedding_model"
        ) as mock_factory:
            with pytest.raises(ValueError):
                await get_embedding(
                    langchain_con=LangChainCon.OLLAMA,
                    model="bad-model",
                    prompt="hello",
                    base_url=self.BASE_URL,
                )

            mock_factory.assert_not_called()


    @pytest.mark.asyncio
    async def test_unsupported_provider_propagates(self):
        """NotImplementedError from factory should bubble up."""
        with pytest.raises(NotImplementedError):
            await get_embedding(
                langchain_con=LangChainCon.ANTHROPIC,
                model=self.VALID_MODEL,
                prompt="hello",
                base_url="http://localhost",
            )