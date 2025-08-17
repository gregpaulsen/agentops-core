# Tenancy Guide

## Overview

PaulyOps is a multi-tenant white-label platform that supports different plan tiers and tenant-specific configurations.

## Tenant Structure

### Plans

Plans define the feature set, limits, and compliance requirements for tenants:

- **Starter (SMB)**: Basic features, limited resources, relaxed compliance
- **Corporate (Enterprise)**: Full features, high limits, strict compliance

### Tenants

Each tenant has:
- Unique tenant ID
- Plan assignment
- Branding configuration
- Feature flag overrides
- Storage configuration
- Auth provider settings

## Configuration Hierarchy

Configuration is loaded in this order (later overrides earlier):

1. **Global defaults** (`config/defaults.py`)
2. **Plan defaults** (`plans/*.yaml`)
3. **Tenant overrides** (`tenants/*.yaml`)
4. **Environment variables** (highest priority)

## Tenant Resolution

Tenants are resolved in this order:

1. **Explicit tenant ID** (CLI `--tenant` parameter)
2. **Environment variable** (`TENANT`)
3. **Default tenant** (first tenant in registry)

## Plan Configuration

### Starter Plan Features

```yaml
feature_flags:
  ENABLE_SSO: false
  ENABLE_AUDIT_LOG: true
  ENABLE_SCIM: false
  ENABLE_DLP: false
  ENABLE_RATE_LIMITS: false
  ENABLE_DASHBOARDS_PRO: false

limits:
  MAX_USERS: 10
  MAX_STORAGE_GB: 50
  MAX_API_QPS: 50
  MAX_AI_TOKENS_PER_DAY: 100000

compliance:
  SOC2_MODE: false
  PII_MASKING: true
  DATA_RESIDENCY: false
```

### Corporate Plan Features

```yaml
feature_flags:
  ENABLE_SSO: true
  ENABLE_AUDIT_LOG: true
  ENABLE_SCIM: true
  ENABLE_DLP: true
  ENABLE_RATE_LIMITS: true
  ENABLE_DASHBOARDS_PRO: true

limits:
  MAX_USERS: 10000
  MAX_STORAGE_GB: 10000
  MAX_API_QPS: 2000
  MAX_AI_TOKENS_PER_DAY: 5000000

compliance:
  SOC2_MODE: true
  PII_MASKING: true
  DATA_RESIDENCY: true
```

## Branding Configuration

Each tenant can customize:

```yaml
branding:
  logo_url: /assets/logos/company.png
  primary_color: "#1A5D2E"
  secondary_color: "#FFD54F"
  email_sender: no-reply@company.com
  legal_footer: "© 2025 Company LLC. All rights reserved."
```

## Usage Examples

### Get Current Tenant

```python
from tenancy.registry import current_tenant, get_tenant_context

# Get current tenant context
context = current_tenant()

# Get specific tenant
context = get_tenant_context("bigsky")
```

### Get Feature Flags

```python
from tenancy.registry import get_feature_flags

flags = get_feature_flags("bigsky")
if flags["ENABLE_SSO"]:
    # Enable SSO features
    pass
```

### Get Limits

```python
from tenancy.registry import get_limits

limits = get_limits("bigsky")
max_users = limits["MAX_USERS"]
```

## CLI Usage

```bash
# Run with specific tenant
python system_function_check.py --tenant bigsky

# Set tenant via environment
export TENANT=bigsky
python system_health.py
```

## Adding New Tenants

1. Create tenant file in `tenants/`:
   ```yaml
   tenant_id: newcompany
   name: New Company
   plan: starter
   branding:
     logo_url: /assets/logos/newcompany.png
     primary_color: "#FF0000"
   ```

2. Configure storage and auth settings
3. Test with `--tenant newcompany`

## Adding New Plans

1. Create plan file in `plans/`:
   ```yaml
   plan_id: premium
   name: Premium
   feature_flags:
     ENABLE_SSO: true
   limits:
     MAX_USERS: 100
   ```

2. Update tenant to use new plan
3. Test configuration loading
