"""Tenant registry for multi-tenant white-label platform."""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional, List
from contextvars import ContextVar

from .models import Tenant, Plan, TenantContext

# Global context for current tenant
_current_tenant: ContextVar[Optional[TenantContext]] = ContextVar("current_tenant", default=None)


class TenantRegistry:
    """Tenant registry with file-based provider."""
    
    def __init__(self, tenants_dir: str = "tenants", plans_dir: str = "plans"):
        self.tenants_dir = Path(tenants_dir)
        self.plans_dir = Path(plans_dir)
        self._tenants: Dict[str, Tenant] = {}
        self._plans: Dict[str, Plan] = {}
        self._load_plans()
        self._load_tenants()
    
    def _load_plans(self):
        """Load all plan configurations."""
        if not self.plans_dir.exists():
            return
        
        for plan_file in self.plans_dir.glob("*.yaml"):
            try:
                with open(plan_file, 'r') as f:
                    data = yaml.safe_load(f)
                    plan = Plan.from_dict(data)
                    self._plans[plan.plan_id] = plan
            except Exception as e:
                print(f"Warning: Failed to load plan {plan_file}: {e}")
    
    def _load_tenants(self):
        """Load all tenant configurations."""
        if not self.tenants_dir.exists():
            return
        
        for tenant_file in self.tenants_dir.glob("*.yaml"):
            try:
                with open(tenant_file, 'r') as f:
                    data = yaml.safe_load(f)
                    tenant = Tenant.from_dict(data)
                    self._tenants[tenant.tenant_id] = tenant
            except Exception as e:
                print(f"Warning: Failed to load tenant {tenant_file}: {e}")
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID."""
        return self._tenants.get(tenant_id)
    
    def get_plan(self, plan_id: str) -> Optional[Plan]:
        """Get plan by ID."""
        return self._plans.get(plan_id)
    
    def get_tenant_context(self, tenant_id: str) -> Optional[TenantContext]:
        """Get tenant context with plan."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return None
        
        plan = self.get_plan(tenant.plan)
        if not plan:
            print(f"Warning: Plan {tenant.plan} not found for tenant {tenant_id}")
            return None
        
        return TenantContext(tenant=tenant, plan=plan)
    
    def list_tenants(self) -> List[str]:
        """List all tenant IDs."""
        return list(self._tenants.keys())
    
    def list_plans(self) -> List[str]:
        """List all plan IDs."""
        return list(self._plans.keys())


class TenantResolver:
    """Resolve current tenant from various sources."""
    
    def __init__(self, registry: TenantRegistry):
        self.registry = registry
    
    def resolve_tenant(self, tenant_id: Optional[str] = None) -> Optional[TenantContext]:
        """Resolve tenant from various sources in order of precedence."""
        
        # 1. Explicit tenant ID parameter
        if tenant_id:
            return self.registry.get_tenant_context(tenant_id)
        
        # 2. Environment variable
        env_tenant = os.getenv("TENANT")
        if env_tenant:
            return self.registry.get_tenant_context(env_tenant)
        
        # 3. Default to first tenant if available
        tenants = self.registry.list_tenants()
        if tenants:
            return self.registry.get_tenant_context(tenants[0])
        
        return None


# Global registry instance
_registry = TenantRegistry()
_resolver = TenantResolver(_registry)


def current_tenant() -> Optional[TenantContext]:
    """Get current tenant context."""
    return _current_tenant.get()


def set_current_tenant(tenant_context: TenantContext):
    """Set current tenant context."""
    _current_tenant.set(tenant_context)


def get_tenant_context(tenant_id: Optional[str] = None) -> Optional[TenantContext]:
    """Get tenant context, resolving if needed."""
    if tenant_id:
        return _resolver.resolve_tenant(tenant_id)
    return current_tenant()


def get_feature_flags(tenant_id: Optional[str] = None) -> Optional[Dict[str, bool]]:
    """Get feature flags for tenant."""
    context = get_tenant_context(tenant_id)
    if not context:
        return None
    
    flags = context.get_feature_flags()
    return {field: getattr(flags, field) for field in flags.__dataclass_fields__}


def get_limits(tenant_id: Optional[str] = None) -> Optional[Dict[str, int]]:
    """Get limits for tenant."""
    context = get_tenant_context(tenant_id)
    if not context:
        return None
    
    limits = context.get_limits()
    return {field: getattr(limits, field) for field in limits.__dataclass_fields__}


def get_compliance(tenant_id: Optional[str] = None) -> Optional[Dict[str, bool]]:
    """Get compliance settings for tenant."""
    context = get_tenant_context(tenant_id)
    if not context:
        return None
    
    compliance = context.get_compliance()
    return {field: getattr(compliance, field) for field in compliance.__dataclass_fields__}
