#!/usr/bin/env bash

CURRENT_DIR="$(pwd)"
cd "$(dirname "$0")"

npx --yes vitest run

cd "$CURRENT_DIR"
