# Authentication Guide

## Overview

PaulyOps supports provider-agnostic OIDC/OAuth2 authentication with normalized user mapping and JWT verification.

## Supported Providers

- **Google**: Google OAuth2
- **Okta**: Okta OIDC
- **Microsoft Entra**: Azure AD v2
- **Auth0**: Auth0 OIDC
- **Keycloak**: Keycloak OIDC
- **Ping**: PingOne OIDC
- **AWS Cognito**: Cognito OIDC

## Configuration

### Environment Variables

```bash
# Provider selection
AUTH_PROVIDER=google  # google|okta|entra|auth0|keycloak|ping|cognito

# OIDC configuration
OIDC_ISSUER_URL=https://accounts.google.com
OIDC_CLIENT_ID=your-client-id
OIDC_CLIENT_SECRET=your-client-secret
OIDC_AUDIENCE=api://default
OIDC_SCOPES=openid profile email offline_access

# Security settings
TOKEN_CLOCK_SKEW_SEC=60
AUTH_ROLE_GROUP_PREFIX=app_
```

### Tenant-Specific Auth

```yaml
# tenants/bigsky.yaml
auth:
  AUTH_PROVIDER: google
  OIDC_ISSUER_URL: https://accounts.google.com
  OIDC_CLIENT_ID: your-client-id
  OIDC_CLIENT_SECRET: your-client-secret
```

## Provider Setup

### Google OAuth2

1. Create OAuth2 credentials in Google Cloud Console
2. Set redirect URI: `https://your-domain/auth/callback`
3. Configure scopes: `openid profile email offline_access`

```bash
export AUTH_PROVIDER=google
export OIDC_ISSUER_URL=https://accounts.google.com
export OIDC_CLIENT_ID=your-client-id
export OIDC_CLIENT_SECRET=your-client-secret
```

### Okta OIDC

1. Create OIDC app in Okta Admin Console
2. Set redirect URI: `https://your-domain/auth/callback`
3. Configure scopes: `openid profile email offline_access`

```bash
export AUTH_PROVIDER=okta
export OIDC_ISSUER_URL=https://dev-XXXX.okta.com/oauth2/default
export OIDC_CLIENT_ID=your-client-id
export OIDC_CLIENT_SECRET=your-client-secret
```

### Microsoft Entra (Azure AD)

1. Register app in Azure AD
2. Set redirect URI: `https://your-domain/auth/callback`
3. Configure API permissions

```bash
export AUTH_PROVIDER=entra
export OIDC_ISSUER_URL=https://login.microsoftonline.com/<TENANT_ID>/v2.0
export OIDC_CLIENT_ID=your-client-id
export OIDC_CLIENT_SECRET=your-client-secret
```

## Security Best Practices

### PKCE (Proof Key for Code Exchange)

Always use PKCE for public clients:

```python
import secrets
import base64
import hashlib

# Generate code verifier
code_verifier = secrets.token_urlsafe(32)

# Generate code challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip('=')
```

### State and Nonce

Always include state and nonce parameters:

```python
import secrets

state = secrets.token_urlsafe(32)
nonce = secrets.token_urlsafe(32)
```

### Token Refresh

Implement automatic token refresh:

```python
async def refresh_token(refresh_token: str):
    provider = auth_config.create_provider()
    new_tokens = await provider.refresh(refresh_token)
    return new_tokens
```

## User Mapping

### Normalized Claims

All providers map to standard claims:

```python
@dataclass
class UserInfo:
    sub: str              # Subject (user ID)
    email: str            # Email address
    name: str             # Full name
    given_name: str       # First name
    family_name: str      # Last name
    groups: List[str]     # Group memberships
    roles: List[str]      # Role assignments
    picture: str          # Profile picture URL
    email_verified: bool  # Email verification status
```

### Group to Role Mapping

Map OIDC groups to RBAC roles:

```python
# Example: app_admin group → admin role
role_mapping = {
    "app_owner": Role.OWNER,
    "app_admin": Role.ADMIN,
    "app_editor": Role.EDITOR,
    "app_viewer": Role.VIEWER,
    "app_service": Role.SERVICE,
}
```

## JWT Verification

### Standard Verification

```python
async def verify_jwt(token: str):
    provider = auth_config.create_provider()
    claims = await provider.verify_jwt(token)
    return claims
```

### Custom Claims Validation

```python
async def verify_jwt_with_claims(token: str, required_claims: List[str]):
    claims = await verify_jwt(token)
    
    for claim in required_claims:
        if claim not in claims:
            raise ValueError(f"Missing required claim: {claim}")
    
    return claims
```

## FastAPI Integration

### Auth Middleware

```python
from fastapi import Depends, HTTPException
from auth.middleware import require_auth

@app.get("/protected")
async def protected_endpoint(user: UserInfo = Depends(require_auth)):
    return {"message": f"Hello {user.name}"}
```

### Role-Based Access

```python
@app.get("/admin")
async def admin_endpoint(user: UserInfo = Depends(require_auth(roles=["admin"]))):
    return {"message": "Admin access granted"}
```

## Error Handling

### Common Errors

- **Invalid Token**: Token expired or malformed
- **Missing Claims**: Required claims not present
- **Provider Error**: OIDC provider unavailable
- **Rate Limiting**: Too many requests

### Error Responses

```python
{
    "error": "invalid_token",
    "error_description": "Token expired",
    "status_code": 401
}
```

## Testing

### Unit Tests

```python
def test_google_provider():
    provider = GoogleProvider(client_id="test", client_secret="test")
    assert provider.auth_provider == "google"

def test_jwt_verification():
    # Test with mock JWT
    pass
```

### Integration Tests

```python
@pytest.mark.google
def test_google_auth_flow():
    # Test complete auth flow
    pass

@pytest.mark.okta
def test_okta_auth_flow():
    # Test Okta-specific flow
    pass
```

## Troubleshooting

### Common Issues

1. **Clock Skew**: Adjust `TOKEN_CLOCK_SKEW_SEC`
2. **Missing Scopes**: Verify `OIDC_SCOPES` configuration
3. **Invalid Audience**: Check `OIDC_AUDIENCE` setting
4. **Provider Discovery**: Verify `OIDC_ISSUER_URL`

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
```

### Health Check

Run auth health check:

```bash
python system_health.py
```
