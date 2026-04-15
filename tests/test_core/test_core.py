import pytest

from core.config import config

class TestSupportedModels:

    def test_supported_llms(self):
        result = config.supported_models(type="llms")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_supported_vector_embeddings(self):
        result = config.supported_models(type="vector_embeddings")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_supported_translators(self):
        result = config.supported_models(type="translations")
        assert isinstance(result, dict)
        assert len(result) > 0

    def testValueError(self):
        with pytest.raises(
            ValueError,
            match="Invalid type"):
            config.supported_models(type="test")