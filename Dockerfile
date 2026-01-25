FROM python:3.14.2-alpine3.23 AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_NO_CACHE=1

WORKDIR /home/appuser/app

COPY pyproject.toml uv.lock ./
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --no-editable --no-dev

COPY main.py .
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv pip install --no-deps .

FROM python:3.14.2-alpine3.23

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/app/.venv/bin:${PATH}" \
    PORT=8000 \
    HOST=0.0.0.0

RUN adduser -s /bin/sh -D appuser

USER appuser
WORKDIR /home/appuser/app

COPY --from=builder --chown=appuser:appuser /home/appuser/app/.venv ./.venv
COPY --chown=appuser:appuser . .

#RUN chmod +x entrypoint.sh

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider ${HOST}:${PORT}/health || exit 1

ENTRYPOINT ["./entrypoint.sh"]