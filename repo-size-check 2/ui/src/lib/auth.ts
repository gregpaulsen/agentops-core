import { useState, useEffect } from 'react';
import { api } from './api';
import { UserInfoSchema, type UserInfo } from './schemas';

export interface AuthState {
  user: UserInfo | null;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

export interface AuthActions {
  login: (provider?: string) => void;
  logout: () => void;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

export type UseAuthReturn = AuthState & AuthActions;

// Mock user for development
const MOCK_USER: UserInfo = {
  sub: 'user_123',
  email: 'user@bigskyag.farm',
  name: 'Demo User',
  roles: ['admin'],
  groups: ['bigsky-admin'],
};

export function useAuth(): UseAuthReturn {
  const [state, setState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null,
    isAuthenticated: false,
  });

  // Check if we're using mocks
  const useMocks = process.env.NEXT_PUBLIC_USE_MOCKS === 'true';

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));

      if (useMocks) {
        // Use mock user for development
        setState({
          user: MOCK_USER,
          loading: false,
          error: null,
          isAuthenticated: true,
        });
        return;
      }

      // Check for existing token
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setState({
          user: null,
          loading: false,
          error: null,
          isAuthenticated: false,
        });
        return;
      }

      // Verify token with backend
      const response = await api.get<UserInfo>('/auth/user');
      
      if (response.error) {
        // Token is invalid, clear it
        localStorage.removeItem('auth_token');
        setState({
          user: null,
          loading: false,
          error: response.error.message,
          isAuthenticated: false,
        });
        return;
      }

      if (response.data) {
        const user = UserInfoSchema.parse(response.data);
        setState({
          user,
          loading: false,
          error: null,
          isAuthenticated: true,
        });
      }
    } catch (error) {
      setState({
        user: null,
        loading: false,
        error: error instanceof Error ? error.message : 'Authentication failed',
        isAuthenticated: false,
      });
    }
  };

  const login = (provider: string = 'google') => {
    if (useMocks) {
      // Mock login
      setState({
        user: MOCK_USER,
        loading: false,
        error: null,
        isAuthenticated: true,
      });
      return;
    }

    // Redirect to OAuth provider
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
    const redirectUri = `${window.location.origin}/auth/callback`;
    const state = Math.random().toString(36).substring(7);
    
    // Store state for verification
    sessionStorage.setItem('oauth_state', state);
    
    const authUrl = `${baseUrl}/auth/login?provider=${provider}&redirect_uri=${encodeURIComponent(redirectUri)}&state=${state}`;
    window.location.href = authUrl;
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    sessionStorage.removeItem('oauth_state');
    
    setState({
      user: null,
      loading: false,
      error: null,
      isAuthenticated: false,
    });
  };

  const hasRole = (role: string): boolean => {
    if (!state.user) return false;
    return state.user.roles.includes(role);
  };

  const hasPermission = (permission: string): boolean => {
    if (!state.user) return false;
    
    // Simple permission mapping - in a real app, this would be more sophisticated
    const permissionMap: Record<string, string[]> = {
      'manage_users': ['owner', 'admin'],
      'manage_backups': ['owner', 'admin', 'editor'],
      'view_files': ['owner', 'admin', 'editor', 'viewer'],
      'upload_files': ['owner', 'admin', 'editor'],
      'delete_files': ['owner', 'admin'],
      'view_operations': ['owner', 'admin', 'editor', 'viewer'],
      'manage_settings': ['owner', 'admin'],
    };

    const requiredRoles = permissionMap[permission] || [];
    return state.user.roles.some(role => requiredRoles.includes(role));
  };

  return {
    ...state,
    login,
    logout,
    hasRole,
    hasPermission,
  };
}

// Auth context for global state
export interface AuthContextType extends UseAuthReturn {
  refresh: () => void;
}

// Handle OAuth callback
export async function handleAuthCallback(code: string, state: string): Promise<boolean> {
  try {
    const storedState = sessionStorage.getItem('oauth_state');
    if (state !== storedState) {
      throw new Error('Invalid state parameter');
    }

    const baseUrl = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
    const response = await fetch(`${baseUrl}/auth/callback?code=${code}&state=${state}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Authentication failed');
    }

    const data = await response.json();
    
    if (data.access_token) {
      localStorage.setItem('auth_token', data.access_token);
      sessionStorage.removeItem('oauth_state');
      return true;
    }

    return false;
  } catch (error) {
    console.error('Auth callback error:', error);
    return false;
  }
}
