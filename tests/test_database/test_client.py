from unittest.mock import MagicMock
import pytest
import uuid

from database.client import ApplicationClient, get_client_from_client_id
from database.schemas.clients import ClientsT


# -------------------------------------------------------------------
# Test Fixtures
# -------------------------------------------------------------------

@pytest.fixture
def mock_session():
    """Provides a mocked SQLAlchemy Session."""
    return MagicMock()


@pytest.fixture
def sample_client_id():
    """Provides a consistent UUID for testing."""
    return uuid.UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def sample_client(sample_client_id):
    """Provides a mocked ClientsT database row."""
    client = MagicMock(spec=ClientsT)
    client.id = sample_client_id
    client.encrypted_redirect_uri = "encrypted_uri_value"
    return client


class TestGetClientFromClientId:
    """Tests for the get_client_from_client_id function."""

    def test_returns_application_client_when_client_exists(
        self, mock_session, sample_client_id, sample_client
    ):
        """Should return an ApplicationClient when a matching client is found."""
        mock_session.query.return_value.filter.return_value.one_or_none.return_value = (
            sample_client
        )

        result = get_client_from_client_id(mock_session, sample_client_id)

        assert isinstance(result, ApplicationClient)
        assert result.id == sample_client_id
        assert result.encrypted_redirect_uri == "encrypted_uri_value"

        mock_session.query.assert_called_once_with(ClientsT)


    def test_raises_lookup_error_when_client_not_found(
        self, mock_session, sample_client_id
    ):
        """Should raise LookupError when no client matches the provided client_id."""
        mock_session.query.return_value.filter.return_value.one_or_none.return_value = (
            None
        )

        with pytest.raises(LookupError, match=f"Invalid Client ID: {sample_client_id}"):
            get_client_from_client_id(mock_session, sample_client_id)