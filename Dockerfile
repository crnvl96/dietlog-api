FROM python:3.12-slim

WORKDIR /root

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /root

RUN uv sync --frozen --no-cache

EXPOSE 8000

ENTRYPOINT ["/root/.venv/bin/fastapi", "run", "/root/app/main.py", "--port", "8000", "--host", "0.0.0.0", "--reload"]
