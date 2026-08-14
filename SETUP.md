# Setup Guide

## Prerequisites

- **Docker** and **Docker Compose** installed
- **Redis 6+** instance (local or hosted)
- **PostgreSQL** instance (local or hosted)
- **UV**

---

## 1. Environment Configuration

Copy the example environment file and open it for editing:

```bash
cp .env.example .env
nano .env
```

Fill in each section as described below.

### Redis Credentials

A Redis 6+ instance is required. Some API GET requests are cached through Redis.

```env
REDIS_USER=your_redis_user
REDIS_HOSTNAME=your_redis_host
REDIS_PASSWORD=your_redis_password
REDIS_PREFIX=your_prefix
REDIS_PORT=6379
```

### PostgreSQL Credentials

```env
PG_HOSTNAME=your_pg_host
PG_USERNAME=your_pg_user
PG_PASSWORD=your_pg_password
PG_DATABASE=your_database_name
PG_DIALECT=postgresql
PG_DRIVER=psycopg2
PG_PORT=5432
```

### Encryption

All sensitive data is encrypted at rest. You must provide a strong encryption key.

```env
ENCRYPTION_KEY=your_encryption_key
```

### Blind Index

The blind index key is used for searchable encryption. Generate a separate key from your encryption key.

```env
BLIND_INDEX_KEY=your_blind_index_key
```

### JWT Secret

Used to sign and verify authentication tokens.

```env
JWT_SECRET=your_jwt_secret
```

### Logging

Available levels: `debug`, `info`, `warn`, `error`

```env
LOG_LEVEL=debug
```

### Google Login (Optional)

Set `ENABLE_GOOGLE_LOGIN=true` and fill in the remaining fields only if you want to enable Google OAuth.

```env
ENABLE_GOOGLE_LOGIN=false
GOOGLE_CLIENT_ID=
GOOGLE_REDIRECT_URI=
GOOGLE_AUTH_URL=
GOOGLE_HMAC=
GOOGLE_TOKEN_URL=
GOOGLE_CLIENT_SECRET=
```

---

## 2. Configure Initial Clients and Providers (Optional)

> [!NOTE]
> If skipping this step, you'll need to add all tables manually.

in src/init.py, set whether you want to create all tables, as well as preconfigured Providers and Clients / Users:
```python
CREATE_PRECONFIGURED_CLIENTS=true       # Seed initial Clients/Users from src/init/configure_init_clients.json
CREATE_PRECONFIGURED_PROVIDERS=true     # Seed initial Providers from src/init/configure_init_providers.json
CREATE_TABLES=true                      # Create required database tables
```

### Providers

```bash
cp src/init/configure_init_providers.json.example src/setup/configure_init_providers.json
nano src/init/configure_init_providers.json
```

Fill in the provider details according to your infrastructure.

### Clients

```bash
cp src/init/configure_init_clients.json.example src/setup/configure_init_clients.json
nano src/init/configure_init_clients.json
```

There are two types of clients:

| Type | Description | Where to add |
|------|-------------|--------------|
| **Application Client** | A backend service or application that calls the API on behalf of users. Users do not interact with the API directly. | Add under the `applications` section |
| **User Client** | A client where users interact with the API directly (e.g., a frontend application). | Add under the `users` section |

Add each client to the appropriate section in the configuration file based on how it will interact with the API.

### Init Tables & Users
From the root directory, run:
```bash
uv run src/init.py
```

---

## 3. Run the Application

```bash
docker compose up
```

To run in detached mode:

```bash
docker compose up -d
```

To verify the container is running:

```bash
docker compose ps
```

To view logs:

```bash
docker compose logs -f
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis connection errors | Verify Redis 6+ is running and credentials in `.env` are correct |
| PostgreSQL connection errors | Verify PostgreSQL is running and credentials in `.env` are correct |
| Preconfigured data not loading | Ensure the JSON config files exist (without `.example`) and `CREATE_PRECONFIGURED_CLIENTS` / `CREATE_PRECONFIGURED_PROVIDERS` are set to `true` |
| Container won't start | Run `docker compose logs` to check for specific error messages |