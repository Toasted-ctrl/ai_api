from core.logging import get_logger
from init.create_tables import create_tables
from init.preconfigurations import (
    create_preconfigured_clients,
    create_preconfigured_providers
)

# -------------------------------------------------------------------
# Init file to create all database tables and initial users
# -------------------------------------------------------------------

# This file should only be executed if you need to set up the required
# database tables, as well as when needing to create the preconfigured clients.

CREATE_TABLES = True
CREATE_PRECONFIGURED_CLIENTS = True
CREATE_PRECONFIGURED_PROVIDERS = True

log = get_logger()

if CREATE_TABLES:
    create_tables()

if CREATE_PRECONFIGURED_PROVIDERS:
    create_preconfigured_providers()

if CREATE_PRECONFIGURED_CLIENTS:
    try:
        create_preconfigured_clients()
    except ValueError as e:
        log.info(e)