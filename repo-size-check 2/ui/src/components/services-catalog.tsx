'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useServicesCatalog, useServicesStatus, useEnableService, useDisableService } from '@/lib/query';
import { useToast } from '@/hooks/use-toast';
import { Lock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { useState } from 'react';
import { ServiceCatalogItem } from '@/lib/schemas';

interface ServicesCatalogProps {
  enabled: boolean;
  canManage: boolean;
  loading: boolean;
}

export function ServicesCatalog({ enabled, canManage, loading }: ServicesCatalogProps) {
  const { data: catalog, isLoading: catalogLoading } = useServicesCatalog();
  const { data: status, isLoading: statusLoading } = useServicesStatus();
  const enableService = useEnableService();
  const disableService = useDisableService();
  const { toast } = useToast();
  const [optimisticStates, setOptimisticStates] = useState<Record<string, boolean>>({});

  const isLoading = loading || catalogLoading || statusLoading;

  const handleToggle = async (serviceId: string, currentState: boolean) => {
    if (!enabled || !canManage) {
      toast({
        title: "Access Denied",
        description: "Managed Services are not available in your current plan.",
        variant: "destructive",
      });
      return;
    }

    // Optimistic update
    setOptimisticStates(prev => ({ ...prev, [serviceId]: !currentState }));

    try {
      if (currentState) {
        await disableService.mutateAsync(serviceId);
        toast({
          title: "Service Disabled",
          description: "The service has been successfully disabled.",
        });
      } else {
        await enableService.mutateAsync(serviceId);
        toast({
          title: "Service Enabled",
          description: "The service has been successfully enabled.",
        });
      }
    } catch (error) {
      // Revert optimistic update
      setOptimisticStates(prev => ({ ...prev, [serviceId]: currentState }));
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to update service status.",
        variant: "destructive",
      });
    }
  };

  const getServiceStatus = (serviceId: string) => {
    const optimisticState = optimisticStates[serviceId];
    if (optimisticState !== undefined) {
      return optimisticState;
    }
    return status?.enabled.includes(serviceId) || false;
  };

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
              <Skeleton className="h-4 w-48" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-full mb-4" />
              <div className="flex items-center justify-between">
                <Skeleton className="h-6 w-16" />
                <Skeleton className="h-6 w-12" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!catalog || catalog.length === 0) {
    return (
      <Card>
        <CardContent className="text-center py-8">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Services Available</h3>
          <p className="text-gray-600">No managed services are currently available.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {catalog.map((service: ServiceCatalogItem) => {
        const isEnabled = getServiceStatus(service.id);
        const canToggle = enabled && canManage;
        
        return (
          <Card key={service.id} className="relative">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg font-semibold flex items-center space-x-2">
                    <span>{service.name}</span>
                    {service.category && (
                      <Badge variant="outline" className="text-xs">
                        {service.category}
                      </Badge>
                    )}
                  </CardTitle>
                  <p className="text-sm text-gray-600 mt-1">{service.desc}</p>
                </div>
                {!canToggle && (
                  <Lock className="h-4 w-4 text-gray-400 flex-shrink-0" />
                )}
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {isEnabled ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <XCircle className="h-4 w-4 text-gray-400" />
                  )}
                  <span className={`text-sm font-medium ${
                    isEnabled ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {isEnabled ? 'Enabled' : 'Disabled'}
                  </span>
                </div>
                <Switch
                  checked={isEnabled}
                  onCheckedChange={() => handleToggle(service.id, isEnabled)}
                  disabled={!canToggle || enableService.isPending || disableService.isPending}
                />
              </div>
              
              {!canToggle && (
                <div className="mt-3 p-2 bg-gray-50 rounded-md">
                  <p className="text-xs text-gray-500">
                    {!enabled 
                      ? "Available with Corporate plan"
                      : "Contact administrator for access"
                    }
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
