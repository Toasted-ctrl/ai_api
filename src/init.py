print("\n>>> STARTING INITIALiZATION PROCESS\n")

from langgraph.checkpoint.postgres import PostgresSaver

from core.config import config
from core.logging import get_logger
from init.create_tables import create_tables
from init.preconfigurations import (
    create_preconfigured_application_clients,
    create_preconfigured_user_clients,
    create_preconfigured_providers,
    create_preconfigured_vector_store,
    create_preconfigured_vector_store_collections
)

# -------------------------------------------------------------------
# Init file to create all database tables and initial users
# -------------------------------------------------------------------

# This file should only be executed if you need to set up the required
# database tables, as well as when needing to create the preconfigured clients.

CREATE_TABLES = True
CREATE_CHECKPOINT_TABLES = True
CREATE_PRECONFIGURED_USER_CLIENTS = True
CREATE_PRECONFIGURED_APPLICATION_CLIENTS = True
CREATE_PRECONFIGURED_PROVIDERS = True
CREATE_PRECONFIGURED_VECTOR_STORES = True
CREATE_PRECONFIGURED_VECTOR_STORE_COLLECTIONS = True

log = get_logger()

if CREATE_TABLES:
    print("\n---- STARTING TABLE CREATION ----\n")
    create_tables()

if CREATE_PRECONFIGURED_PROVIDERS:
    print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED PROVIDERS ----\n")
    create_preconfigured_providers()

if CREATE_PRECONFIGURED_APPLICATION_CLIENTS:
    print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED APPLICATION CLIENTS ----\n")
    create_preconfigured_application_clients()

if CREATE_PRECONFIGURED_USER_CLIENTS:
    print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED USER CLIENTS ----\n")
    create_preconfigured_user_clients()

if CREATE_PRECONFIGURED_VECTOR_STORES:
    print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED VECTOR STORES ----\n")
    create_preconfigured_vector_store()

if CREATE_PRECONFIGURED_VECTOR_STORE_COLLECTIONS:
    print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED VECTOR STORE COLLECTIONS ----\n")
    create_preconfigured_vector_store_collections()

if CREATE_CHECKPOINT_TABLES:
    print("\n---- STARTING CREATION OF CHECKPOINT TABLES ----\n")
    with PostgresSaver.from_conn_string(conn_string=config.PG_CHECKPOINTER_URL) as checkpointer:
        checkpointer.setup()
        log.info("DONE: Checkpoint tables created.")

print("\n>>> DONE: FINISHED INITIALIZATION!\n")