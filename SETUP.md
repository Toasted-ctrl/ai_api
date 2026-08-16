# Setup Guide

> [!NOTE]
> This document was last reviewed on 2026-08-16.

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
cp src/init/configure_init_providers_example.json src/setup/configure_init_providers.json
nano src/init/configure_init_providers.json
```

Fill in the provider details according to your infrastructure.

### Clients

```bash
cp src/init/configure_init_clients_example.json src/setup/configure_init_clients.json
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

## 3. Docker Compose Deployment

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

## 4. Kubernetes Deployment

The repository includes Kubernetes manifests in the k8s/ directory for deploying the API to a Kubernetes cluster.

### Prerequisites

You will need:

- A running Kubernetes cluster
- kubectl configured to access the cluster
- An image of the application pushed to a container registry accessible by the cluster
- An NGINX Ingress Controller if you want to use the included Ingress configuration

The manifests create a dedicated artificial-intelligence-api namespace.

### 4.1 Configure the Secret

Copy the example Secret manifest:

```bash
cp k8s/secret.yaml.example k8s/secret.yaml
```

Edit k8s/secret.yaml and replace the placeholder values with your PostgreSQL, Redis, encryption, JWT, and optional Google OAuth credentials.

```bash
nano k8s/secret.yaml
```

Do **not** commit k8s/secret.yaml containing real credentials to the repository.

The Secret is consumed by the application Deployment as environment variables.

### 4.2 Configure the Container Image

Copy the example Deployment:

```bash
cp k8s/deployment.yaml.example k8s/deployment.yaml
```

Edit k8s/deployment.yaml and replace:

```yaml
image: "YOUR IMAGE REPOSITORY/artificial-intelligence-api:latest"
```

with the image you want Kubernetes to deploy, for example:

```yaml
image: "registry.example.com/artificial-intelligence-api:latest"
```

The example Deployment runs three replicas and is configured for rolling updates. It also expects an image-pull secret named registry-credentials when pulling from a private registry.

If your registry is private, create the pull secret before deploying:

```bash
kubectl create secret docker-registry registry-credentials \
  --docker-server=<REGISTRY> \
  --docker-username=<USERNAME> \
  --docker-password=<PASSWORD> \
  --namespace=artificial-intelligence-api
```

### 4.3 Review the ConfigMap

The default ConfigMap contains the non-sensitive application configuration:

```yaml
APP_ENV: "production"
LOG_LEVEL: "info"
PG_PORT: "5432"
PG_DIALECT: "postgresql"
PG_DRIVER: "psycopg2"
REDIS_PORT: "6379"
COOKIE_SECURE: "false"
COOKIE_MAX_AGE: "86400"
ENABLE_GOOGLE_LOGIN: "false"
```

Adjust these values in k8s/configmap.yaml if required by your environment. Sensitive values should remain in the Kubernetes Secret rather than the ConfigMap.

### 4.4 Deploy the Application

From the repository root, apply the Kubernetes manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pv.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Verify that the resources were created:

```bash
kubectl get all -n artificial-intelligence-api
```

Check the deployment:

```bash
kubectl get deployment -n artificial-intelligence-api
```

Check the pods:

```bash
kubectl get pods -n artificial-intelligence-api
```

The Deployment exposes the application on container port 8000 and the Service exposes it internally on port 80.

### 4.5 Ingress

The repository includes an NGINX Ingress configuration for:

`http://ai-api.k8s.internal`

Apply it with:

```bash
kubectl apply -f k8s/ingress.yaml
```

The Ingress routes traffic to artificial-intelligence-api-service on port 80.

If you use a different hostname, edit k8s/ingress.yaml before applying it:

```yaml
rules:
  - host: your-hostname.example.com
```

Make sure DNS or your local /etc/hosts configuration resolves the hostname to the NGINX Ingress Controller.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis connection errors | Verify Redis 6+ is running and credentials in `.env` are correct |
| PostgreSQL connection errors | Verify PostgreSQL is running and credentials in `.env` are correct |
| Preconfigured data not loading | Ensure the JSON config files exist (without `.example`) and `CREATE_PRECONFIGURED_CLIENTS` / `CREATE_PRECONFIGURED_PROVIDERS` are set to `true` |
| Container won't start | Run `docker compose logs` to check for specific error messages |