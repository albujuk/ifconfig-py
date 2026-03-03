#!/bin/sh
set -e

export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}
exec fastapi run app/main.py --host "$HOST" --port "$PORT"
