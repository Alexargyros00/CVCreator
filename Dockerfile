# Use the official Python image
FROM python:3.13-slim

# Install system dependencies for Playwright/Chromium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Configure Flask for container networking and cleaner logs.
ENV FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000 \
    PYTHONUNBUFFERED=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (without installing the project itself yet)
RUN uv sync --frozen --no-cache

# Install Playwright and Chromium
RUN uv run playwright install --with-deps chromium

# Copy the rest of the application
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Start the application using the virtualenv created at build time
CMD [".venv/bin/python", "app.py"]
