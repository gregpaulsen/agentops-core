import { z } from 'zod';

// API Error Response Schema
export const ApiErrorSchema = z.object({
  code: z.string().optional(),
  message: z.string(),
  details: z.any().optional(),
  trace_id: z.string().optional(),
});

export type ApiError = z.infer<typeof ApiErrorSchema>;

// API Response wrapper
export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

// Get tenant from environment or URL
export function getTenant(): string {
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('tenant') || process.env.NEXT_PUBLIC_TENANT || 'bigsky';
  }
  return process.env.NEXT_PUBLIC_TENANT || 'bigsky';
}

// Get API base URL
export function getApiBase(): string {
  return process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
}

// API client with tenant headers
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const baseUrl = getApiBase();
  const tenant = getTenant();
  
  const url = endpoint.startsWith('http') ? endpoint : `${baseUrl}${endpoint}`;
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Tenant': tenant,
    ...(options.headers as Record<string, string> || {}),
  };

  // Add auth token if available
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');

    if (!response.ok) {
      let error: ApiError;
      
      if (isJson) {
        const errorData = await response.json();
        error = ApiErrorSchema.parse(errorData);
      } else {
        error = {
          message: `HTTP ${response.status}: ${response.statusText}`,
          code: `HTTP_${response.status}`,
        };
      }
      
      return { error };
    }

    if (isJson) {
      const data = await response.json();
      return { data: data as T };
    }

    return { data: null as T };
  } catch (error) {
    const apiError: ApiError = {
      message: error instanceof Error ? error.message : 'Network error',
      code: 'NETWORK_ERROR',
    };
    return { error: apiError };
  }
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string) => apiRequest<T>(endpoint),
  
  post: <T>(endpoint: string, data?: any) => 
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    }),
  
  put: <T>(endpoint: string, data?: any) => 
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    }),
  
  delete: <T>(endpoint: string) => 
    apiRequest<T>(endpoint, { method: 'DELETE' }),
  
  upload: <T>(endpoint: string, file: File, onProgress?: (progress: number) => void) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return new Promise<ApiResponse<T>>((resolve) => {
      const xhr = new XMLHttpRequest();
      const tenant = getTenant();
      const baseUrl = getApiBase();
      const url = `${baseUrl}${endpoint}`;
      
      xhr.open('POST', url);
      xhr.setRequestHeader('X-Tenant', tenant);
      
      const token = localStorage.getItem('auth_token');
      if (token) {
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
      }
      
      if (onProgress) {
        xhr.upload.onprogress = (event) => {
          if (event.lengthComputable) {
            const progress = (event.loaded / event.total) * 100;
            onProgress(progress);
          }
        };
      }
      
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const data = JSON.parse(xhr.responseText);
            resolve({ data });
          } catch {
            resolve({ data: null as T });
          }
        } else {
          try {
            const error = JSON.parse(xhr.responseText);
            resolve({ error });
          } catch {
            resolve({
              error: {
                message: `Upload failed: ${xhr.statusText}`,
                code: `HTTP_${xhr.status}`,
              },
            });
          }
        }
      };
      
      xhr.onerror = () => {
        resolve({
          error: {
            message: 'Upload failed: Network error',
            code: 'NETWORK_ERROR',
          },
        });
      };
      
      xhr.send(formData);
    });
  },
};
