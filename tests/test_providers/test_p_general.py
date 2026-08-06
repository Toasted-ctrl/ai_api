import uuid

from database.providers import Provider
from providers.general import get_providers_configured_user


class TestGetProvidersConfiguredUser:

    """Test suite for the get_providers_configured_user() function."""

    def test_valid(self):

        p_list = []

        p1 = Provider(
            id=uuid.uuid4(),
            name="test_name",
            base_url="test_url",
            internal=True,
            requires_api_key=False,
            langchain_con="test_con",
            api_key_configured=False,
            mac_address="test_mac_1"
        )

        p_list.append(p1)

        p2 = Provider(
            id=uuid.uuid4(),
            name="test_name2",
            base_url="test_url2",
            internal=False,
            requires_api_key=True,
            langchain_con="test_con",
            api_key_configured=True,
            mac_address="test_mac_2"
        )

        p_list.append(p2)

        p3 = Provider(
            id=uuid.uuid4(),
            name="test_name3",
            base_url="test_url3",
            internal=False,
            requires_api_key=True,
            langchain_con="test_con",
            api_key_configured=False,
            mac_address="test_mac_3"
        )

        p_list.append(p3)

        result = get_providers_configured_user(providers=p_list)

        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Provider)
        assert isinstance(result[1], Provider)