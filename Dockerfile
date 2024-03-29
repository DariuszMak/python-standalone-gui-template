# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV DOCKER_RUNTIME=1

ENV QT_QPA_PLATFORM=minimal


WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN apt update \
 && apt install -y sudo

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

RUN python -m venv /opt/venv
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    . /opt/venv/bin/activate && python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . ./app

ADD . /app
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD . /opt/venv/bin/activate && python src/gui_setup.py && python src/main.py
