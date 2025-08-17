'use client';

import { Navigation } from '@/components/navigation';
import { DashboardStats } from '@/components/dashboard-stats';
import { DashboardCharts } from '@/components/dashboard-charts';
import { RecentOperations } from '@/components/recent-operations';
import { useSummary, useFeatures } from '@/lib/query';
import { useAuth } from '@/lib/auth';
import { useEffect } from 'react';
import { createMockWebSocket } from '@/lib/ws';

export default function DashboardPage() {
  const { data: summary, isLoading: summaryLoading } = useSummary();
  const { data: features, isLoading: featuresLoading } = useFeatures();
  const { isAuthenticated, loading: authLoading } = useAuth();

  // Initialize mock WebSocket for development
  useEffect(() => {
    if (process.env.NEXT_PUBLIC_USE_MOCKS === 'true') {
      const cleanup = createMockWebSocket();
      return cleanup;
    }
  }, []);

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
            <p className="mt-2 text-gray-600">You need to be authenticated to view the dashboard.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="p-6">
        <div className="mx-auto max-w-7xl">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-2 text-gray-600">
              Welcome to your PaulyOps platform overview
            </p>
          </div>

          {/* Stats Cards */}
          <DashboardStats 
            summary={summary} 
            loading={summaryLoading} 
          />

          {/* Charts */}
          <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
            <DashboardCharts 
              summary={summary} 
              loading={summaryLoading} 
            />
          </div>

          {/* Recent Operations */}
          <div className="mt-8">
            <RecentOperations />
          </div>
        </div>
      </main>
    </div>
  );
}
