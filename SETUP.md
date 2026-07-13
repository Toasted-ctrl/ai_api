# Environment
First, rename the .env.example file:
```bash
mv .env.example .env
```
Open the .env file, and add your own environment variables:
```bash
sudo nano .env
```
Redis 6+ is required. Make sure to enter redis credentials to cache all calls.
# Run Docker Container
```bash
docker compose up
```