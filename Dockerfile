# Optimized Dockerfile for faster builds
FROM python:3.12-slim

# Set environment variables for performance
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app directory and non-root user early
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apt-get remove -y gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean

# Copy application files (order matters for caching)
COPY ml_pipeline.py .
COPY app.py .
COPY templates/ templates/
COPY models/ models/

# Create models directory with proper permissions
RUN mkdir -p models && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5001

# Optimized health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run app
CMD ["python", "app.py"]

# Metadata
LABEL maintainer="ML Team" \
      version="1.0.1" \
      description="Optimized ML Model API Service"
