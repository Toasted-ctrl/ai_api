from sqlalchemy.orm import Session
import pytest

from core.config import config
from database.store_client import store_client, StoredClient
from database.schemas.clients import ClientsT
from security.encryption import decrypt
from security.hash import get_hash_sha256
from security.hmac import hash_hmac


class TestCreateApiKey:

    """Test battery for the create_api_key function."""

    # -------------------------------------------------------------------
    # Happy-path tests
    # -------------------------------------------------------------------

    def test_valid(self, test_db_engine):
        with Session(bind=test_db_engine) as session:

            hmac = "test_hmac"

            _client = store_client(
                session=session,
                client_name="test_client",
                key_type="User",
                owner_email="test_mail",
                hmac_secret=hmac
            )
            session.commit()

            assert (
                session.query(ClientsT)
                .filter(ClientsT.api_key_hash == get_hash_sha256(_client.api_key))
                .count()
            ) == 1

            assert (
                session.query(ClientsT.encrypted_hmac_secret)
                .filter(
                    ClientsT.blind_index_owner_email == hash_hmac(
                        content="test_mail",
                        key=config.BLIND_INDEX_HMAC_KEY
                    )
                )
                .scalar()
            ) != hmac

            assert decrypt(
                (
                    session.query(ClientsT.encrypted_hmac_secret)
                    .filter(
                        ClientsT.blind_index_owner_email == hash_hmac(
                        content="test_mail",
                        key=config.BLIND_INDEX_HMAC_KEY
                        )
                    )
                    .scalar()
                )
            ) == hmac

            assert isinstance(_client, StoredClient)
            assert _client.hmac_secret == hmac

            session.close()
            

    # -------------------------------------------------------------------
    # Error propagation
    # -------------------------------------------------------------------

    def test_duplicate_key(self, test_db_engine):
        with Session(bind=test_db_engine) as session:
            test_client = "test_client"
            secrets = store_client(
                session=session,
                client_name=test_client,
                key_type="User",
                owner_email="test_mail"
            )
            session.commit()
            with pytest.raises(
                ValueError,
                match=f"Client '{test_client}' with owner 'test_mail' already exists"
            ):
                secrets2 = store_client(
                    session=session,
                    client_name=test_client,
                    key_type="User",
                    owner_email="test_mail"
                )
                session.commit()
            session.close()