'use client';

import { Navigation } from '@/components/navigation';
import { ServicesCatalog } from '@/components/services-catalog';
import { useFeatures } from '@/lib/query';
import { useAuth } from '@/lib/auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Lock, Zap } from 'lucide-react';

export default function ServicesPage() {
  const { data: features, isLoading: featuresLoading } = useFeatures();
  const { isAuthenticated, loading: authLoading, hasPermission } = useAuth();

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900">Please sign in</h2>
            <p className="mt-2 text-gray-600">You need to be authenticated to view services.</p>
          </div>
        </div>
      </div>
    );
  }

  const canManageServices = hasPermission('manage_settings');
  const managedServicesEnabled = features?.feature_flags?.ENABLE_MANAGED_SERVICES || false;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="p-6">
        <div className="mx-auto max-w-7xl">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center space-x-3">
              <Zap className="h-8 w-8 text-green-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Managed Services</h1>
                <p className="mt-2 text-gray-600">
                  Configure and manage additional services for your platform
                </p>
              </div>
            </div>
          </div>

          {/* Plan Status */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <span>Plan Status</span>
                {!managedServicesEnabled && (
                  <Badge variant="secondary" className="flex items-center space-x-1">
                    <Lock className="h-3 w-3" />
                    <span>Starter Plan</span>
                  </Badge>
                )}
                {managedServicesEnabled && (
                  <Badge variant="default" className="bg-green-100 text-green-800">
                    <span>Corporate Plan</span>
                  </Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!managedServicesEnabled ? (
                <div className="text-gray-600">
                  <p className="mb-2">
                    Managed Services are available with the Corporate plan. 
                    Contact your administrator to upgrade your plan.
                  </p>
                  <p className="text-sm text-gray-500">
                    Current plan: <strong>Starter</strong> • 
                    Services available: <strong>Read-only</strong>
                  </p>
                </div>
              ) : (
                <div className="text-gray-600">
                  <p className="mb-2">
                    You have access to all managed services with your Corporate plan.
                  </p>
                  <p className="text-sm text-gray-500">
                    Current plan: <strong>Corporate</strong> • 
                    Services available: <strong>Full access</strong>
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Services Catalog */}
          <ServicesCatalog 
            enabled={managedServicesEnabled}
            canManage={canManageServices}
            loading={featuresLoading}
          />
        </div>
      </main>
    </div>
  );
}
