import json
import os
import uuid

from core.logging import get_logger
from database.providers import get_or_create_provider
from database.schemas.clients import ClientsT
from database.schemas.persons_users import UsersT, PersonsT
from database.schemas.providers import ProvidersT
from database.schemas.user_keys import UserKeysT
from database.schemas.vector_store import VectorStoreSettingsT
from database.schemas.vector_store_collections import VectorStoreCollectionT
from database.session import get_db_session_ctx
from security.encryption import encrypt
from security.hash import get_hash_sha256

log = get_logger()


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


def create_preconfigured_vector_store() -> None:
    """Loads the configure_init_vs.json file and adds all preconfigured vector stores to the database.
    Will force a shutdown if the file is missing."""
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_vs.json')
    if not os.path.exists(file_path):
        log.error("ENV: CREATE_PRECONFIGURED_VS is enabled, but 'configure_init_vs.json' is missing. Shutting down ...")
        raise SystemExit(1)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    num_vs = len(data)
    if num_vs == 0:
        log.error("ENV: CREATE_PRECONFIGURED_VS is enabled, but 'configure_init_vs.json' is empty. Shutting down ..." )
        raise SystemExit(1)

    for vs in data:
        with get_db_session_ctx() as session:
            exists = (
                session.query(VectorStoreSettingsT)
                .filter(VectorStoreSettingsT.id == uuid.UUID(vs.get("id")))
                .all()
            )

            if len(exists) > 0:
                log.info(f"Vector Store '{vs.get("vendor")}' with URL '{vs.get("base_url")}' already exists, skipping ...")
                continue

            log.info(f"Adding new Vector Store, vendor '{vs.get("vendor")}', URL '{vs.get("base_url")}' ...")
            with get_db_session_ctx() as session:
                nvs = VectorStoreSettingsT(
                    id=uuid.UUID(vs.get("id")),
                    encrypted_api_key=encrypt(vs.get("api_key")),
                    vendor=vs.get("vendor"),
                    base_url=vs.get("base_url"),
                    port=vs.get("port")
                )

                session.add(nvs)
                log.info("Vectore Store added.")

    log.info("DONE: All Vector Stores configured.")
    return


def create_preconfigured_vector_store_collections() -> None:
    """Loads the configure_init_vs_colections.json file and adds all preconfigured collections to the database.
    Will force a shutdown if the file is missing."""
            
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_vs_collections.json')
    if not os.path.exists(file_path):
        log.error(
            "ENV: CREATE_PRECONFIGURED_VS_COLLECTIONS is enabled, but 'configure_init_vs_collections.json' is missing. "
            "Shutting down ..."
        )
        raise SystemExit(1)
        
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    num_col = len(data)
    if num_col == 0:
        log.error(
            "ENV: CREATE_PRECONFIGURED_VS is enabled, but 'configure_init_vs_collections.json' is empty. "
            "Shutting down ..."
        )
        raise SystemExit(1)

    with get_db_session_ctx() as session:
        for col in data:
            exists = (
                session.query(VectorStoreCollectionT)
                .filter(VectorStoreCollectionT.id == uuid.UUID(col.get("id")))
                .all()
            )
                
            if len(exists) > 0:
                log.info(f"Vector Store collection '{col.get("name")}' already exists, skipping ...")
                continue

            log.info(f"Adding new Vector Store with name '{col.get("name")}' ...")
            ncol = VectorStoreCollectionT(
                id=uuid.UUID(col.get("id")),
                name=col.get("name"),
                vector_store_id=uuid.UUID(col.get("vector_store_id")),
                e_provider=col.get("embedding_provider"),
                e_model=col.get("embedding_model"),
                e_dimensions=col.get("embedding_dimensions"),
                access_type=col.get("access_type"),
                required_filters=col.get("required_filters")
            )

            session.add(ncol)
            log.info(f"Vector Store collection '{col.get("name")}' added.")

    log.info("DONE: All Vector collections configured.")
    return


def create_preconfigured_application_clients() -> None:
    """Loads the configure_init_clients.json file and adds all preconfigured application clients to the database.
    Will force a shutdown if the file is missing."""
                
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_clients.json')
    if not os.path.exists(file_path):
        log.error(
            "ENV: CREATE_PRECONFIGURED_APPLICATION_CLIENTS is enabled, but 'configure_init_clients.json' is missing. "
            "Shutting down ..."
        )
        raise SystemExit(1)
            
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    clients = data.get("applications")
        
    num_clients = len(clients)
    if num_clients == 0:
        log.error(
            "ENV: CREATE_PRECONFIGURED_CLIENTS is enabled, but 'configure_init_clients.json' > 'applications' is empty. "
            "Shutting down ..."
        )
        raise SystemExit(1)

    for client in clients:
        with get_db_session_ctx() as session:
            exists = (
                session.query(ClientsT)
                .filter(ClientsT.id == client.get("id"))
                .all()
            )

            if len(exists) > 0:
                log.info(f"Client '{client.get("client_name")}' already exists, skipping ...")
                continue

            nc = ClientsT(
                id=uuid.UUID(client.get("id")),
                api_key_hash=get_hash_sha256(client.get("api_key")),
                key_type="Application",
                require_jwt=client.get("require_jwt"),
                is_active=True,
                require_external_id=True,
                encrypted_owner_email=encrypt(client.get("owner_email")),
                encrypted_hmac_secret=encrypt(client.get("hmac")),
                encrypted_client_name=encrypt(client.get("client_name")),
                encrypted_redirect_uri=encrypt(client.get("redirect_uri")),
                blind_index_client_name=get_hash_sha256(client.get("client_name")),
                blind_index_owner_email=get_hash_sha256(client.get("owner_email"))
            )

            session.add(nc)
            log.info(f"Added Client '{client.get("client_name")}' to the database ...")

    log.info("DONE: All application Clients configured.")
    return


