from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import pytest
import uuid

from database.providers import get_or_create_provider
from database.schemas.user_keys import UserKeysT
from database.user_keys import ProviderAPIKey, get_or_store_key, get_user_active_keys
from security.encryption import encrypt


class TestGetOrStoreKey:

    """Test suite for the get_or_store_function()."""

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            test_key = "test_key_long"
            user_id = uuid.uuid4()

            # Creating a Provider first, otherwise test will fail by default.

            provider = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=False,
                requires_api_key=True,
                host="test_host"
            )

            key = get_or_store_key(
                session=session,
                api_key=test_key,
                user_id=user_id,
                provider_id=provider.id
            )

            assert isinstance(key, ProviderAPIKey)
            assert isinstance(key.user_id, uuid.UUID)
            assert isinstance(key.provider_id, uuid.UUID)
            assert isinstance(key.expiration_date, datetime)
            assert isinstance(key.api_key_short, str)
            assert len(key.api_key_short) == 10
            assert key.api_key == test_key
            assert (
                session.query(UserKeysT.encrypted_api_key)
                .filter(
                    UserKeysT.user_id == user_id,
                    UserKeysT.provider_id == provider.id
                ).scalar()
            ) != test_key


    def test_existing_key(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            test_key = "test_key_long"
            test_key2 = "test_key_long2"
            user_id = uuid.uuid4()

            # Creating a Provider first, otherwise test will fail by default.

            provider = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=False,
                requires_api_key=True,
                host="test_host"
            )

            key = get_or_store_key(
                session=session,
                api_key=test_key,
                user_id=user_id,
                provider_id=provider.id
            )

            key2 = get_or_store_key(
                session=session,
                api_key=test_key2,
                user_id=user_id,
                provider_id=provider.id
            )

            assert isinstance(key, ProviderAPIKey)
            assert isinstance(key2, ProviderAPIKey)
            assert key == key2
            assert session.query(UserKeysT).count() == 1


    def test_invalid_provider(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            with pytest.raises(
                ValueError
            ):
                get_or_store_key(
                    session=session,
                    api_key="test_api_key",
                    user_id=uuid.uuid4(),
                    provider_id=uuid.uuid4()
                )


class TestGetUserActiveKeys:

    """Test suite for the get_user_active_keys() function."""

    def test_valid_nonconfigured(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            result = get_user_active_keys(
                session=session,
                user_id=uuid.uuid4()
            )

            assert isinstance(result, list)
            assert len(result) == 0


    def test_valid_configured(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            test_user = uuid.uuid4()

            provider = get_or_create_provider(
                session=session,
                name="test_name",
                langchain_con="test_con",
                base_url="test_url",
                internal=False,
                requires_api_key=True,
                host="test_host"
            )
            
            key = get_or_store_key(
                session=session,
                api_key="test_key",
                user_id=test_user,
                provider_id=provider.id
            )

            result = get_user_active_keys(
                session=session,
                user_id=test_user
            )

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], ProviderAPIKey)


    def test_expired_key(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            test_user_id = uuid.uuid4()

            key = UserKeysT(
                encrypted_api_key=encrypt("test_encrypted_key"),
                api_key_short="test_encrypted_key"[:10],
                provider_id=uuid.uuid4(),
                user_id=test_user_id,
                expiration_date=datetime.now() - timedelta(days=1)
            )

            session.add(key)
            session.flush()

            assert session.query(UserKeysT).count() == 1
            assert (
                session.query(UserKeysT.expiration_date)
                .filter(UserKeysT.user_id == test_user_id)
                .scalar()
            ) < datetime.now()

            result = get_user_active_keys(
                session=session,
                user_id=test_user_id
            )

            assert isinstance(result, list)
            assert len(result) == 0