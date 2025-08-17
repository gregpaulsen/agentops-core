import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { api } from './api';
import {
  Backup,
  Branding,
  Features,
  File,
  Operation,
  ServiceCatalogItem,
  ServicesStatus,
  ServiceToggleRequest,
  SummaryReport
} from './schemas';

// Create a client
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Query keys
export const queryKeys = {
  branding: ['branding'],
  features: ['features'],
  summary: ['summary'],
  files: ['files'],
  backups: ['backups'],
  operations: ['operations'],
  services: {
    catalog: ['services', 'catalog'],
    status: ['services', 'status'],
  },
} as const;

// Custom hooks
export function useBranding() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.branding,
    queryFn: async (): Promise<Branding> => {
      const response = await api.get<Branding>('/branding');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useFeatures() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.features,
    queryFn: async (): Promise<Features> => {
      const response = await api.get<Features>('/features');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useSummary() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.summary,
    queryFn: async (): Promise<SummaryReport> => {
      const response = await api.get<SummaryReport>('/reports/summary');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useFiles() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.files,
    queryFn: async (): Promise<File[]> => {
      const response = await api.get<File[]>('/files');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useBackups() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.backups,
    queryFn: async (): Promise<Backup> => {
      const response = await api.get<Backup>('/backups');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useOperations() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.operations,
    queryFn: async (): Promise<Operation[]> => {
      const response = await api.get<Operation[]>('/operations');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

// Managed Services hooks
export function useServicesCatalog() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.services.catalog,
    queryFn: async (): Promise<ServiceCatalogItem[]> => {
      const response = await api.get<ServiceCatalogItem[]>('/services/catalog');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

export function useServicesStatus() {
  const { useQuery } = require('@tanstack/react-query');

  return useQuery({
    queryKey: queryKeys.services.status,
    queryFn: async (): Promise<ServicesStatus> => {
      const response = await api.get<ServicesStatus>('/services/status');
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
  });
}

// Mutation hooks
export function useCreateBackup() {
  const { useMutation, useQueryClient } = require('@tanstack/react-query');
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (dryRun: boolean = false) => {
      const response = await api.post<{ message: string; backup_id?: string }>('/backups', { dry_run: dryRun });
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.backups });
      queryClient.invalidateQueries({ queryKey: queryKeys.summary });
    },
  });
}

export function useUploadFile() {
  const { useMutation, useQueryClient } = require('@tanstack/react-query');
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (file: globalThis.File) => {
      const response = await api.upload<{ message: string }>('/files', file);
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.files });
      queryClient.invalidateQueries({ queryKey: queryKeys.summary });
    },
  });
}

export function useEnableService() {
  const { useMutation, useQueryClient } = require('@tanstack/react-query');
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (serviceId: string) => {
      const request: ServiceToggleRequest = { service_id: serviceId };
      const response = await api.post<{ message: string }>('/services/enable', request);
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.services.status });
    },
  });
}

export function useDisableService() {
  const { useMutation, useQueryClient } = require('@tanstack/react-query');
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (serviceId: string) => {
      const request: ServiceToggleRequest = { service_id: serviceId };
      const response = await api.post<{ message: string }>('/services/disable', request);
      if (response.error) throw new Error(response.error.message);
      return response.data!;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.services.status });
    },
  });
}

// Provider component
export function QueryProvider({ children }: { children: React.ReactNode }) {
  const React = require('react');

  return React.createElement(QueryClientProvider, { client: queryClient }, [
    children,
    React.createElement(ReactQueryDevtools, { initialIsOpen: false, key: 'devtools' })
  ]);
}
