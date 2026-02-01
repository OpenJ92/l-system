FROM python:3.14-slim

WORKDIR /app

# Useful dev basics (optional, but common)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Copy only packaging metadata first (better Docker layer caching)
COPY pyproject.toml README.md LICENSE ./

# Install your package in editable mode with dev extras
RUN pip install --no-cache-dir -U pip

# Now copy the actual source
COPY . .

CMD ["bash"]
