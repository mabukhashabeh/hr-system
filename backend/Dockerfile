FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv \
    && uv pip install --system .

# Copy project
COPY . .

# Copy entry script and make it executable
COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

# Expose port
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/entry.sh"]