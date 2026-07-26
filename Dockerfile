# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /opt/service
RUN python -m pip install "uv==0.11.32"
COPY pyproject.toml uv.lock README.md ./
COPY app ./app
RUN uv sync --locked --no-dev --no-editable

FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/service/.venv/bin:${PATH}"

RUN groupadd --system --gid 10001 service \
    && useradd --system --uid 10001 --gid service --home-dir /nonexistent service

WORKDIR /opt/service
COPY --from=builder /opt/service/.venv /opt/service/.venv

COPY alembic.ini ./
COPY migrations ./migrations

USER 10001:10001
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
