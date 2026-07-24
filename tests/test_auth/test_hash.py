import pytest

from auth.hash import get_hash_sha356

def test_valid():

    input = "test_input"
    output = get_hash_sha356(input=input)
    assert isinstance(output, str)
    assert output == "952822de6a627ea459e1e7a8964191c79fccfb14ea545d93741b5cf3ed71a09a"


def test_invalid_input_type():

    input = 7
    with pytest.raises(
        ValueError,
        match="Input must be of type string"
    ):
        get_hash_sha356(input=input)


def test_empty_string():

    input = ""
    with pytest.raises(
        ValueError,
        match="Input must not be empty string"
    ):
        get_hash_sha356(input=input)