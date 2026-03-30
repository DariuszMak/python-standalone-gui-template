# syntax=docker/dockerfile:1

ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    DOCKER_RUNTIME=1 \
    QT_QPA_PLATFORM=minimal \
    UV_PROJECT_ENVIRONMENT="/venv" \
    UV_CACHE_DIR="/tmp/uv-cache"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    sudo \
    libgl1-mesa-dev \
    libxkbcommon-x11-0 \
    libglib2.0-0t64 \
    libfontconfig \
    libdbus-1-3 \
    binutils \
    libgssapi-krb5-2 \
    libssl-dev \
    libqt5network5 \
    dos2unix \
    curl \
    && pip install uv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

COPY pyproject.toml /app/

RUN sudo mkdir -p /venv /tmp/uv-cache \
    && sudo chown -R ${UID}:${UID} /venv /tmp/uv-cache

USER root

RUN uv sync --no-dev --no-cache
RUN uv add debugpy

WORKDIR /app/src/ui/react_ui/frontend

COPY src/ui/react_ui/frontend/package.json ./

RUN npm install --include=optional

COPY src/ui/react_ui/frontend ./

RUN npm run build

WORKDIR /app

CMD uv run python src/gui_setup.py \
    && uv run python src/node_setup.py \
    && uv run python src/main.py