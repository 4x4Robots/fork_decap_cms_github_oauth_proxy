# Decap CMS GitHub OAuth Proxy - Python FastAPI Implementation

This is a Python FastAPI reimplementation of the original TypeScript/Node.js Decap CMS GitHub OAuth Proxy server. It provides the same OAuth2 proxy functionality for GitHub authentication, allowing a Decap CMS frontend to authenticate users via GitHub.

## Features

- **Lightweight**: Built with FastAPI for high performance
- **Standalone**: Single file implementation with no complex dependencies
- **Compatible**: Provides identical API endpoints and behavior to the original
- **Easy to deploy**: Simple configuration via environment variables

## Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Health check and service information |
| GET | `/auth?provider=github` | Initiate GitHub OAuth flow |
| GET | `/callback?provider=github&code=...` | Handle GitHub OAuth callback |

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or copy this directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your GitHub OAuth credentials
   nano .env
   ```

4. **Set up GitHub OAuth App**
   - Go to [GitHub Developer Settings](https://github.com/settings/developers)
   - Create a new OAuth App
   - Set the **Authorization callback URL** to: `https://your-domain.com/callback?provider=github`
   - Copy the **Client ID** and **Client Secret** to your `.env` file

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OAUTH_GITHUB_CLIENT_ID` | ✅ Yes | - | GitHub OAuth App Client ID |
| `OAUTH_GITHUB_CLIENT_SECRET` | ✅ Yes | - | GitHub OAuth App Client Secret |
| `OAUTH_GITHUB_SCOPE` | ❌ No | `repo` | OAuth scope for GitHub API access |
| `HOST` | ❌ No | `0.0.0.0` | Server host address |
| `PORT` | ❌ No | `8000` | Server port |

### Example `.env` file

```env
OAUTH_GITHUB_CLIENT_ID=your_github_client_id_here
OAUTH_GITHUB_CLIENT_SECRET=your_github_client_secret_here
OAUTH_GITHUB_SCOPE=repo,read:user
HOST=0.0.0.0
PORT=8000
```

## Usage

### Using uv (Recommended)

```bash
# Install dependencies with uv
uv pip install -r requirements.txt

# Run with auto-reload
uv run python run.py

# Or run directly
uv run python -m main
```

### Using pip

```bash
# Install dependencies with pip
pip install -r requirements.txt

# Run with auto-reload
python run.py

# Run without auto-reload
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build the image
docker build -t decap-cms-oauth-proxy .

# Run the container
docker run -p 8000:8000 \
  -e OAUTH_GITHUB_CLIENT_ID=your_client_id \
  -e OAUTH_GITHUB_CLIENT_SECRET=your_client_secret \
  -e OAUTH_GITHUB_SCOPE=repo \
  decap-cms-oauth-proxy
```

## API Documentation

Once running, you can access interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## OAuth Flow

### 1. Initiate Authentication

```
GET /auth?provider=github
```

This will redirect the user to GitHub's authorization page with the appropriate parameters.

### 2. Handle Callback

After the user authorizes the application on GitHub, they will be redirected to:

```
GET /callback?provider=github&code=AUTHORIZATION_CODE
```

The server will exchange the authorization code for an access token and return an HTML page that uses `window.postMessage` to send the token back to the opener window.

### 3. Frontend Integration

The frontend should:

1. Open a popup window to `/auth?provider=github`
2. Listen for `message` events
3. Handle the `authorization:github:success:{token}` message
4. Handle the `authorization:github:error:{error}` message

## Comparison with Original TypeScript Version

| Feature | TypeScript | Python FastAPI |
|---------|------------|----------------|
| Framework | @alwatr/nanotron | FastAPI |
| OAuth Library | simple-oauth2 | requests |
| State Generation | crypto.randomBytes | secrets.token_hex |
| HTML Response | Custom | FastAPI HTMLResponse |
| Configuration | Environment variables | Environment variables |
| Routes | 3 routes | 3 identical routes |
| Behavior | Identical | Identical |

## Error Handling

The server returns appropriate HTTP status codes and JSON error responses:

- **400 Bad Request**: Invalid provider or missing code parameter
- **400 Bad Request**: Token exchange failure
- **301 Moved Permanently**: Redirect to GitHub authorization

## Security Considerations

- **State Parameter**: Random state is generated for each authorization request
- **HTTPS**: Should be used in production for secure token transmission
- **Environment Variables**: Never commit `.env` files to version control
- **CORS**: The frontend should be configured to handle cross-origin messaging securely

## Testing

```bash
# Run logic tests (no dependencies required)
python test_logic.py

# Run with test server (requires dependencies)
python -c "
import sys
sys.path.insert(0, '.')
from main import app
print('Routes:', [route.path for route in app.routes])
"
```

## License

MIT License - same as the original project.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

This implementation maintains full compatibility with the original TypeScript version while providing a lightweight Python alternative.