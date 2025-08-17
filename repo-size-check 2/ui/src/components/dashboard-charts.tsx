'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { SummaryReport } from '@/lib/schemas';

interface DashboardChartsProps {
  summary: SummaryReport | undefined;
  loading: boolean;
}

export function DashboardCharts({ summary, loading }: DashboardChartsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <Skeleton className="h-4 w-32" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <Skeleton className="h-4 w-32" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Storage Usage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center h-64 text-gray-500">
              No data available
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-center h-64 text-gray-500">
              No data available
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { stats, recent_activity } = summary;

  // Storage usage data for pie chart
  const storageData = [
    { name: 'Used', value: stats.storage_used_gb, color: '#10B981' },
    { name: 'Available', value: stats.storage_limit_gb - stats.storage_used_gb, color: '#E5E7EB' },
  ];

  // Activity data for bar chart (last 7 days)
  const activityData = [
    { day: 'Mon', operations: 12, uploads: 8 },
    { day: 'Tue', operations: 15, uploads: 10 },
    { day: 'Wed', operations: 8, uploads: 5 },
    { day: 'Thu', operations: 20, uploads: 12 },
    { day: 'Fri', operations: 18, uploads: 9 },
    { day: 'Sat', operations: 5, uploads: 2 },
    { day: 'Sun', operations: 3, uploads: 1 },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Storage Usage Pie Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Storage Usage</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={storageData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {storageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value: number) => [`${value} GB`, 'Storage']}
                labelFormatter={(label) => `${label} Storage`}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 text-center">
            <div className="text-2xl font-bold text-gray-900">
              {stats.storage_used_gb} GB
            </div>
            <div className="text-sm text-gray-500">
              of {stats.storage_limit_gb} GB used
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Activity Bar Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold">Weekly Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={activityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="operations" fill="#3B82F6" name="Operations" />
              <Bar dataKey="uploads" fill="#10B981" name="Uploads" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
