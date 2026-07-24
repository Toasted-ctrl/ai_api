from core.config import config
from core.logging import get_logger
from database.schemas import Persons, ApiKeys
from database.session import get_db_session
from database.store_secrets import store_secrets
from database.store_person import store_person
from database.store_user import store_user

log = get_logger()

def create_admin_user():

    with get_db_session(db_url=config.PG_DB_URL) as session:

        # Creating API key entry

        try:

            log.info("Creating Admin Secret...")
            key = store_secrets(
                session=session,
                client=config.ADMIN_CLIENT,
                key_type=config.ADMIN_KEY_TYPE,
                owner_email=config.ADMIN_OWNER_EMAIL,
                require_jwt=config.ADMIN_REQUIRE_JWT,
                require_external_id=config.ADMIN_REQUIRE_GOOGLE_ID,
                api_key=config.ADMIN_API_KEY,
                hmac_secret=config.ADMIN_HMAC
            )

        except ValueError as e:
            log.warning(e)
            result = (
                session.query(ApiKeys.id, ApiKeys.key_type)
                .filter(ApiKeys.owner_email == config.ADMIN_OWNER_EMAIL)
                .first()
            )
            if result:
                key = {
                    "client_id": result.id,
                    "client_key_type": result.key_type
                }

            else:
                log.error("Admin API key not found, unable to proceed...")

        try:

            log.info("Creating Admin Person record...")
            person = store_person(
                session=session,
                first_name=config.ADMIN_FIRST_NAME,
                last_name=config.ADMIN_LAST_NAME,
                email=config.ADMIN_OWNER_EMAIL
            )

        except ValueError as e:
            log.warning(e)
            person = (
                session.query(Persons.id)
                .filter(Persons.email == config.ADMIN_OWNER_EMAIL)
                .scalar()
            )

        try:

            log.info("Creating Admin User record...")
            store_user(
                session=session,
                person_id=person,
                api_key_id=key.get("client_id"),
                key_type=key.get("client_key_type")
            )

        except ValueError as e:
            log.warning(e)

        log.info("Admin User created...")

        return