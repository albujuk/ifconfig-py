ARG PYTHON_VERSION=3.14.2
ARG ALPINE_VERSION=3.23

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_NO_CACHE=1

WORKDIR /home/appuser/ifconfig-py

COPY pyproject.toml uv.lock ./
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --no-editable --no-dev

COPY app/ ./app/
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv pip install --no-deps .

FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/ifconfig-py/.venv/bin:${PATH}" \
    PORT=8000 \
    HOST=0.0.0.0

RUN adduser -s /bin/sh -D appuser

USER appuser
WORKDIR /home/appuser/ifconfig-py

COPY --from=builder --chown=appuser:appuser /home/appuser/ifconfig-py/.venv ./.venv
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser docker/entrypoint.sh ./docker/entrypoint.sh
RUN chmod +x docker/entrypoint.sh

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider ${HOST}:${PORT}/health || exit 1

ENTRYPOINT ["./docker/entrypoint.sh"]
