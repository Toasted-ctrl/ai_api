# Use Python image
FROM python:3.14-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /code

ARG VERSION
ENV APP_VERSION=${VERSION}

# Copy dependency files and install dependencies
COPY ./pyproject.toml /code/pyproject.toml
COPY ./uv.lock /code/uv.lock
RUN uv sync --frozen --no-cache

# Copy the application code
COPY ./src /code/app

# Setting src as pythonpath
ENV PYTHONPATH=/code/app

# Command to run the app
CMD ["uv", "run", "--frozen", "python", "-m", "app.main"]