"""Base provider interface for OIDC/OAuth2."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode, urljoin

from .models import UserInfo, TokenSet, OIDCDiscovery, JWKSet


class ProviderInterface(ABC):
    """Base interface for OIDC/OAuth2 providers."""
    
    def __init__(self, client_id: str, client_secret: str, issuer_url: str, 
                 audience: str = "api://default", scopes: str = "openid profile email offline_access"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer_url = issuer_url.rstrip('/')
        self.audience = audience
        self.scopes = scopes
        self.discovery: Optional[OIDCDiscovery] = None
        self.jwks: Optional[JWKSet] = None
    
    @abstractmethod
    async def discovery(self) -> OIDCDiscovery:
        """Get OIDC discovery document."""
        pass
    
    @abstractmethod
    def auth_url(self, redirect_uri: str, state: str, nonce: str, 
                 response_type: str = "code") -> str:
        """Generate authorization URL."""
        pass
    
    @abstractmethod
    async def exchange_code(self, code: str, redirect_uri: str, 
                           code_verifier: Optional[str] = None) -> TokenSet:
        """Exchange authorization code for tokens."""
        pass
    
    @abstractmethod
    async def refresh(self, refresh_token: str) -> TokenSet:
        """Refresh access token."""
        pass
    
    @abstractmethod
    async def client_credentials(self) -> TokenSet:
        """Get client credentials token."""
        pass
    
    @abstractmethod
    async def verify_jwt(self, token: str, clock_skew_seconds: int = 60) -> Dict[str, Any]:
        """Verify JWT token."""
        pass
    
    @abstractmethod
    async def map_userinfo(self, claims: Dict[str, Any]) -> UserInfo:
        """Map claims to normalized UserInfo."""
        pass
    
    def _build_auth_url(self, discovery: OIDCDiscovery, redirect_uri: str, 
                       state: str, nonce: str, response_type: str = "code") -> str:
        """Build authorization URL with standard parameters."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": response_type,
            "scope": self.scopes,
            "state": state,
            "nonce": nonce
        }
        
        # Add PKCE if supported
        if "code_challenge_methods_supported" in discovery.__dict__:
            if "S256" in discovery.code_challenge_methods_supported:
                params["code_challenge_method"] = "S256"
                # Note: code_challenge should be set by caller
        
        query_string = urlencode(params)
        return f"{discovery.authorization_endpoint}?{query_string}"
    
    def _get_discovery_url(self) -> str:
        """Get discovery document URL."""
        return f"{self.issuer_url}/.well-known/openid_configuration"
    
    def _get_jwks_url(self, discovery: OIDCDiscovery) -> str:
        """Get JWKS URL from discovery document."""
        return discovery.jwks_uri
    
    async def _fetch_discovery(self) -> OIDCDiscovery:
        """Fetch discovery document."""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self._get_discovery_url()) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch discovery document: {response.status}")
                
                data = await response.json()
                return OIDCDiscovery.from_dict(data)
    
    async def _fetch_jwks(self, discovery: OIDCDiscovery) -> JWKSet:
        """Fetch JWKS."""
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self._get_jwks_url(discovery)) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch JWKS: {response.status}")
                
                data = await response.json()
                return JWKSet.from_dict(data)
    
    async def _ensure_discovery(self) -> OIDCDiscovery:
        """Ensure discovery document is loaded."""
        if not self.discovery:
            self.discovery = await self._fetch_discovery()
        return self.discovery
    
    async def _ensure_jwks(self) -> JWKSet:
        """Ensure JWKS is loaded."""
        if not self.jwks:
            discovery = await self._ensure_discovery()
            self.jwks = await self._fetch_jwks(discovery)
        return self.jwks
