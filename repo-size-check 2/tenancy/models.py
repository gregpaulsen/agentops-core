"""Tenancy models for multi-tenant white-label platform."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from enum import Enum


class PlanTier(Enum):
    """Plan tiers."""
    STARTER = "starter"
    CORPORATE = "corporate"


@dataclass
class FeatureFlags:
    """Feature flags configuration."""
    ENABLE_SSO: bool = False
    ENABLE_AUDIT_LOG: bool = True
    ENABLE_SCIM: bool = False
    ENABLE_DLP: bool = False
    ENABLE_RATE_LIMITS: bool = False
    ENABLE_DASHBOARDS_PRO: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureFlags":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class Limits:
    """Resource limits configuration."""
    MAX_USERS: int = 10
    MAX_STORAGE_GB: int = 50
    MAX_API_QPS: int = 50
    MAX_AI_TOKENS_PER_DAY: int = 100000
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Limits":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class Compliance:
    """Compliance configuration."""
    SOC2_MODE: bool = False
    PII_MASKING: bool = True
    DATA_RESIDENCY: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Compliance":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class Branding:
    """Branding configuration."""
    logo_url: str = ""
    primary_color: str = "#1A5D2E"
    secondary_color: str = "#FFD54F"
    email_sender: str = "no-reply@example.com"
    legal_footer: str = "© 2025 Example Corp. All rights reserved."
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Branding":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class Plan:
    """Plan configuration."""
    plan_id: str
    name: str
    feature_flags: FeatureFlags = field(default_factory=FeatureFlags)
    limits: Limits = field(default_factory=Limits)
    compliance: Compliance = field(default_factory=Compliance)
    defaults: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        """Create from dictionary."""
        return cls(
            plan_id=data["plan_id"],
            name=data["name"],
            feature_flags=FeatureFlags.from_dict(data.get("feature_flags", {})),
            limits=Limits.from_dict(data.get("limits", {})),
            compliance=Compliance.from_dict(data.get("compliance", {})),
            defaults=data.get("defaults", {})
        )


@dataclass
class Tenant:
    """Tenant configuration."""
    tenant_id: str
    name: str
    plan: str
    branding: Branding = field(default_factory=Branding)
    feature_flags: Dict[str, Any] = field(default_factory=dict)
    limits: Dict[str, Any] = field(default_factory=dict)
    storage: Dict[str, str] = field(default_factory=dict)
    ingest: Dict[str, str] = field(default_factory=dict)
    auth: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tenant":
        """Create from dictionary."""
        return cls(
            tenant_id=data["tenant_id"],
            name=data["name"],
            plan=data["plan"],
            branding=Branding.from_dict(data.get("branding", {})),
            feature_flags=data.get("feature_flags", {}),
            limits=data.get("limits", {}),
            storage=data.get("storage", {}),
            ingest=data.get("ingest", {}),
            auth=data.get("auth", {})
        )


@dataclass
class TenantContext:
    """Current tenant context."""
    tenant: Tenant
    plan: Plan
    config: Dict[str, Any] = field(default_factory=dict)
    
    def get_feature_flags(self) -> FeatureFlags:
        """Get effective feature flags (tenant overrides plan)."""
        plan_flags = self.plan.feature_flags
        tenant_flags = self.tenant.feature_flags
        
        # Merge tenant overrides with plan defaults
        effective_flags = {}
        for field in plan_flags.__dataclass_fields__:
            plan_value = getattr(plan_flags, field)
            tenant_value = tenant_flags.get(field, plan_value)
            effective_flags[field] = tenant_value
        
        return FeatureFlags(**effective_flags)
    
    def get_limits(self) -> Limits:
        """Get effective limits (tenant overrides plan)."""
        plan_limits = self.plan.limits
        tenant_limits = self.tenant.limits
        
        # Merge tenant overrides with plan defaults
        effective_limits = {}
        for field in plan_limits.__dataclass_fields__:
            plan_value = getattr(plan_limits, field)
            tenant_value = tenant_limits.get(field, plan_value)
            effective_limits[field] = tenant_value
        
        return Limits(**effective_limits)
    
    def get_compliance(self) -> Compliance:
        """Get compliance settings (inherited from plan)."""
        return self.plan.compliance
