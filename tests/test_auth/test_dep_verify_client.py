from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound
from unittest.mock import MagicMock, patch
import pytest
import uuid

from auth.dep_verify_client import (
    VerifiedClient,
    depends_get_client,
    depends_get_application_client,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_session():
    """Provides a mocked SQLAlchemy session."""
    return MagicMock()


@pytest.fixture
def sample_client_id():
    return uuid.uuid4()


@pytest.fixture
def mock_client_row(sample_client_id):
    """Simulates a row returned from the ClientsT table."""
    client = MagicMock()
    client.id = sample_client_id
    client.key_type = "Application"
    return client


@pytest.fixture
def mock_non_application_client_row(sample_client_id):
    """Simulates a client row with a non-Application key_type."""
    client = MagicMock()
    client.id = sample_client_id
    client.key_type = "Service"
    return client


class TestDependsGetClient:

    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_valid_api_key_returns_verified_client(
        self, mock_hash, mock_session, mock_client_row
    ):
        mock_session.query().filter().one_or_none.return_value = mock_client_row

        result = depends_get_client(api_key="valid-key", session=mock_session)

        assert isinstance(result, VerifiedClient)
        assert result.id == mock_client_row.id
        assert result.key_type == mock_client_row.key_type


    def test_empty_api_key_raises_401(self, mock_session):
        with pytest.raises(HTTPException) as exc_info:
            depends_get_client(api_key="", session=mock_session)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Missing API Key"


    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_no_matching_client_raises_401(self, mock_hash, mock_session):
        mock_session.query().filter().one_or_none.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            depends_get_client(api_key="unknown-key", session=mock_session)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid API Key"


    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_multiple_results_raises_500(self, mock_hash, mock_session):
        mock_session.query().filter().one_or_none.side_effect = MultipleResultsFound

        with pytest.raises(HTTPException) as exc_info:
            depends_get_client(api_key="dup-key", session=mock_session)

        assert exc_info.value.status_code == 500
        assert "Unexpected error" in exc_info.value.detail


    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_hash_called_with_api_key(self, mock_hash, mock_session, mock_client_row):
        mock_session.query().filter().one_or_none.return_value = mock_client_row

        depends_get_client(api_key="my-secret-key", session=mock_session)

        mock_hash.assert_called_with("my-secret-key")


    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_returns_correct_key_type(self, mock_hash, mock_session, sample_client_id):
        client = MagicMock()
        client.id = sample_client_id
        client.key_type = "Service"
        mock_session.query().filter().one_or_none.return_value = client

        result = depends_get_client(api_key="service-key", session=mock_session)

        assert result.key_type == "Service"


    @patch("auth.dep_verify_client.get_hash_sha256", return_value="hashed_key")
    def test_none_client_is_treated_as_missing(self, mock_hash, mock_session):
        """Covers the `if not client` branch when one_or_none returns None."""
        mock_session.query().filter().one_or_none.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            depends_get_client(api_key="some-key", session=mock_session)

        assert exc_info.value.status_code == 401


# ---------------------------------------------------------------------------
# depends_get_application_client tests
# ---------------------------------------------------------------------------

class TestDependsGetApplicationClient:

    def test_application_key_type_passes(self, sample_client_id):
        client = VerifiedClient(id=sample_client_id, key_type="Application")

        result = depends_get_application_client(client=client)

        assert result is client
        assert result.id == sample_client_id
        assert result.key_type == "Application"


    @pytest.mark.parametrize(
        "key_type",
        ["service", "APPLICATION", "Admin", "Internal", "", "application"],
    )
    def test_non_exact_application_key_type_raises_403(self, sample_client_id, key_type):
        """key_type matching is case-sensitive and must be exactly 'Application'."""
        client = VerifiedClient(id=sample_client_id, key_type=key_type)

        with pytest.raises(HTTPException) as exc_info:
            depends_get_application_client(client=client)

        assert exc_info.value.status_code == 403
        assert "frontend application" in exc_info.value.detail