# AI Api (AIA)

![Python](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

> A unified API gateway for multiple LLM providers.

This project intends to build an "Artificial Intelligence API" (AIA), which will serve as an API gateway to multiple LLM providers. Currently only Ollama is supported, but the intention is to add support for more providers later on (Anthropic, OpenAI, Melious, etc.).

## Features
- Login support (Google OAuth2) for Applications intended to serve multiple users.
- API Key verification for users that should be allowed to poll the API directly, no Login required.
- Chat completion through LLM providers.
- Local Ollama configurations may be added.

## Tech Stack
- FastAPI
- LangChain
- Ollama
- Docker (Compose)
- Redis
- PostgreSQL
- GCP (OAuth2)

## Setup
- Please check the 'SETUP.md' file to get started.

## API Endpoints
> All Endpoints are prefixed with '/api/v1'.

- GET /auth/google/login
- GET /auth/google/callback
- POST /chat_completion
- GET /models
- GET /models/chat_completion
- GET /models/translation
- GET /models/vector_embedding
- GET /providers
- GET /servers
- POST /servers/wake/{provider_name}
- GET /status
- GET /translation/translategemma
- POST /translation/translategemma

## Roadmap
### Short Term
- Tests for all base functionalities (i.e., Google Login)
- Making Redis caching optional.

### Long Term
- Implement support for various LLM providers (OpenAI, Anthropic, Melious, etc.), expanding beyond Ollama.
- Add support for more Login providers.
- Add agent building functionalities.
- Add support for storing API Keys for external providers in the database.
- Log conversation ids and history in a conversation table.
- Enable possibility to share agents with other users.
- Build 'testing' endpoints, which is intended to build tests for agents you created.
- Add MCP calling support.
- Add upload of documents endpoint, including vector embedding said documents.

## Contributing
PRs welcome!

## Documentation
Full interactive API documentation is available at `/docs` (Swagger UI)
or `/redoc` (ReDoc) when the server is running.