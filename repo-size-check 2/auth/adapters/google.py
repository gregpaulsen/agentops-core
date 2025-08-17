"""Google OAuth2 adapter."""

import base64
import hashlib
import secrets
from typing import Dict, Any, Optional
from urllib.parse import urlencode

from ..base import ProviderInterface
from ..models import UserInfo, TokenSet, OIDCDiscovery


class GoogleProvider(ProviderInterface):
    """Google OAuth2 provider."""
    
    def __init__(self, client_id: str, client_secret: str, 
                 audience: str = "api://default"):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            issuer_url="https://accounts.google.com",
            audience=audience,
            scopes="openid profile email offline_access"
        )
    
    async def discovery(self) -> OIDCDiscovery:
        """Get Google OIDC discovery document."""
        return await self._ensure_discovery()
    
    def auth_url(self, redirect_uri: str, state: str, nonce: str, 
                 response_type: str = "code") -> str:
        """Generate Google authorization URL."""
        discovery = self.discovery or OIDCDiscovery(
            issuer=self.issuer_url,
            authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
            token_endpoint="https://oauth2.googleapis.com/token",
            jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
        )
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": self.scopes,
            "state": state,
            "nonce": nonce,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = urlencode(params)
        return f"{discovery.authorization_endpoint}?{query_string}"
    
    async def exchange_code(self, code: str, redirect_uri: str, 
                           code_verifier: Optional[str] = None) -> TokenSet:
        """Exchange authorization code for tokens."""
        import aiohttp
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        
        if code_verifier:
            data["code_verifier"] = code_verifier
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://oauth2.googleapis.com/token", data=data) as response:
                if response.status != 200:
                    raise Exception(f"Token exchange failed: {response.status}")
                
                token_data = await response.json()
                return TokenSet(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in"),
                    refresh_token=token_data.get("refresh_token"),
                    id_token=token_data.get("id_token"),
                    scope=token_data.get("scope")
                )
    
    async def refresh(self, refresh_token: str) -> TokenSet:
        """Refresh access token."""
        import aiohttp
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://oauth2.googleapis.com/token", data=data) as response:
                if response.status != 200:
                    raise Exception(f"Token refresh failed: {response.status}")
                
                token_data = await response.json()
                return TokenSet(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in"),
                    scope=token_data.get("scope")
                )
    
    async def client_credentials(self) -> TokenSet:
        """Get client credentials token."""
        import aiohttp
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": self.scopes
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://oauth2.googleapis.com/token", data=data) as response:
                if response.status != 200:
                    raise Exception(f"Client credentials failed: {response.status}")
                
                token_data = await response.json()
                return TokenSet(
                    access_token=token_data["access_token"],
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_in=token_data.get("expires_in"),
                    scope=token_data.get("scope")
                )
    
    async def verify_jwt(self, token: str, clock_skew_seconds: int = 60) -> Dict[str, Any]:
        """Verify JWT token."""
        import jwt
        from jwt import PyJWKClient
        
        # For Google, we can use the public JWKS
        jwks_client = PyJWKClient("https://www.googleapis.com/oauth2/v3/certs")
        
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer_url,
                options={"verify_signature": True}
            )
            return payload
        except Exception as e:
            raise Exception(f"JWT verification failed: {e}")
    
    async def map_userinfo(self, claims: Dict[str, Any]) -> UserInfo:
        """Map Google claims to normalized UserInfo."""
        return UserInfo(
            sub=claims.get("sub", ""),
            email=claims.get("email", ""),
            name=claims.get("name", ""),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            groups=claims.get("groups", []),
            roles=claims.get("roles", []),
            picture=claims.get("picture"),
            email_verified=claims.get("email_verified", False),
            locale=claims.get("locale"),
            zoneinfo=claims.get("zoneinfo")
        )
