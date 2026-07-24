from auth.create_secret import create_secret

def test_valid():

    key = create_secret()

    assert isinstance(key, str)
    assert len(key) == 86