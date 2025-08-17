"""Auth models for OIDC/OAuth2 integration."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


@dataclass
class UserInfo:
    """Normalized user information."""
    sub: str
    email: str
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    groups: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    picture: Optional[str] = None
    email_verified: bool = False
    locale: Optional[str] = None
    zoneinfo: Optional[str] = None
    
    @classmethod
    def from_claims(cls, claims: Dict[str, Any]) -> "UserInfo":
        """Create UserInfo from OIDC claims."""
        return cls(
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


@dataclass
class TokenSet:
    """OAuth2 token set."""
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Set expires_at if expires_in is provided."""
        if self.expires_in and not self.expires_at:
            self.expires_at = datetime.now() + timedelta(seconds=self.expires_in)
    
    def is_expired(self, clock_skew_seconds: int = 60) -> bool:
        """Check if token is expired."""
        if not self.expires_at:
            return False
        
        return datetime.now() > (self.expires_at - timedelta(seconds=clock_skew_seconds))
    
    def needs_refresh(self, refresh_threshold_seconds: int = 300) -> bool:
        """Check if token needs refresh."""
        if not self.expires_at:
            return False
        
        return datetime.now() > (self.expires_at - timedelta(seconds=refresh_threshold_seconds))


@dataclass
class ClaimsMap:
    """Normalized claims mapping."""
    sub: str = ""
    email: str = ""
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    groups: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    picture: str = ""
    email_verified: bool = False
    locale: str = ""
    zoneinfo: str = ""
    
    @classmethod
    def get_standard_mapping(cls) -> Dict[str, str]:
        """Get standard OIDC claim mappings."""
        return {
            "sub": "sub",
            "email": "email",
            "name": "name",
            "given_name": "given_name",
            "family_name": "family_name",
            "picture": "picture",
            "email_verified": "email_verified",
            "locale": "locale",
            "zoneinfo": "zoneinfo"
        }
    
    def map_claims(self, raw_claims: Dict[str, Any], custom_mapping: Dict[str, str] = None) -> Dict[str, Any]:
        """Map raw claims to normalized format."""
        mapping = {**self.get_standard_mapping(), **(custom_mapping or {})}
        
        normalized_claims = {}
        for standard_key, raw_key in mapping.items():
            if raw_key in raw_claims:
                normalized_claims[standard_key] = raw_claims[raw_key]
        
        # Handle groups/roles mapping
        if "groups" in raw_claims:
            normalized_claims["groups"] = raw_claims["groups"]
        elif "roles" in raw_claims:
            normalized_claims["groups"] = raw_claims["roles"]
        
        return normalized_claims


@dataclass
class OIDCDiscovery:
    """OIDC discovery document."""
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: Optional[str] = None
    jwks_uri: str
    end_session_endpoint: Optional[str] = None
    scopes_supported: List[str] = field(default_factory=list)
    claims_supported: List[str] = field(default_factory=list)
    response_types_supported: List[str] = field(default_factory=list)
    grant_types_supported: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OIDCDiscovery":
        """Create from discovery document."""
        return cls(
            issuer=data.get("issuer", ""),
            authorization_endpoint=data.get("authorization_endpoint", ""),
            token_endpoint=data.get("token_endpoint", ""),
            userinfo_endpoint=data.get("userinfo_endpoint"),
            jwks_uri=data.get("jwks_uri", ""),
            end_session_endpoint=data.get("end_session_endpoint"),
            scopes_supported=data.get("scopes_supported", []),
            claims_supported=data.get("claims_supported", []),
            response_types_supported=data.get("response_types_supported", []),
            grant_types_supported=data.get("grant_types_supported", [])
        )


@dataclass
class JWK:
    """JSON Web Key."""
    kid: str
    kty: str
    use: str
    alg: str
    n: Optional[str] = None
    e: Optional[str] = None
    x5c: Optional[List[str]] = None
    x5t: Optional[str] = None
    x5t_256: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JWK":
        """Create from JWK dictionary."""
        return cls(
            kid=data.get("kid", ""),
            kty=data.get("kty", ""),
            use=data.get("use", ""),
            alg=data.get("alg", ""),
            n=data.get("n"),
            e=data.get("e"),
            x5c=data.get("x5c"),
            x5t=data.get("x5t"),
            x5t_256=data.get("x5t#S256")
        )


@dataclass
class JWKSet:
    """JSON Web Key Set."""
    keys: List[JWK] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JWKSet":
        """Create from JWKS dictionary."""
        keys = [JWK.from_dict(key_data) for key_data in data.get("keys", [])]
        return cls(keys=keys)
    
    def get_key(self, kid: str) -> Optional[JWK]:
        """Get key by key ID."""
        for key in self.keys:
            if key.kid == kid:
                return key
        return None
