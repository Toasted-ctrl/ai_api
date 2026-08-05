import json
import os

from core.logging import get_logger
from database.providers import get_or_create_provider
from database.session import get_db_session_ctx
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
                id=provider.get("id"),
                name=provider.get("name"),
                langchain_con=provider.get("langchain_con"),
                base_url=provider.get("base_url"),
                internal=provider.get("internal"),
                requires_api_key=provider.get("requires_api_key"),
                host=provider.get("host"),
                mac_address=provider.get("mac_address")
            )

    return None