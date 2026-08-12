# Python FastAPI implementation of Decap CMS GitHub OAuth Proxy
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create .env file from environment variables
RUN echo "OAUTH_GITHUB_CLIENT_ID=${OAUTH_GITHUB_CLIENT_ID}" > .env && \
    echo "OAUTH_GITHUB_CLIENT_SECRET=${OAUTH_GITHUB_CLIENT_SECRET}" >> .env && \
    echo "OAUTH_GITHUB_SCOPE=${OAUTH_GITHUB_SCOPE:-repo}" >> .env && \
    echo "HOST=${HOST:-0.0.0.0}" >> .env && \
    echo "PORT=${PORT:-8000}" >> .env

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]