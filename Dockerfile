FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"


CMD ["fastapi", "run", "src/core/web.py", "--port", "8123", "--host", "0.0.0.0"]