from core.config import config
from security.hmac import hash_hmac, is_valid_hmac

class TestHashHmac:

    """Test battery for the hash_hmac function."""

    def test_valid(self):

        key = config.BLIND_INDEX_HMAC_KEY
        content = "test_content"

        result = hash_hmac(content=content, key=key)

        assert result == "348d7cb8035cdfa9d340de16c195c144c5dadd2f59860b3aaa2c030ed01661ab"


class TestIsValidHMAC:

    """Test battery for the is_valid_hmac() function."""

    def test_invalid(self):

        key = config.BLIND_INDEX_HMAC_KEY
        content_1 = "TEST_1"
        content_2 = "TEST_2"

        hmac_1 = hash_hmac(content=content_1, key=key)
        hmac_2 = hash_hmac(content=content_2, key=key)

        result = is_valid_hmac(hmac_1, hmac_2)

        assert isinstance(result, bool)
        assert result == False


    def test_valid(self):

        key = config.BLIND_INDEX_HMAC_KEY
        content = "TEST"
        
        hmac_1 = hash_hmac(content=content, key=key)
        hmac_2 = hash_hmac(content=content, key=key)
        
        result = is_valid_hmac(hmac_1, hmac_2)
        
        assert isinstance(result, bool)
        assert result == True