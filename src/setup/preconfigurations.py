import json
import os

from core.config import config
from core.logging import get_logger
from database.providers import get_or_create_provider, get_provider
from database.schemas.clients import ClientsT
from database.schemas.persons_users import UsersT
from database.session import get_db_session_ctx
from database.user_keys import get_or_store_key
from security.hmac import hash_hmac
from setup.application_client import create_application_client
from setup.user_client_user import create_user_client_user

log = get_logger()

def create_preconfigured_clients() -> None:

    """Loads the configure_init_clients.json file and adds all preconfigured clients to the database.
    Will force a shutdown if the file appears misconfigured."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_clients.json')
    if not os.path.exists(file_path):
        log.error("ENV: CREATE_PRECONFIGURED_CLIENTS is enabled, but 'configure_init_clients.json' is missing. Shutting down...")
        raise SystemExit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data.get("configured", False) == False:
        log.error("ENV: CREATE_PRECONFIGURED_CLIENTS is enabled, but 'configure_init_clients.json' appears misconfigured. Shutting down...")
        raise SystemExit(1)

    # TODO: Perhaps we need to build in some kind of check that validates all info is present 
    # per preconfigured client / user? Applies to both user clients and application clients.

    try:
        user_clients = data.get("users")
        if len(user_clients) == 0:
            log.info("No Backend Clients to configure, skipping...")
        else:
            for client in user_clients:
                with get_db_session_ctx() as session:
                    log.info("Creating User Client")
                    create_user_client_user(
                        session=session,
                        client_name=client.get("client_name"),
                        key_type=client.get("key_type"),
                        owner_email=client.get("owner_email"),
                        require_external_id=client.get("require_external_id"),
                        require_jwt=client.get("require_jwt"),
                        api_key=client.get("api_key"),
                        hmac_secret=client.get("hmac"),
                        first_name=client.get("first_name"),
                        last_name=client.get("last_name")
                    )

                    # TODO: Key creation will skip if user already created.
                    # Fix that it won't skip, also probably should fix the below. Works but janky.

                    if 'keys' in client.keys():

                        client_id = (
                            session.query(ClientsT.id)
                            .filter(
                                ClientsT.key_type == "User",
                                ClientsT.blind_index_owner_email == hash_hmac(
                                    content=client.get("owner_email"),
                                    key=config.BLIND_INDEX_HMAC_KEY
                                ),
                                ClientsT.blind_index_client_name == hash_hmac(
                                    content=client.get("client_name"),
                                    key=config.BLIND_INDEX_HMAC_KEY
                                )
                            )
                            .scalar()
                        )
                        log.info(f"Add keys: located User Client: '{client_id}'")

                        user_id = (
                            session.query(UsersT.id)
                            .filter(UsersT.api_key_id == client_id)
                            .scalar()
                        )
                        log.info(f"Add keys: located User ID: '{user_id}'")

                        log.info("Attempting to add User Client preconfigured keys...")
                        for provider, key in client.get("keys").items():
                            log.info(f"Add key: Adding Provider '{provider}' with key {key[:10]}...")
                            prov = get_provider(
                                session=session,
                                provider_name=provider
                            )
                            get_or_store_key(
                                session=session,
                                api_key=key,
                                provider_id=prov.id,
                                user_id=user_id
                            )
                        log.info("Add keys: All keys were added.")

    except ValueError as e:
        log.info(e)

    try:

        application_clients = data.get("applications")
        if len(application_clients) == 0:
            log.info("No Application Clients to configure, skipping...")
        else:
            for client in application_clients:
                with get_db_session_ctx() as session:
                    log.info("Creating Application Client...")
                    create_application_client(
                        session=session,
                        client_name=client.get("client_name"),
                        key_type=client.get("key_type"),
                        owner_email=client.get("owner_email"),
                        require_external_id=client.get("require_external_id"),
                        require_jwt=client.get("require_jwt"),
                        api_key=client.get("api_key"),
                        hmac_secret=client.get("hmac")
                    )

    except ValueError as e:
        log.info(e)

    return None


def create_preconfigured_providers() -> None:

    """Loads the configure_init_providers.json file and adds all preconfigured providers to the database.
    Will force a shutdown if the file appears misconfigured."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_providers.json')
    if not os.path.exists(file_path):
        log.error("ENV: CREATE_PRECONFIGURED_PROVIDERS is enabled, but 'configure_init_providers.json' is missing. Shutting down...")
        raise SystemExit(1)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data.get("configured", False) == False:
        log.error("ENV: CREATE_PRECONFIGURED_PROVIDERS is enabled, but 'configure_init_providers.json' appears misconfigured. Shutting down...")
        raise SystemExit(1)

    providers = data.get("providers")
    if len(providers) == 0:
        log.info("No Providers to configure, skipping...")
        return None

    for provider in providers:
        with get_db_session_ctx() as session:
            get_or_create_provider(
                session=session,
                name=provider.get("name"),
                langchain_con=provider.get("langchain_con"),
                base_url=provider.get("base_url"),
                internal=provider.get("internal"),
                requires_api_key=provider.get("requires_api_key"),
                host=provider.get("host"),
                mac_address=provider.get("mac_address")
            )

    return None