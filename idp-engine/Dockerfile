FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

WORKDIR /app

# Install minimal system dependencies + tini for proper PID 1 handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r app && useradd -r -g app app

# Install Python dependencies (deterministic, no cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

# Set proper ownership
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Use tini as init system
ENTRYPOINT ["tini", "--"]

# Start worker
CMD ["python", "app/worker.py"]