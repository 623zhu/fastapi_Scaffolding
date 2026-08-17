FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -c "import subprocess, sys, tomllib; dependencies = tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']; subprocess.check_call([sys.executable, '-m', 'pip', 'wheel', '--wheel-dir', '/wheels', *dependencies])"

COPY app ./app

RUN python -m pip wheel --no-deps --wheel-dir /wheels .


FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN python -m pip install /wheels/* && rm -rf /wheels

COPY alembic.ini ./
COPY alembic ./alembic

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM runtime AS development

USER root
WORKDIR /workspace
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
