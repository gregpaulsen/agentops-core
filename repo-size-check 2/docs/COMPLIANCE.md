# Compliance Guide

## Overview

PaulyOps supports configurable compliance modes for SOC2, PII masking, and data residency requirements.

## Compliance Modes

### SOC2 Mode

Enables SOC2 compliance requirements:

- **Secret Scanning**: Automatic detection of secrets in content
- **Coverage Threshold**: Minimum 30% test coverage requirement
- **Log Retention**: 90-day log retention period

```yaml
compliance:
  SOC2_MODE: true
```

### PII Masking

Masks personally identifiable information in logs:

- **Email Addresses**: `user@example.com` → `u***@example.com`
- **Phone Numbers**: `555-123-4567` → `***-***-****`
- **SSNs**: `123-45-6789` → `***-**-****`
- **Credit Cards**: `1234-5678-9012-3456` → `****-****-****-****`

```yaml
compliance:
  PII_MASKING: true
```

### Data Residency

Enforces data residency requirements:

- **Allowed Regions**: Restricts data to specific regions
- **Cross-Region Blocking**: Prevents data movement across regions
- **Region Validation**: Validates storage locations

```yaml
compliance:
  DATA_RESIDENCY: true
```

## Plan-Based Compliance

### Starter Plan (SMB)

```yaml
compliance:
  SOC2_MODE: false      # No SOC2 requirements
  PII_MASKING: true     # Basic PII protection
  DATA_RESIDENCY: false # No residency restrictions
```

### Corporate Plan (Enterprise)

```yaml
compliance:
  SOC2_MODE: true       # Full SOC2 compliance
  PII_MASKING: true     # Enhanced PII protection
  DATA_RESIDENCY: true  # Strict residency controls
```

## Usage Examples

### Compliance Manager

```python
from compliance.modes import ComplianceManager

# Initialize with tenant
manager = ComplianceManager("bigsky")

# Check SOC2 requirements
if manager.soc2.enabled:
    requires_scan = manager.soc2.require_secret_scan(content)
    coverage_ok = manager.soc2.check_coverage(covered_lines, total_lines)

# Mask PII in logs
masked_content = manager.pii_masking.mask_pii(log_content, privileged_role=False)

# Validate data residency
region_ok = manager.data_residency.check_region_compliance("us-east-1")
```

### Secret Scanning

```python
# Check if content requires secret scanning
if manager.soc2.require_secret_scan(content):
    # Perform secret scan
    secrets_found = scan_for_secrets(content)
    if secrets_found:
        raise SecurityException("Secrets detected in content")
```

### PII Detection

```python
# Check if content contains PII
if manager.pii_masking.has_pii(content):
    # Mask PII before logging
    masked_content = manager.pii_masking.mask_pii(content)
    logger.info(masked_content)
```

## Configuration

### Environment Variables

```bash
# Compliance settings
SOC2_MODE=false
PII_MASKING=true
DATA_RESIDENCY=false

# SOC2 settings
SOC2_COVERAGE_THRESHOLD=0.30
SOC2_LOG_RETENTION_DAYS=90

# Data residency settings
ALLOWED_REGIONS=us-east-1,us-west-2
```

### Tenant Overrides

```yaml
# tenants/enterprise.yaml
compliance:
  SOC2_MODE: true
  PII_MASKING: true
  DATA_RESIDENCY: true
```

## Testing

### Unit Tests

```python
def test_soc2_compliance():
    manager = ComplianceManager("corporate")
    assert manager.soc2.enabled == True
    assert manager.soc2.coverage_threshold == 0.30

def test_pii_masking():
    manager = ComplianceManager("starter")
    masked = manager.pii_masking.mask_pii("user@example.com")
    assert "***" in masked
```

### Integration Tests

```python
@pytest.mark.compliance
def test_compliance_workflow():
    # Test complete compliance workflow
    pass
```

## Monitoring

### Compliance Reports

Generate compliance reports:

```bash
python system_health.py
```

### Audit Logs

Compliance events are logged:

```json
{
  "timestamp": "2024-12-12T10:00:00Z",
  "event": "compliance_check",
  "tenant": "bigsky",
  "mode": "SOC2",
  "result": "pass"
}
```

## Troubleshooting

### Common Issues

1. **False Positives**: Adjust secret scanning patterns
2. **Coverage Failures**: Increase test coverage
3. **Region Violations**: Check allowed regions configuration
4. **PII Detection**: Verify PII patterns

### Debug Mode

Enable compliance debugging:

```bash
export LOG_LEVEL=DEBUG
```
