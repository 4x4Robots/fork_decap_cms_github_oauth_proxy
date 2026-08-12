#!/usr/bin/env python3
"""
FastAPI reimplementation of the Decap CMS GitHub OAuth Proxy Server

This server provides OAuth2 proxy functionality for GitHub authentication,
allowing a Decap CMS frontend to authenticate users via GitHub.

Routes:
- GET /          : Health check and service info
- GET /auth      : Initiate GitHub OAuth flow
- GET /callback   : Handle GitHub OAuth callback

Environment Variables:
- OAUTH_GITHUB_CLIENT_ID     : GitHub OAuth App Client ID
- OAUTH_GITHUB_CLIENT_SECRET : GitHub OAuth App Client Secret  
- OAUTH_GITHUB_SCOPE         : OAuth scope (default: 'repo')
- HOST                        : Server host (default: '0.0.0.0')
- PORT                        : Server port (default: 8000)
"""

import os
import secrets
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration validation
OAUTH_GITHUB_CLIENT_ID = os.getenv("OAUTH_GITHUB_CLIENT_ID")
OAUTH_GITHUB_CLIENT_SECRET = os.getenv("OAUTH_GITHUB_CLIENT_SECRET")
OAUTH_GITHUB_SCOPE = os.getenv("OAUTH_GITHUB_SCOPE", "repo")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

if not OAUTH_GITHUB_CLIENT_ID:
    raise ValueError("OAUTH_GITHUB_CLIENT_ID environment variable is required")
if not OAUTH_GITHUB_CLIENT_SECRET:
    raise ValueError("OAUTH_GITHUB_CLIENT_SECRET environment variable is required")

# GitHub OAuth configuration
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

app = FastAPI(
    title="Decap CMS GitHub OAuth Proxy",
    description="GitHub OAuth2 proxy server for Decap CMS",
    version="1.0.0"
)


def generate_state() -> str:
    """Generate a random state string for CSRF protection."""
    return secrets.token_hex(4)


@app.get("/", response_class=JSONResponse)
async def home():
    """
    Home route that returns service information.
    Equivalent to the TypeScript version's home route.
    """
    return {
        "ok": True,
        "data": {
            "app": "..:: Decap CMS Backend Microservice ::..",
            "message": "Hello"
        }
    }


@app.get("/auth")
async def auth(request: Request, provider: Optional[str] = None):
    """
    Initiate OAuth flow with GitHub.
    
    This route validates the provider parameter and redirects to GitHub's
    authorization endpoint with the appropriate parameters.
    """
    if provider != "github":
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "statusCode": 400,
                "errorCode": "invalid_provider"
            }
        )
    
    # Get the host from the request headers
    host = request.headers.get("host", HOST)
    
    # Generate state for CSRF protection
    state = generate_state()
    
    # Build the authorization URL
    params = {
        "client_id": OAUTH_GITHUB_CLIENT_ID,
        "redirect_uri": f"https://{host}/callback?provider={provider}",
        "scope": OAUTH_GITHUB_SCOPE,
        "state": state
    }
    
    authorization_uri = f"{GITHUB_AUTHORIZE_URL}?" + "&".join(
        f"{k}={v}" for k, v in params.items()
    )
    
    print(f"authorizationUri: {authorization_uri}")
    
    # Return 301 redirect to GitHub
    return RedirectResponse(
        url=authorization_uri,
        status_code=301
    )


@app.get("/callback")
async def callback(request: Request, provider: Optional[str] = None, code: Optional[str] = None):
    """
    Handle OAuth callback from GitHub.
    
    This route validates the provider and code parameters, exchanges the
    authorization code for an access token, and returns an HTML page
    that posts the token back to the opener window.
    """
    if provider != "github":
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "statusCode": 400,
                "errorCode": "invalid_provider"
            }
        )
    
    if not code:
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "statusCode": 400,
                "errorCode": "require_code"
            }
        )
    
    # Get the host from the request headers
    host = request.headers.get("host", HOST)
    
    # Exchange code for access token
    token_data = {
        "client_id": OAUTH_GITHUB_CLIENT_ID,
        "client_secret": OAUTH_GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": f"https://{host}/callback?provider={provider}"
    }
    
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.post(GITHUB_TOKEN_URL, data=token_data, headers=headers)
        response.raise_for_status()
        
        access_token = response.json().get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail={
                    "ok": False,
                    "statusCode": 400,
                    "errorCode": "invalid_token_response"
                }
            )
        
        # Return HTML page that posts the token back to the opener
        html_content = render_body("success", access_token)
        return HTMLResponse(content=html_content)
        
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for token: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "ok": False,
                "statusCode": 400,
                "errorCode": "token_exchange_failed"
            }
        )


def render_body(status: str, token: Optional[str] = None) -> str:
    """
    Render the HTML response for the callback.
    
    This generates the same JavaScript-based response as the TypeScript version,
    which posts the authorization result back to the opener window.
    """
    return f"""
    <script>
      const receiveMessage = (message) => {{
        window.opener.postMessage(
          'authorization:github:{status}:{{JSON.stringify({{ "token": token }})}}',
          message.origin
        );

        window.removeEventListener("message", receiveMessage, false);
      }}
      window.addEventListener("message", receiveMessage, false);

      window.opener.postMessage("authorizing:github", "*");
    </script>
    """


if __name__ == "__main__":
    import uvicorn
    
    print("..:: Alwatr Decap CMS Backend ::..")
    print(f"Starting server on {HOST}:{PORT}")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )