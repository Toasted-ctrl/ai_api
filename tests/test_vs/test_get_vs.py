from unittest.mock import patch, MagicMock
import pytest

from providers.dataclasses import LangChainCon
from vs.get_vs import get_vector_store, VectorStore

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def embedding_params():
    """Common embedding-related parameters."""
    return {
        "e_model": "text-embedding-3-small",
        "e_base_url": "https://api.openai.com/v1",
        "e_langchain_con": LangChainCon.OLLAMA,
        "e_encrypted_api_key": "encrypted-emb-key-xyz",
        "e_dimensions": 1536,
    }


@pytest.fixture
def qdrant_params():
    """Common Qdrant-related parameters."""
    return {
        "vs_collection_name": "my_collection",
        "vs_vendor": VectorStore.QDRANT,
        "vs_port": 6333,
        "vs_base_url": "http://localhost:6333",
        "vs_encrypted_api_key": "encrypted-qdrant-key-abc",
    }


@pytest.fixture
def mock_embedding():
    """A mock embedding model returned by _build_embedding_model."""
    return MagicMock(name="embedding_model")


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

class TestGetVectorStoreQdrant:

    @patch("vs.get_vs.decrypt", return_value="decrypted-qdrant-key")
    @patch("vs.get_vs.QdrantVectorStore")
    @patch("vs.get_vs._build_embedding_model")
    def test_returns_qdrant_store_with_api_key(
        self,
        mock_build_emb,
        mock_qdrant_cls,
        mock_decrypt,
        mock_embedding,
        qdrant_params,
        embedding_params,
    ):
        mock_build_emb.return_value = mock_embedding
        expected_store = MagicMock(name="qdrant_vector_store")
        mock_qdrant_cls.from_existing_collection.return_value = expected_store

        result = get_vector_store(**qdrant_params, **embedding_params)

        # -- Embedding model built with correct args --
        mock_build_emb.assert_called_once_with(
            langchain_con=embedding_params["e_langchain_con"],
            model=embedding_params["e_model"],
            base_url=embedding_params["e_base_url"],
            dimensions=embedding_params["e_dimensions"],
            encrypted_api_key=embedding_params["e_encrypted_api_key"],
        )

        # -- API key decrypted --
        mock_decrypt.assert_called_once_with(qdrant_params["vs_encrypted_api_key"])

        # -- Qdrant store created with correct args --
        mock_qdrant_cls.from_existing_collection.assert_called_once_with(
            collection_name=qdrant_params["vs_collection_name"],
            url=qdrant_params["vs_base_url"],
            embedding=mock_embedding,
            port=qdrant_params["vs_port"],
            api_key="decrypted-qdrant-key",
        )

        assert result is expected_store
        

    @patch("vs.get_vs.decrypt")
    @patch("vs.get_vs.QdrantVectorStore")
    @patch("vs.get_vs._build_embedding_model")
    def test_passes_none_api_key_when_not_provided(
        self,
        mock_build_emb,
        mock_qdrant_cls,
        mock_decrypt,
        mock_embedding,
        qdrant_params,
        embedding_params,
    ):
        """When vs_encrypted_api_key is None, decrypt should NOT be called
        and api_key should be passed as None."""
        mock_build_emb.return_value = mock_embedding
        qdrant_params["vs_encrypted_api_key"] = None

        get_vector_store(**qdrant_params, **embedding_params)

        mock_decrypt.assert_not_called()
        _, kwargs = mock_qdrant_cls.from_existing_collection.call_args
        assert kwargs["api_key"] is None


# ---------------------------------------------------------------------------
# Unsupported vendor
# ---------------------------------------------------------------------------

class TestGetVectorStoreUnsupportedVendor:

    @patch("vs.get_vs._build_embedding_model")
    def test_raises_value_error_for_unknown_vendor(
        self,
        mock_build_emb,
        mock_embedding,
        embedding_params,
    ):
        mock_build_emb.return_value = mock_embedding

        with pytest.raises(ValueError, match="currently not supported"):
            get_vector_store(
                vs_collection_name="col",
                vs_vendor="pinecone",
                vs_port=443,
                vs_base_url="https://pinecone.io",
                vs_encrypted_api_key=None,
                **embedding_params,
            )


# ---------------------------------------------------------------------------
# Edge cases / error propagation
# ---------------------------------------------------------------------------

class TestErrorPropagation:

    @patch("vs.get_vs._build_embedding_model", side_effect=Exception("embedding boom"))
    def test_embedding_build_failure_propagates(
        self, mock_build_emb, qdrant_params, embedding_params
    ):
        with pytest.raises(Exception, match="embedding boom"):
            get_vector_store(**qdrant_params, **embedding_params)


    @patch("vs.get_vs.decrypt", side_effect=Exception("decrypt failed"))
    @patch("vs.get_vs._build_embedding_model")
    def test_decrypt_failure_propagates(
        self, mock_build_emb, mock_decrypt, mock_embedding, qdrant_params, embedding_params
    ):
        mock_build_emb.return_value = mock_embedding

        with pytest.raises(Exception, match="decrypt failed"):
            get_vector_store(**qdrant_params, **embedding_params)


    @patch("vs.get_vs.decrypt", return_value="key")
    @patch("vs.get_vs.QdrantVectorStore")
    @patch("vs.get_vs._build_embedding_model")
    def test_qdrant_connection_failure_propagates(
        self, mock_build_emb, mock_qdrant_cls, mock_decrypt, mock_embedding,
        qdrant_params, embedding_params
    ):
        mock_build_emb.return_value = mock_embedding
        mock_qdrant_cls.from_existing_collection.side_effect = ConnectionError("refused")

        with pytest.raises(ConnectionError, match="refused"):
            get_vector_store(**qdrant_params, **embedding_params)