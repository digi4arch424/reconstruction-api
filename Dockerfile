# =============================================================================
# reconstruction-api
# Generic spatial reconstruction pipeline API
# Build: docker build -t reconstruction-api .
# =============================================================================

FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies first for layer cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Shell form ensures $PORT expands correctly on Fly.io and Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"]
