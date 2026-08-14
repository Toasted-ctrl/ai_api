# Artificial Intelligence API (AIA)

![Python](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-v1.28-blue?logo=kubernetes&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

> A unified API gateway for multiple LLM providers.

This project intends to build an "Artificial Intelligence API" (AIA), which will serve as an API gateway to multiple LLM providers. The goal is to make an easy to integrate unified API, which could easily be self-hosted on low-power hardware.

## Features
- Login support (Google OAuth2) for Applications intended to serve multiple users.
- API Key verification for users that should be allowed to poll the API directly, no Login required.
- Chat completion through LLM providers.
- Local Ollama configurations may be added.
- Users may add their own API keys for interaction with third party LLM Providers.

## Tech Stack
- FastAPI
- LangChain
- Docker (Compose)
- Redis
- PostgreSQL
- GCP (OAuth2)
- Kubernetes

## Supported LLM Providers
- Current supported Providers are tested and verified with personally obtained API keys.

### Current
- Ollama (if self-hosted)
- Anthropic
- Melious

### Upcoming
- OpenAI

## Setup
- Please check the 'SETUP.md' file to get started.

## API Endpoints
> All Endpoints are prefixed with '/api/v1'.

### GET
- GET /auth/google/login
- GET /auth/google/callback
- GET /models
- GET /models/chat_completion
- GET /models/translation
- GET /models/vector_embedding
- GET /providers
- GET /root
- GET /status
- GET /translation/translategemma

### POST
- POST /chat_completion
- POST /translation/translategemma

## Roadmap

### Short Term
- Tests for all base functionalities (i.e., Google Login).
- Making Redis caching optional.
- Add HMAC hashing and verification for each path.
- Add Chat Completion support for all supported Providers.
- Add OpenAI support.
- Build a function to locate which server is currently supporting translategemma: Check internal
servers first, follow by external ones. Return internal as this one is free of charge.

### Long Term
- Caching solution for internal non-route functions, to avoid repeat expensive calls.
- Add support for more Login providers.
- Add agent building functionalities.
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