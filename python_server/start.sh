#!/usr/bin/env bash
# Start the Decap CMS GitHub OAuth Proxy server using uv

echo "..:: Alwatr Decap CMS Backend ::.."
echo "Starting server with uv..."
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "Using .env file for configuration"
else
    echo "Warning: No .env file found. Using environment variables."
fi

echo "Available routes:"
echo "  GET /          - Service info"
echo "  GET /auth      - Initiate GitHub OAuth"
echo "  GET /callback  - OAuth callback handler"
echo ""

# Run the server with uv
uv run python run.py

