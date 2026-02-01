FROM python:3.14-slim

WORKDIR /app

# Useful dev basics (optional, but common)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Copy everything (including src/)
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# Install your package in editable mode with dev extras
RUN pip install --no-cache-dir -U pip  && \
    pip install --no-cache-dir -e ".[dev]"

COPY . .    

CMD ["bash"]