def create_preconfigured_user_clients() -> None:
    """Loads the configure_init_clients.json file and adds all preconfigured user clients to the database.
    Will force a shutdown if the file is missing."""
                    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'configure_init_clients.json')
    if not os.path.exists(file_path):
        log.error(
            "ENV: CREATE_PRECONFIGURED_VS_COLLECTIONS is enabled, but 'configure_init_clients.json' is missing. "
            "Shutting down ..."
        )
        raise SystemExit(1)
                
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    clients = data.get("users")
            
    num_clients = len(clients)
    if num_clients == 0:
        log.error(
            "ENV: CREATE_PRECONFIGURED_USER_CLIENTS is enabled, but 'configure_init_clients.json' > 'users' is empty. "
            "Shutting down ..."
        )
        raise SystemExit(1)

    for client in clients:

        with get_db_session_ctx() as session:

            c_exists = (
                session.query(ClientsT)
                .filter(ClientsT.id == uuid.UUID(client.get("client_id")))
                .all()
            )
            
            if len(c_exists) > 0:
                log.info(f"Client '{client.get("client_name")}' already exists, skipping client creation.")

            else:
                nc = ClientsT(
                    id=uuid.UUID(client.get("client_id")),
                    api_key_hash=get_hash_sha256(client.get("api_key")),
                    key_type="User",
                    require_jwt=client.get("require_jwt"),
                    is_active=True,
                    require_external_id=True,
                    encrypted_owner_email=encrypt(client.get("owner_email")),
                    encrypted_hmac_secret=encrypt(client.get("hmac")),
                    encrypted_client_name=encrypt(client.get("client_name")),
                    encrypted_redirect_uri=None,
                    blind_index_client_name=get_hash_sha256(client.get("client_name")),
                    blind_index_owner_email=get_hash_sha256(client.get("owner_email"))
                    )
            
                session.add(nc)
                log.info(f"Added Client '{client.get("client_name")}' to the database ...")

            p_exists = (
                session.query(PersonsT)
                .filter(PersonsT.id == uuid.UUID(client.get("person_id")))
                .all()
            )

            if len(p_exists) > 0:
                log.info(f"User with Client ID '{client.get("client_id")}' already exists, skipping person and user generation ...")

            else:

                np = PersonsT(
                    id=uuid.UUID(client.get("person_id")),
                    encrypted_email=encrypt(client.get("owner_email")),
                    encrypted_first_name=encrypt(client.get("first_name")),
                    encrypted_last_name=encrypt(client.get("last_name")),
                    blind_index_email=get_hash_sha256(client.get("owner_email"))
                )

                session.add(np)

                nu = UsersT(
                    person_id=uuid.UUID(client.get("person_id")),
                    api_key_id=uuid.UUID(client.get("client_id")),
                    external_id=None,
                    login_provider=None
                )

                session.add(nu)
                log.info(f"Created new user for Client '{client.get("client_id")}' ...")

            session.flush()

            user_id = (
                session.query(UsersT.id)
                .filter(UsersT.api_key_id == uuid.UUID(client.get("client_id")))
                .scalar()
            )

            log.info(f"User ID is '{user_id}' for Client '{client.get("client_id")}' ...")

            api_keys = client.get("keys")
            if api_keys == []:
                log.info(f"No user keys configured for user with Client ID '{client.get("client_id")}', skipping key creation ...")

            else:
                for key, value in api_keys.items():
                    provider_id = (
                        session.query(ProvidersT.id)
                        .filter(ProvidersT.name == key)
                        .scalar()
                    )

                    k_exists = (
                        session.query(UserKeysT)
                        .filter(UserKeysT.provider_id == provider_id, UserKeysT.user_id == user_id)
                        .all()
                    )

                    if len(k_exists) > 0:
                        log.info(f"Key '{key}' already exists for user '{user_id}', skipping key creation ...")
                        continue

                    else:
                        nk = UserKeysT(
                            user_id=user_id,
                            provider_id=provider_id,
                            encrypted_api_key=encrypt(value),
                            api_key_short=value[:10]
                        )

                    session.add(nk)
                    log.info(f"'{key}' added for user '{user_id}' ...")

    log.info("DONE: All user Clients configured.")
    return