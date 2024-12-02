FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/.poetry /app/.cache /tmp/aoc_solutions && \
    chmod 777 /app/.poetry /app/.cache /tmp/aoc_solutions

# Install poetry
RUN pip install poetry

# Configure poetry environment
ENV POETRY_HOME=/app/.poetry
ENV POETRY_CACHE_DIR=/app/.cache
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy just the poetry files first
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Run as non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run the application with proper host binding
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]