from auth.create_api_key import create_api_key

def test_valid():

    key = create_api_key()

    assert isinstance(key, str)
    assert len(key) == 86