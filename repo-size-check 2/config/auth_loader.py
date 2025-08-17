"""Auth configuration loader."""

import os
from typing import Optional, Dict, Any

from tenancy.registry import get_tenant_context


class AuthConfig:
    """Auth configuration manager."""
    
    def __init__(self, tenant_id: Optional[str] = None):
        self.tenant_id = tenant_id
        self.tenant_context = get_tenant_context(tenant_id)
        self._load_config()
    
    def _load_config(self):
        """Load auth configuration from environment and tenant."""
        # Environment variables (highest priority)
        self.auth_provider = os.getenv("AUTH_PROVIDER", "google")
        self.oidc_issuer_url = os.getenv("OIDC_ISSUER_URL", "")
        self.oidc_client_id = os.getenv("OIDC_CLIENT_ID", "")
        self.oidc_client_secret = os.getenv("OIDC_CLIENT_SECRET", "")
        self.oidc_audience = os.getenv("OIDC_AUDIENCE", "api://default")
        self.oidc_scopes = os.getenv("OIDC_SCOPES", "openid profile email offline_access")
        self.token_clock_skew_sec = int(os.getenv("TOKEN_CLOCK_SKEW_SEC", "60"))
        self.auth_role_group_prefix = os.getenv("AUTH_ROLE_GROUP_PREFIX", "app_")
        
        # Tenant overrides (if available)
        if self.tenant_context and self.tenant_context.tenant.auth:
            tenant_auth = self.tenant_context.tenant.auth
            self.auth_provider = tenant_auth.get("AUTH_PROVIDER", self.auth_provider)
            self.oidc_issuer_url = tenant_auth.get("OIDC_ISSUER_URL", self.oidc_issuer_url)
            self.oidc_client_id = tenant_auth.get("OIDC_CLIENT_ID", self.oidc_client_id)
            self.oidc_client_secret = tenant_auth.get("OIDC_CLIENT_SECRET", self.oidc_client_secret)
            self.oidc_audience = tenant_auth.get("OIDC_AUDIENCE", self.oidc_audience)
            self.oidc_scopes = tenant_auth.get("OIDC_SCOPES", self.oidc_scopes)
        
        # Plan defaults (if available)
        if self.tenant_context and self.tenant_context.plan.defaults:
            plan_defaults = self.tenant_context.plan.defaults
            if not self.oidc_scopes:
                self.oidc_scopes = plan_defaults.get("OIDC_SCOPES", self.oidc_scopes)
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get provider-specific configuration."""
        return {
            "provider": self.auth_provider,
            "client_id": self.oidc_client_id,
            "client_secret": self.oidc_client_secret,
            "issuer_url": self.oidc_issuer_url,
            "audience": self.oidc_audience,
            "scopes": self.oidc_scopes,
            "clock_skew_seconds": self.token_clock_skew_sec,
            "role_group_prefix": self.auth_role_group_prefix
        }
    
    def has_credentials(self) -> bool:
        """Check if auth credentials are configured."""
        return bool(self.oidc_client_id and self.oidc_client_secret and self.oidc_issuer_url)
    
    def get_provider_class(self):
        """Get the provider class based on configuration."""
        if self.auth_provider == "google":
            from auth.adapters.google import GoogleProvider
            return GoogleProvider
        else:
            raise ValueError(f"Unsupported auth provider: {self.auth_provider}")
    
    def create_provider(self):
        """Create provider instance."""
        provider_class = self.get_provider_class()
        return provider_class(
            client_id=self.oidc_client_id,
            client_secret=self.oidc_client_secret,
            audience=self.oidc_audience
        )
    
    def print_summary(self):
        """Print auth configuration summary."""
        print("=" * 60)
        print("AUTH CONFIGURATION SUMMARY")
        print("=" * 60)
        print(f"Tenant: {self.tenant_id or 'NOT SET'}")
        print(f"Provider: {self.auth_provider}")
        print(f"Issuer URL: {'***' if self.oidc_issuer_url else 'NOT SET'}")
        print(f"Client ID: {'***' if self.oidc_client_id else 'NOT SET'}")
        print(f"Client Secret: {'***' if self.oidc_client_secret else 'NOT SET'}")
        print(f"Audience: {self.oidc_audience}")
        print(f"Scopes: {self.oidc_scopes}")
        print(f"Clock Skew: {self.token_clock_skew_sec}s")
        print(f"Role Group Prefix: {self.auth_role_group_prefix}")
        print(f"Credentials Configured: {'✅' if self.has_credentials() else '❌'}")
        print("=" * 60)
