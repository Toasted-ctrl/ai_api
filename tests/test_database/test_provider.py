from sqlalchemy.orm import Session
import uuid

from database.providers import (
    get_or_create_provider,
    Provider,
    get_all_provider_configurations,
    get_providers_by_location,
    UserProviderRegistry,
    ProviderConfiguration
)
from database.schemas.providers import ProvidersT


class TestGetOrCreateProvider:

    """Test suite for the get_or_create_provider() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            provider = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=True,
                requires_api_key=False,
                host="test_host"
            )

            assert provider is not None
            assert isinstance(provider, Provider)
            assert isinstance(provider.id, uuid.UUID)
            assert isinstance(provider.name, str)
            assert isinstance(provider.base_url, str)
            assert isinstance(provider.langchain_con, str)
            assert isinstance(provider.requires_api_key, bool)
            assert isinstance(provider.internal, bool)


    def test_duplicate(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            provider1 = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=True,
                requires_api_key=False,
                host="test_host"
            )

            provider2 = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=True,
                requires_api_key=False,
                host="test_host"
            )

            record_count = (
                session.query(ProvidersT)
                .count()
            )

            assert record_count == 1
            assert isinstance(provider1, Provider)
            assert isinstance(provider2, Provider)


class TestGetAllProvidersSupportUser:

    """Test suite for the get_all_provider_configurations() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            
            provider1 = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=True,
                requires_api_key=False,
                host="test_host"
            )

            provider2 = get_or_create_provider(
                session=session,
                name="test_name_2",
                langchain_con="test_con_2",
                base_url="test_url_2",
                internal=True,
                requires_api_key=False,
                host="test_host_2"
            )

            p_count = (
                session.query(ProvidersT).count()
            )

            assert p_count == 2

            providers = get_all_provider_configurations(
                session=session,
                user_id=uuid.uuid4()
            )

            assert isinstance(providers, UserProviderRegistry)

            p1: ProviderConfiguration = getattr(providers, "test_name")
            assert isinstance(p1, ProviderConfiguration)
            assert isinstance(p1.base_url, str)
            assert isinstance(p1.api_key_configured, bool)
            assert isinstance(p1.id, uuid.UUID)
            assert isinstance(p1.internal, bool)

            assert p1.name == "test_name"

            p2: ProviderConfiguration = getattr(providers, "test_name_2")
            assert isinstance(p2, ProviderConfiguration)
            assert isinstance(p2.base_url, str)
            assert isinstance(p2.api_key_configured, bool)
            assert isinstance(p2.id, uuid.UUID)
            assert isinstance(p2.internal, bool)

            assert p2.name == "test_name_2"


class TestGetProvidersByLocation:

    """Test suite for the get_providers_by_location() function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
                
            provider1 = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=True,
                requires_api_key=False,
                host="test_host"
            )
    
            provider2 = get_or_create_provider(
                session=session,
                name="test_name_2",
                langchain_con="test_con_2",
                base_url="test_url_2",
                internal=False,
                requires_api_key=False,
                host="test_host_2"
            )

            internal = get_providers_by_location(
                session=session,
                is_internal=True
            )

            assert len(internal) == 1
            assert isinstance(internal, list)
            assert isinstance(internal[0], Provider)

            external = get_providers_by_location(
                session=session,
                is_internal=False
            )

            assert len(external) == 1
            assert isinstance(external, list)
            assert isinstance(external[0], Provider)