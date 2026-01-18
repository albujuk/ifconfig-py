FROM python:3.14.2-alpine3.23

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 
    
RUN adduser -s /bin/sh -D appuser

USER appuser

WORKDIR /home/appuser/app


COPY --chown=appuser:appuser . .

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --no-editable --no-dev && \
    uv pip install --no-deps . && \
    rm -rf ifconfig_py.egg-info build

ENTRYPOINT [".venv/bin/fastapi", "run", "main.py"]
