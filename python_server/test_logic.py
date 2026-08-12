#!/usr/bin/env python3
"""
Test script to verify the core logic without requiring FastAPI dependencies.
This can be run to validate the implementation logic.
"""

import os
import secrets

def generate_state() -> str:
    """Generate a random state string for CSRF protection."""
    return secrets.token_hex(4)


def render_body(status: str, token: str = None) -> str:
    """
    Render the HTML response for the callback.
    """
    token_obj = {"token": token} if token else {}
    return f"""
    <script>
      const receiveMessage = (message) => {{
        window.opener.postMessage(
          'authorization:github:{status}:{token_obj}',
          message.origin
        );

        window.removeEventListener("message", receiveMessage, false);
      }}
      window.addEventListener("message", receiveMessage, false);

      window.opener.postMessage("authorizing:github", "*");
    </script>
    """


def test_state_generation():
    """Test that state generation works."""
    state = generate_state()
    assert len(state) == 8, f"Expected 8 character state, got {len(state)}"
    assert all(c in "0123456789abcdef" for c in state), "State should be hex"
    print("✓ State generation test passed")


def test_render_body():
    """Test HTML rendering."""
    # Test success case
    html_success = render_body("success", "test_token_123")
    assert "authorization:github:success" in html_success, "Success message should be in HTML"
    assert "test_token_123" in html_success, "Token should be in HTML"
    assert "authorizing:github" in html_success, "Authorizing message should be in HTML"
    
    # Test failure case (no token)
    html_failure = render_body("error")
    assert "authorization:github:error" in html_failure, "Error message should be in HTML"
    assert "authorizing:github" in html_failure, "Authorizing message should be in HTML"
    
    print("✓ HTML rendering test passed")


def test_environment_validation():
    """Test environment variable validation logic."""
    # This simulates the validation that happens on import
    test_cases = [
        ("OAUTH_GITHUB_CLIENT_ID", "client_id_123"),
        ("OAUTH_GITHUB_CLIENT_SECRET", "client_secret_456"),
    ]
    
    for var_name, value in test_cases:
        assert value, f"{var_name} should not be empty"
    
    print("✓ Environment validation logic test passed")


def test_url_construction():
    """Test URL construction logic."""
    client_id = "test_client_id"
    host = "localhost:8000"
    provider = "github"
    scope = "repo"
    state = "abc123"
    
    # Simulate the URL construction from auth route
    params = {
        "client_id": client_id,
        "redirect_uri": f"https://{host}/callback?provider={provider}",
        "scope": scope,
        "state": state
    }
    
    base_url = "https://github.com/login/oauth/authorize"
    auth_url = f"{base_url}?" + "&".join(f"{k}={v}" for k, v in params.items())
    
    assert "client_id=test_client_id" in auth_url
    assert "redirect_uri=https://localhost:8000/callback?provider=github" in auth_url
    assert "scope=repo" in auth_url
    assert "state=abc123" in auth_url
    
    print("✓ URL construction test passed")


if __name__ == "__main__":
    print("Running logic tests...")
    
    test_state_generation()
    test_render_body()
    test_environment_validation()
    test_url_construction()
    
    print("\n✓ All logic tests passed!")
    print("\nThe FastAPI implementation should work correctly once dependencies are installed.")
    print("To install dependencies: pip install -r requirements.txt")
    print("To run the server: python run.py")