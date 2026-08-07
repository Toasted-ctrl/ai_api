from core.config import config

# -------------------------------------------------------------------
# Happy-path tests
# -------------------------------------------------------------------

def test_db_url():

    assert isinstance(config.PG_DB_URL, str)


def test_model_types():

    assert isinstance(config.MODEL_TYPES, dict)
    keys = config.MODEL_TYPES.keys()
    assert "chat_completion" in keys
    assert "vector_embedding" in keys
    assert "image_generation" in keys
    assert "translation" in keys
    assert "audio_transcription" in keys
    assert "safeguard" in keys

    assert isinstance(config.MODEL_TYPES["chat_completion"], list)
    assert isinstance(config.MODEL_TYPES["vector_embedding"], list)
    assert isinstance(config.MODEL_TYPES["image_generation"], list)
    assert isinstance(config.MODEL_TYPES["translation"], list)
    assert isinstance(config.MODEL_TYPES["audio_transcription"], list)
    assert isinstance(config.MODEL_TYPES["safeguard"], list)


def test_blind_index_hmac():

    assert isinstance(config.BLIND_INDEX_HMAC_KEY, bytes)


def test_google_hmac():

    assert isinstance(config.GOOGLE_HMAC_SECRET, bytes)


def test_translation_models():

    assert isinstance(config.TRANSLATION_MODELS, list)


def test_vector_embedding_models():

    assert isinstance(config.VECTOR_EMBEDDING_MODELS, list)


def test_chat_completion_models():

    assert isinstance(config.CHAT_COMPLETION_MODELS, list)