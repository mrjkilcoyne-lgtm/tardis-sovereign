# =============================================================================
# TARDIS Sovereign Dispatch - Multi-stage Docker build
# Minimal image for cost-efficient Civo deployment
# =============================================================================

# --- Stage 1: Build ---
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build deps only (no dev deps in production)
COPY pyproject.toml ./
COPY sovereign_dispatch/ ./sovereign_dispatch/
COPY config/ ./config/

RUN pip install --no-cache-dir --prefix=/install .

# --- Stage 2: Runtime ---
FROM python:3.12-slim AS runtime

# Non-root user for security
RUN groupadd -r sovereign && useradd -r -g sovereign -d /app sovereign

WORKDIR /app

# Copy only the installed packages and source
COPY --from=builder /install /usr/local
COPY --from=builder /build/config/default.yaml /app/config/default.yaml
COPY --from=builder /build/sovereign_dispatch/ /app/sovereign_dispatch/

# Create data directory for cache/ledger
RUN mkdir -p /data && chown sovereign:sovereign /data

# Minimal HTTP API wrapper
COPY infrastructure/civo/serve.py /app/serve.py

USER sovereign

EXPOSE 8080

ENV PYTHONUNBUFFERED=1
ENV SOVEREIGN_CONFIG=/config/default.yaml

# Health check built into the serve.py
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=2 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

CMD ["python", "/app/serve.py"]
