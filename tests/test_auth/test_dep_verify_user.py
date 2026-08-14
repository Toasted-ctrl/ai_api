from fastapi import HTTPException, status
from sqlalchemy.exc import MultipleResultsFound
from unittest.mock import MagicMock, patch
import pytest
import uuid

from auth.dep_verify_client import VerifiedClient
from auth.dep_verify_user import VerifiedUser, depends_verify_user


@pytest.fixture
def mock_session():
    """Create a mock SQLAlchemy session."""
    session = MagicMock()
    return session


@pytest.fixture
def make_client():
    """Factory fixture to create a VerifiedClient with configurable fields."""
    def _make_client(key_type: str = "User", client_id: uuid.UUID = None):
        if client_id is None:
            client_id = uuid.uuid4()
        return VerifiedClient(id=client_id, key_type=key_type)
    return _make_client


@pytest.fixture
def mock_user():
    """Create a mock user DB row."""
    user = MagicMock()
    user.id = uuid.uuid4()
    return user


# -------------------------------------------------------------------
# Happy-path tests
# -------------------------------------------------------------------

class TestDepVerUsrSuccess:

    def test_returns_verified_user_for_valid_user_key(
        self, mock_session, make_client, mock_user
    ):
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.return_value = mock_user

        result = depends_verify_user(client=client, session=mock_session)

        assert isinstance(result, VerifiedUser)
        assert result.id == mock_user.id


    def test_verified_user_id_matches_db_user_id(
        self, mock_session, make_client, mock_user
    ):
        expected_id = uuid.uuid4()
        mock_user.id = expected_id
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.return_value = mock_user

        result = depends_verify_user(client=client, session=mock_session)

        assert result.id == expected_id


# -------------------------------------------------------------------
# Application Key Rejection
# -------------------------------------------------------------------

class TestDepVerUsrApplicationKey:

    def test_raises_401_for_application_key(self, mock_session, make_client):
        client = make_client(key_type="Application")

        with pytest.raises(HTTPException) as exc_info:
            depends_verify_user(client=client, session=mock_session)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Application key JWT decoding not yet supported" in exc_info.value.detail


    def test_does_not_query_db_for_application_key(self, mock_session, make_client):
        client = make_client(key_type="Application")

        with pytest.raises(HTTPException):
            depends_verify_user(client=client, session=mock_session)

        mock_session.query.assert_not_called()


# -------------------------------------------------------------------
# Unexpected Key Type
# -------------------------------------------------------------------

class TestDepVerUsrUnexpectedKeyType:

    @pytest.mark.parametrize("bad_key_type", ["Admin", "Service", "", "unknown", "user"])
    def test_raises_500_for_unexpected_key_type(
        self, mock_session, make_client, bad_key_type
    ):
        client = make_client(key_type=bad_key_type)

        with pytest.raises(HTTPException) as exc_info:
            depends_verify_user(client=client, session=mock_session)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Unexpected error" in exc_info.value.detail


    @patch("auth.dep_verify_user.log")
    def test_logs_error_for_unexpected_key_type(
        self, mock_log, mock_session, make_client
    ):
        client = make_client(key_type="BadType")

        with pytest.raises(HTTPException):
            depends_verify_user(client=client, session=mock_session)

        mock_log.error.assert_called_once()
        assert "BadType" in mock_log.error.call_args[0][0]


# -------------------------------------------------------------------
# Multiple Results
# -------------------------------------------------------------------

class TestDepVerUsrMultipleResults:

    def test_raises_500_on_multiple_results(self, mock_session, make_client):
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.side_effect = MultipleResultsFound()

        with pytest.raises(HTTPException) as exc_info:
            depends_verify_user(client=client, session=mock_session)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Unexpected error" in exc_info.value.detail


    @patch("auth.dep_verify_user.log")
    def test_logs_critical_on_multiple_results(
        self, mock_log, mock_session, make_client
    ):
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.side_effect = MultipleResultsFound()

        with pytest.raises(HTTPException):
            depends_verify_user(client=client, session=mock_session)

        mock_log.critical.assert_called_once()
        assert str(client.id) in mock_log.critical.call_args[0][0]


# -------------------------------------------------------------------
# No User Found
# -------------------------------------------------------------------

class TestDepVerUsrNoUserFound:

    def test_raises_401_when_no_user_found(self, mock_session, make_client):
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            depends_verify_user(client=client, session=mock_session)

        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid API Key" in exc_info.value.detail


    @patch("auth.dep_verify_user.log")
    def test_logs_warning_when_no_user_found(
        self, mock_log, mock_session, make_client
    ):
        client = make_client(key_type="User")
        mock_session.query().filter().one_or_none.return_value = None

        with pytest.raises(HTTPException):
            depends_verify_user(client=client, session=mock_session)

        mock_log.warning.assert_called_once()
        assert str(client.id) in mock_log.warning.call_args[0][0]