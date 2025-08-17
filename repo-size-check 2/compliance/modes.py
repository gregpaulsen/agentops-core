"""Compliance modes for multi-tenant platform."""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from tenancy.registry import get_compliance


@dataclass
class ComplianceConfig:
    """Compliance configuration."""
    SOC2_MODE: bool = False
    PII_MASKING: bool = True
    DATA_RESIDENCY: bool = False


class SOC2Compliance:
    """SOC2 compliance mode."""
    
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.coverage_threshold = 0.30  # 30% minimum coverage
        self.log_retention_days = 90
    
    def require_secret_scan(self, content: str) -> bool:
        """Require secret scanning if SOC2 mode enabled."""
        if not self.enabled:
            return False
        
        # Basic secret patterns
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def check_coverage(self, covered_lines: int, total_lines: int) -> bool:
        """Check if test coverage meets SOC2 threshold."""
        if not self.enabled:
            return True
        
        if total_lines == 0:
            return True
        
        coverage = covered_lines / total_lines
        return coverage >= self.coverage_threshold
    
    def get_log_retention_days(self) -> int:
        """Get log retention period for SOC2."""
        return self.log_retention_days if self.enabled else 30


class PIIMasking:
    """PII masking compliance."""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        
        # PII patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
        }
    
    def mask_pii(self, text: str, privileged_role: bool = False) -> str:
        """Mask PII in text unless privileged role."""
        if not self.enabled or privileged_role:
            return text
        
        masked_text = text
        
        for pii_type, pattern in self.pii_patterns.items():
            if pii_type == 'email':
                masked_text = re.sub(pattern, self._mask_email, masked_text)
            elif pii_type == 'phone':
                masked_text = re.sub(pattern, '***-***-****', masked_text)
            elif pii_type == 'ssn':
                masked_text = re.sub(pattern, '***-**-****', masked_text)
            elif pii_type == 'credit_card':
                masked_text = re.sub(pattern, '****-****-****-****', masked_text)
        
        return masked_text
    
    def _mask_email(self, match) -> str:
        """Mask email address."""
        email = match.group(0)
        if '@' in email:
            username, domain = email.split('@', 1)
            if len(username) <= 2:
                masked_username = username
            else:
                masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
            return f"{masked_username}@{domain}"
        return email
    
    def has_pii(self, text: str) -> bool:
        """Check if text contains PII."""
        for pattern in self.pii_patterns.values():
            if re.search(pattern, text):
                return True
        return False


class DataResidency:
    """Data residency compliance."""
    
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.allowed_regions = ['us-east-1', 'us-west-2']  # Default US regions
    
    def check_region_compliance(self, region: str) -> bool:
        """Check if region is compliant with data residency requirements."""
        if not self.enabled:
            return True
        
        return region in self.allowed_regions
    
    def block_cross_region_move(self, source_region: str, target_region: str) -> bool:
        """Block cross-region data moves if data residency enabled."""
        if not self.enabled:
            return False
        
        return source_region != target_region
    
    def get_allowed_regions(self) -> List[str]:
        """Get list of allowed regions."""
        return self.allowed_regions.copy()


class ComplianceManager:
    """Main compliance manager."""
    
    def __init__(self, tenant_id: Optional[str] = None):
        compliance_config = get_compliance(tenant_id) or {}
        
        self.soc2 = SOC2Compliance(enabled=compliance_config.get('SOC2_MODE', False))
        self.pii_masking = PIIMasking(enabled=compliance_config.get('PII_MASKING', True))
        self.data_residency = DataResidency(enabled=compliance_config.get('DATA_RESIDENCY', False))
    
    def mask_log_content(self, content: str, privileged_role: bool = False) -> str:
        """Mask PII in log content."""
        return self.pii_masking.mask_pii(content, privileged_role)
    
    def check_secret_scan(self, content: str) -> bool:
        """Check if content requires secret scanning."""
        return self.soc2.require_secret_scan(content)
    
    def validate_region(self, region: str) -> bool:
        """Validate region for data residency."""
        return self.data_residency.check_region_compliance(region)
    
    def get_log_retention_days(self) -> int:
        """Get log retention period."""
        return self.soc2.get_log_retention_days()
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get compliance configuration summary."""
        return {
            'SOC2_MODE': self.soc2.enabled,
            'PII_MASKING': self.pii_masking.enabled,
            'DATA_RESIDENCY': self.data_residency.enabled,
            'log_retention_days': self.get_log_retention_days(),
            'allowed_regions': self.data_residency.get_allowed_regions()
        }
