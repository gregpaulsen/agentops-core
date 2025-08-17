import { api } from './api';
import { BrandingSchema, type Branding } from './schemas';

// Theme context type
export interface ThemeContext {
  branding: Branding | null;
  loading: boolean;
  error: string | null;
}

// Load branding and apply theme
export async function loadTheme(): Promise<Branding | null> {
  try {
    const response = await api.get<Branding>('/branding');
    
    if (response.error) {
      console.error('Failed to load branding:', response.error);
      return null;
    }
    
    if (response.data) {
      const branding = BrandingSchema.parse(response.data);
      applyTheme(branding);
      return branding;
    }
    
    return null;
  } catch (error) {
    console.error('Error loading theme:', error);
    return null;
  }
}

// Apply theme to CSS variables
export function applyTheme(branding: Branding): void {
  if (typeof document === 'undefined') return;
  
  const root = document.documentElement;
  
  // Set CSS custom properties
  root.style.setProperty('--primary-color', branding.primary_color);
  root.style.setProperty('--secondary-color', branding.secondary_color);
  root.style.setProperty('--tenant-name', `"${branding.tenant_name}"`);
  root.style.setProperty('--logo-url', `url(${branding.logo_url})`);
  
  // Update document title
  document.title = `${branding.tenant_name} - PaulyOps`;
  
  // Update favicon if logo is available
  if (branding.logo_url && branding.logo_url !== '/assets/logos/bigsky.png') {
    const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    (link as HTMLLinkElement).type = 'image/x-icon';
    (link as HTMLLinkElement).rel = 'shortcut icon';
    (link as HTMLLinkElement).href = branding.logo_url;
    document.getElementsByTagName('head')[0].appendChild(link);
  }
}

// Get theme CSS variables
export function getThemeVariables(): Record<string, string> {
  if (typeof document === 'undefined') {
    return {
      '--primary-color': '#1A5D2E',
      '--secondary-color': '#FFD54F',
      '--tenant-name': '"Big Sky Ag"',
      '--logo-url': 'url(/assets/logos/bigsky.png)',
    };
  }
  
  const root = document.documentElement;
  const computedStyle = getComputedStyle(root);
  
  return {
    '--primary-color': computedStyle.getPropertyValue('--primary-color') || '#1A5D2E',
    '--secondary-color': computedStyle.getPropertyValue('--secondary-color') || '#FFD54F',
    '--tenant-name': computedStyle.getPropertyValue('--tenant-name') || '"Big Sky Ag"',
    '--logo-url': computedStyle.getPropertyValue('--logo-url') || 'url(/assets/logos/bigsky.png)',
  };
}

// Format file size
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Format date
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// Format duration
export function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  if (seconds < 3600) return `${(seconds / 60).toFixed(1)}m`;
  return `${(seconds / 3600).toFixed(1)}h`;
}

// Get status color
export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'completed':
    case 'success':
      return 'text-green-600 bg-green-50';
    case 'running':
    case 'in_progress':
      return 'text-blue-600 bg-blue-50';
    case 'failed':
    case 'error':
      return 'text-red-600 bg-red-50';
    case 'queued':
    case 'pending':
      return 'text-yellow-600 bg-yellow-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
}

// Get operation icon
export function getOperationIcon(operation: string): string {
  switch (operation.toLowerCase()) {
    case 'file_ingest':
      return '📁';
    case 'backup_rotation':
      return '💾';
    case 'storage_sync':
      return '☁️';
    case 'health_check':
      return '🏥';
    case 'system_check':
      return '🔍';
    default:
      return '⚙️';
  }
}
