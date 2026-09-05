from fastapi import FastAPI
import openai

from .exc_openai import not_found_handler


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the app."""
    app.add_exception_handler(openai.NotFoundError, not_found_handler)