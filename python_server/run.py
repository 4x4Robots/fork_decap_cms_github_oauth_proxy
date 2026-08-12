#!/usr/bin/env python3
"""
Convenience script to run the FastAPI server.
Usage: python run.py
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from main import app, HOST, PORT
    
    print("..:: Alwatr Decap CMS Backend ::..")
    print(f"Starting server on {HOST}:{PORT}")
    print(f"Available routes:")
    print(f"  GET /          - Service info")
    print(f"  GET /auth      - Initiate GitHub OAuth")
    print(f"  GET /callback   - OAuth callback handler")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )