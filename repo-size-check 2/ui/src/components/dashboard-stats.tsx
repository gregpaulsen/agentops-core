'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  FolderOpen, 
  HardDrive, 
  Activity, 
  Clock,
  TrendingUp,
  AlertTriangle
} from 'lucide-react';
import { SummaryReport } from '@/lib/schemas';
import { formatFileSize } from '@/lib/theme';

interface DashboardStatsProps {
  summary: SummaryReport | undefined;
  loading: boolean;
}

export function DashboardStats({ summary, loading }: DashboardStatsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-8 w-16 mb-2" />
              <Skeleton className="h-3 w-32" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              No Data Available
            </CardTitle>
            <AlertTriangle className="h-4 w-4 text-gray-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-400">--</div>
            <p className="text-xs text-gray-500">Unable to load dashboard data</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { stats } = summary;

  const statCards = [
    {
      title: 'Total Files',
      value: stats.total_files.toLocaleString(),
      description: 'Files in storage',
      icon: FolderOpen,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Storage Used',
      value: formatFileSize(stats.storage_used_gb * 1024 * 1024 * 1024),
      description: `${((stats.storage_used_gb / stats.storage_limit_gb) * 100).toFixed(1)}% of ${formatFileSize(stats.storage_limit_gb * 1024 * 1024 * 1024)}`,
      icon: HardDrive,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Operations Today',
      value: stats.operations_today.toString(),
      description: 'Completed operations',
      icon: Activity,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      title: 'Total Backups',
      value: stats.total_backups.toString(),
      description: 'Available backups',
      icon: Clock,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => (
        <Card key={index}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">
              {stat.title}
            </CardTitle>
            <div className={`p-2 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gray-900">
              {stat.value}
            </div>
            <p className="text-xs text-gray-500">
              {stat.description}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
