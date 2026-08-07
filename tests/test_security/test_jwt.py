from joserfc.errors import ExpiredTokenError, InvalidClaimError
import pytest
import uuid

from security.jwt import create_jwt, decode_jwt, DecodedJWT

class TestCreateJWT:

    """Test suite for the 'create_jwt()' function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self):

        test_client_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_client_id")
        test_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_user_id")

        result = create_jwt(
            client_id=test_client_id,
            user_id=test_user_id
        )

        assert isinstance(result, str)
        assert len(result.split(sep=".")) == 3


class TestDecodeJWT:

    """Test suite for the 'decode_jwt()' function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self):

        test_client_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_client_id")
        test_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_user_id")
        
        jwt = create_jwt(
            client_id=test_client_id,
            user_id=test_user_id
        )

        assert isinstance(jwt, str)
        assert len(jwt.split(sep=".")) == 3

        decoded = decode_jwt(token=jwt)

        assert isinstance(decoded, DecodedJWT)
        assert isinstance(decoded.aud, uuid.UUID)
        assert isinstance(decoded.sub, uuid.UUID)
        assert isinstance(decoded.iat, int)
        assert isinstance(decoded.exp, int)
        assert isinstance(decoded.iss, str)
        assert decoded.iss == "AIA"
        assert decoded.sub == test_user_id
        assert decoded.aud == test_client_id


    # -------------------------------------------------------------------
    # Error propagation
    # -------------------------------------------------------------------

    def test_expired(self):

        test_client_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_client_id")
        test_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_user_id"),
        test_exp_seconds = -10
                
        jwt = create_jwt(
            client_id=test_client_id,
            user_id=test_user_id,
            exp_seconds=test_exp_seconds
        )

        with pytest.raises(
            ExpiredTokenError,
            match="expired_token: The token is expired"
        ):

            decode_jwt(token=jwt)


    def test_invalid_claim(self):
    
        test_client_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_client_id")
        test_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, "test_user_id"),
        test_iss = "test_iss"
                    
        jwt = create_jwt(
            client_id=test_client_id,
            user_id=test_user_id,
            iss=test_iss
        )
    
        with pytest.raises(
            InvalidClaimError,
            match="invalid_claim: Invalid claim: 'iss'"
        ):
    
            decode_jwt(token=jwt)