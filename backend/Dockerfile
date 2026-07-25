# syntax=docker/dockerfile:1

# =========================================================
# Stage 1: Build Python dependencies
# =========================================================
FROM python:3.13.13-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev \
    && python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV/bin/pip" install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /build

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


# =========================================================
# Stage 2: Final runtime image
# =========================================================
FROM python:3.13.13-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libpq5 \
        curl \
    && groupadd --system django \
    && useradd \
        --system \
        --gid django \
        --create-home \
        --home-dir /home/django \
        django \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY --chown=django:django . /app

RUN mkdir -p /app/staticfiles \
    && chown -R django:django /app

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s \
    --timeout=5s \
    --start-period=20s \
    --retries=3 \
    CMD curl --fail http://127.0.0.1:${PORT}/api/health/live/ || exit 1

CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT} --workers=${GUNICORN_WORKERS:-3} --threads=${GUNICORN_THREADS:-2} --timeout=${GUNICORN_TIMEOUT:-120} --access-logfile=- --error-logfile=-"]