import pytest

from security.encryption import encrypt, decrypt

class TestEncrypt:

    """Test battery for the encrypt() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self):

        content = "Test sentence to encrypt: Bamboozle!"
        result = encrypt(content=content)
        assert isinstance(result, str)
        assert result != ""


    # -------------------------------------------------------------------
    # Error propagation
    # -------------------------------------------------------------------

    def test_invalid_input(self):
        with pytest.raises(TypeError, match="Content must be a string"):
            encrypt(6)


    def test_empty_string(self):
        with pytest.raises(ValueError, match="Empty string"):
            encrypt("")


class TestDecrypt:

    """Test battery for the decrypt() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self):

        content = "gAAAAABqZ3Zm0FtN64eL5OnyFJB6WZoVNlhiNn3DKwSJrmvr3-j-olzyVHD7BqZ-pKd8ledQyhlTzbdOEQ3QAlrFoyRBc-F21VfWpMPUq83SygYi3AdlDMkJQjIncdXFDvemIqm0FGqa"
        result = decrypt(content=content)
        assert isinstance(result, str)
        assert result == "Test sentence to encrypt: Bamboozle!"


    # -------------------------------------------------------------------
    # Error propagation
    # -------------------------------------------------------------------  

    def test_invalid_input(self):
        with pytest.raises(TypeError, match="Content must be a string"):
            decrypt(6)
    
    
    def test_empty_string(self):
        with pytest.raises(ValueError, match="Empty string"):
            decrypt("")