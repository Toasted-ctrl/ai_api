print("\n>>> STARTING INITIALiZATION PROCESS\n")

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
CREATE_PRECONFIGURED_USER_CLIENTS = True
CREATE_PRECONFIGURED_APPLICATION_CLIENTS = True
CREATE_PRECONFIGURED_PROVIDERS = True
CREATE_PRECONFIGURED_VECTOR_STORES = True
CREATE_PRECONFIGURED_VECTOR_STORE_COLLECTIONS = True

log = get_logger()

print("\n---- STARTING TABLE CREATION ----\n")
if CREATE_TABLES:
    create_tables()

print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED PROVIDERS ----\n")
if CREATE_PRECONFIGURED_PROVIDERS:
    create_preconfigured_providers()

print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED APPLICATION CLIENTS ----\n")
if CREATE_PRECONFIGURED_APPLICATION_CLIENTS:
    create_preconfigured_application_clients()

print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED USER CLIENTS ----\n")
if CREATE_PRECONFIGURED_USER_CLIENTS:
    create_preconfigured_user_clients()

print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED VECTOR STORES ----\n")
if CREATE_PRECONFIGURED_VECTOR_STORES:
    create_preconfigured_vector_store()

print("\n---- STARTING CREATION OF / CHECKING PRECONFIGURED VECTOR STORE COLLECTIONS ----\n")
if CREATE_PRECONFIGURED_VECTOR_STORE_COLLECTIONS:
    create_preconfigured_vector_store_collections()

print("\n>>> DONE: FINISHED INITIALIZATION!\n")