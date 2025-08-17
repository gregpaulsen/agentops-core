"""RBAC models for multi-tenant platform."""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from enum import Enum
import secrets
import time


class Role(Enum):
    """User roles."""
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    SERVICE = "service"


class Permission(Enum):
    """Permissions."""
    # User management
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    
    # Configuration
    MANAGE_CONFIG = "manage_config"
    VIEW_CONFIG = "view_config"
    
    # Storage
    MANAGE_STORAGE = "manage_storage"
    VIEW_STORAGE = "view_storage"
    UPLOAD_FILES = "upload_files"
    DOWNLOAD_FILES = "download_files"
    
    # Backups
    MANAGE_BACKUPS = "manage_backups"
    VIEW_BACKUPS = "view_backups"
    RESTORE_BACKUPS = "restore_backups"
    
    # API
    MANAGE_API_KEYS = "manage_api_keys"
    USE_API = "use_api"
    
    # Compliance
    VIEW_AUDIT_LOGS = "view_audit_logs"
    MANAGE_COMPLIANCE = "manage_compliance"


@dataclass
class RolePermissions:
    """Role permissions mapping."""
    role: Role
    permissions: Set[Permission] = field(default_factory=set)
    
    @classmethod
    def get_default_permissions(cls) -> Dict[Role, Set[Permission]]:
        """Get default role permissions."""
        return {
            Role.OWNER: {
                Permission.MANAGE_USERS, Permission.VIEW_USERS,
                Permission.MANAGE_CONFIG, Permission.VIEW_CONFIG,
                Permission.MANAGE_STORAGE, Permission.VIEW_STORAGE,
                Permission.UPLOAD_FILES, Permission.DOWNLOAD_FILES,
                Permission.MANAGE_BACKUPS, Permission.VIEW_BACKUPS,
                Permission.RESTORE_BACKUPS, Permission.MANAGE_API_KEYS,
                Permission.USE_API, Permission.VIEW_AUDIT_LOGS,
                Permission.MANAGE_COMPLIANCE
            },
            Role.ADMIN: {
                Permission.MANAGE_USERS, Permission.VIEW_USERS,
                Permission.MANAGE_CONFIG, Permission.VIEW_CONFIG,
                Permission.MANAGE_STORAGE, Permission.VIEW_STORAGE,
                Permission.UPLOAD_FILES, Permission.DOWNLOAD_FILES,
                Permission.MANAGE_BACKUPS, Permission.VIEW_BACKUPS,
                Permission.RESTORE_BACKUPS, Permission.MANAGE_API_KEYS,
                Permission.USE_API, Permission.VIEW_AUDIT_LOGS
            },
            Role.EDITOR: {
                Permission.VIEW_USERS, Permission.VIEW_CONFIG,
                Permission.VIEW_STORAGE, Permission.UPLOAD_FILES,
                Permission.DOWNLOAD_FILES, Permission.VIEW_BACKUPS,
                Permission.USE_API
            },
            Role.VIEWER: {
                Permission.VIEW_USERS, Permission.VIEW_CONFIG,
                Permission.VIEW_STORAGE, Permission.DOWNLOAD_FILES,
                Permission.VIEW_BACKUPS, Permission.USE_API
            },
            Role.SERVICE: {
                Permission.VIEW_CONFIG, Permission.VIEW_STORAGE,
                Permission.UPLOAD_FILES, Permission.DOWNLOAD_FILES,
                Permission.VIEW_BACKUPS, Permission.USE_API
            }
        }


@dataclass
class User:
    """User model."""
    user_id: str
    email: str
    name: str
    roles: List[Role] = field(default_factory=list)
    groups: List[str] = field(default_factory=list)
    tenant_id: str = ""
    is_active: bool = True
    created_at: float = field(default_factory=time.time)
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has permission."""
        default_permissions = RolePermissions.get_default_permissions()
        
        for role in self.roles:
            if permission in default_permissions.get(role, set()):
                return True
        
        return False
    
    def has_role(self, role: Role) -> bool:
        """Check if user has role."""
        return role in self.roles


@dataclass
class APIKey:
    """API key model."""
    key_id: str
    name: str
    tenant_id: str
    user_id: str
    scopes: List[str] = field(default_factory=list)
    rate_limit_qps: int = 100
    is_active: bool = True
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    
    def is_expired(self) -> bool:
        """Check if API key is expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def can_access_scope(self, scope: str) -> bool:
        """Check if API key can access scope."""
        return scope in self.scopes or "*" in self.scopes


class RBACManager:
    """RBAC manager for tenant."""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, APIKey] = {}
    
    def add_user(self, user: User) -> None:
        """Add user to tenant."""
        user.tenant_id = self.tenant_id
        self.users[user.user_id] = user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def map_oidc_groups_to_roles(self, groups: List[str], prefix: str = "app_") -> List[Role]:
        """Map OIDC groups to roles."""
        role_mapping = {
            f"{prefix}owner": Role.OWNER,
            f"{prefix}admin": Role.ADMIN,
            f"{prefix}editor": Role.EDITOR,
            f"{prefix}viewer": Role.VIEWER,
            f"{prefix}service": Role.SERVICE,
        }
        
        roles = []
        for group in groups:
            if group in role_mapping:
                roles.append(role_mapping[group])
        
        return roles
    
    def create_api_key(self, name: str, user_id: str, scopes: List[str] = None, 
                      rate_limit_qps: int = 100, expires_in_days: Optional[int] = None) -> APIKey:
        """Create API key for user."""
        key_id = secrets.token_urlsafe(32)
        expires_at = None
        if expires_in_days:
            expires_at = time.time() + (expires_in_days * 24 * 3600)
        
        api_key = APIKey(
            key_id=key_id,
            name=name,
            tenant_id=self.tenant_id,
            user_id=user_id,
            scopes=scopes or ["*"],
            rate_limit_qps=rate_limit_qps,
            expires_at=expires_at
        )
        
        self.api_keys[key_id] = api_key
        return api_key
    
    def validate_api_key(self, key_id: str, scope: str = None) -> Optional[APIKey]:
        """Validate API key."""
        api_key = self.api_keys.get(key_id)
        if not api_key or not api_key.is_active or api_key.is_expired():
            return None
        
        if scope and not api_key.can_access_scope(scope):
            return None
        
        return api_key
    
    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get user permissions."""
        user = self.get_user(user_id)
        if not user:
            return set()
        
        default_permissions = RolePermissions.get_default_permissions()
        permissions = set()
        
        for role in user.roles:
            permissions.update(default_permissions.get(role, set()))
        
        return permissions
