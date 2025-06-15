# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.13
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONPATH="${PYTHONPATH}:/app"
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV DOCKER_RUNTIME=1

ENV QT_QPA_PLATFORM=minimal

ENV UV_PROJECT_ENVIRONMENT="/venv"

ENV UV_CACHE_DIR="/tmp/uv-cache"

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN apt update \
&& apt install -y sudo \
&& pip install uv

COPY pyproject.toml /app/
COPY . ./app/

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

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN apt update && apt install -y \
libgl1-mesa-glx \
libxkbcommon-x11-0 \
libgl1-mesa-dev \
libglib2.0-0 \
libfontconfig \
libdbus-1-3

USER appuser

RUN sudo mkdir -p /venv \
&& sudo chown -R 10001:10001 /venv \
&& sudo mkdir -p /tmp/uv-cache \
&& sudo chown -R 10001:10001 /tmp/uv-cache

USER root

RUN uv sync --no-dev --no-cache
RUN uv add debugpy

CMD uv run python src/gui_setup.py && uv run python src/main.py
