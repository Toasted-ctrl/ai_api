# AI Api (AIA)

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

> A unified API gateway for multiple LLM providers
This project intends to build an "Artificial Intelligence API" (AIA), which whill serve as an API gateway to multiple LLM providers. Currently only Ollama is supported, but the intention is to add support for more providers later on (Anthropic, OpenAI, MeliousAI, etc.).

## Features
- Login support (Google OAuth2) for Applications intended to serve multiple users.
- API Key verification for users that should be allowed to poll the API directly, no Login required.

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