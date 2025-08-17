'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { queryClient, useOperations } from '@/lib/query';
import { Operation } from '@/lib/schemas';
import { formatDate, formatDuration, getOperationIcon, getStatusColor } from '@/lib/theme';
import { useWebSocket } from '@/lib/ws';
import { Eye, RefreshCw } from 'lucide-react';

export function RecentOperations() {
  const { data: operations, isLoading, refetch } = useOperations();

  // Subscribe to WebSocket updates
  useWebSocket('operation_completed', (data) => {
    // Invalidate operations query to refresh data
    queryClient.invalidateQueries({ queryKey: ['operations'] });
  });

  useWebSocket('backup_created', (data) => {
    // Invalidate operations query to refresh data
    queryClient.invalidateQueries({ queryKey: ['operations'] });
  });

  useWebSocket('file_uploaded', (data) => {
    // Invalidate operations query to refresh data
    queryClient.invalidateQueries({ queryKey: ['operations'] });
  });

  if (isLoading) {
    return (
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-8 w-20" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex items-center space-x-4">
                <Skeleton className="h-4 w-4" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-4 w-48" />
                  <Skeleton className="h-3 w-32" />
                </div>
                <Skeleton className="h-6 w-16" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!operations || operations.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Recent Operations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            <p>No operations found</p>
            <p className="text-sm">Operations will appear here as they complete</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg font-semibold">Recent Operations</CardTitle>
        <Button
          variant="outline"
          size="sm"
          onClick={() => refetch()}
          className="flex items-center space-x-2"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Refresh</span>
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {operations.slice(0, 10).map((operation: Operation) => (
            <div
              key={operation.id}
              className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center space-x-4">
                <div className="text-2xl">
                  {getOperationIcon(operation.operation)}
                </div>
                <div>
                  <div className="font-medium text-gray-900">
                    {operation.operation.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </div>
                  <div className="text-sm text-gray-500">
                    {operation.details}
                  </div>
                  <div className="text-xs text-gray-400">
                    {formatDate(operation.timestamp)}
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Badge className={getStatusColor(operation.status)}>
                  {operation.status}
                </Badge>
                <div className="text-sm text-gray-500">
                  {formatDuration(operation.duration)}
                </div>
                <Button variant="ghost" size="sm">
                  <Eye className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>

        {operations.length > 10 && (
          <div className="mt-4 text-center">
            <Button variant="outline" size="sm">
              View All Operations
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
