FROM python:3.12-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock ./

# install dependencies into the system python (no venv needed in container)
RUN uv sync --frozen --no-dev --no-editable

# copy source
COPY src/ ./src/

# install the package itself
RUN uv pip install --system --no-deps -e .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uv", "run", "archivist"]
