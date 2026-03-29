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

RUN apt-get update \
&& apt-get install -y sudo \
&& pip install uv

COPY pyproject.toml /app/
COPY uv.lock /app/

ARG UID=10001
RUN adduser \
--disabled-password \
--gecos "" \
--home "/nonexistent" \
--shell "/sbin/nologin" \
--no-create-home \
--uid "${UID}" \
appuser

RUN adduser appuser sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER appuser

RUN apt-get update && apt-get install -y \
libgl1-mesa-dev \
libxkbcommon-x11-0 \
libgl1-mesa-dev \
libglib2.0-0t64 \
libfontconfig \
libdbus-1-3 \
binutils \
libgssapi-krb5-2 \
libssl-dev \
libqt5network5 \
dos2unix

RUN apt-get update && apt-get install -y curl \
 && curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
 && apt-get install -y nodejs

COPY src/ui/react_ui/frontend/package*.json /app/src/ui/react_ui/frontend/
WORKDIR /app/src/ui/react_ui/frontend
RUN npm install -g npm@latest
RUN npm install --include=optional
COPY src/ui/react_ui/frontend /app/src/ui/react_ui/frontend
RUN npm run build

WORKDIR /app

RUN sudo mkdir -p /venv \
&& sudo chown -R 10001:10001 /venv \
&& sudo mkdir -p /tmp/uv-cache \
&& sudo chown -R 10001:10001 /tmp/uv-cache

RUN uv sync --no-dev --locked --no-cache
RUN uv add debugpy

CMD uv run python src/gui_setup.py && uv run python src/node_setup.py && uv run python src/main.py
