import { http, HttpResponse } from 'msw';

// Mock data
const mockBrandingBigSky = {
  tenant_id: 'bigsky',
  tenant_name: 'Big Sky Ag',
  logo_url: '/assets/logos/bigsky.png',
  primary_color: '#1A5D2E',
  secondary_color: '#FFD54F',
  email_sender: 'no-reply@bigskyag.farm',
  legal_footer: '© 2025 Big Sky Ag LLC. All rights reserved.',
};

const mockBrandingAcme = {
  tenant_id: 'acme',
  tenant_name: 'Acme Corporation',
  logo_url: '/assets/logos/acme.png',
  primary_color: '#2563EB',
  secondary_color: '#F59E0B',
  email_sender: 'no-reply@acme.com',
  legal_footer: '© 2025 Acme Corporation. All rights reserved.',
};

const mockFeaturesBigSky = {
  tenant_id: 'bigsky',
  plan: 'starter',
  feature_flags: {
    ENABLE_SSO: false,
    ENABLE_AUDIT_LOG: true,
    ENABLE_SCIM: false,
    ENABLE_DLP: false,
    ENABLE_RATE_LIMITS: false,
    ENABLE_DASHBOARDS_PRO: false,
    ENABLE_MANAGED_SERVICES: false,
  },
  limits: {
    MAX_USERS: 10,
    MAX_STORAGE_GB: 50,
    MAX_API_QPS: 50,
    MAX_AI_TOKENS_PER_DAY: 100000,
  },
};

const mockFeaturesAcme = {
  tenant_id: 'acme',
  plan: 'corporate',
  feature_flags: {
    ENABLE_SSO: true,
    ENABLE_AUDIT_LOG: true,
    ENABLE_SCIM: true,
    ENABLE_DLP: true,
    ENABLE_RATE_LIMITS: true,
    ENABLE_DASHBOARDS_PRO: true,
    ENABLE_MANAGED_SERVICES: true,
  },
  limits: {
    MAX_USERS: 10000,
    MAX_STORAGE_GB: 10000,
    MAX_API_QPS: 2000,
    MAX_AI_TOKENS_PER_DAY: 5000000,
  },
};

const mockSummaryBigSky = {
  tenant: 'bigsky',
  plan: 'starter',
  status: 'active',
  stats: {
    total_files: 25,
    total_backups: 3,
    storage_used_gb: 2.4,
    storage_limit_gb: 50,
    operations_today: 4,
    last_backup: '2024-12-12T10:00:00Z',
  },
  recent_activity: [
    {
      type: 'file_upload',
      description: 'Uploaded field_report_2024_12_12.pdf',
      timestamp: new Date().toISOString(),
    },
    {
      type: 'backup_created',
      description: 'Created daily backup',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    },
    {
      type: 'system_check',
      description: 'Health check completed',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    },
  ],
  feature_flags: mockFeaturesBigSky.feature_flags,
  limits: mockFeaturesBigSky.limits,
};

const mockSummaryAcme = {
  tenant: 'acme',
  plan: 'corporate',
  status: 'active',
  stats: {
    total_files: 1250,
    total_backups: 15,
    storage_used_gb: 45.2,
    storage_limit_gb: 10000,
    operations_today: 45,
    last_backup: '2024-12-12T10:00:00Z',
  },
  recent_activity: [
    {
      type: 'file_upload',
      description: 'Uploaded quarterly_report.pdf',
      timestamp: new Date().toISOString(),
    },
    {
      type: 'backup_created',
      description: 'Created automated backup',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    },
    {
      type: 'system_check',
      description: 'Health check completed',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    },
  ],
  feature_flags: mockFeaturesAcme.feature_flags,
  limits: mockFeaturesAcme.limits,
};

const mockFiles = [
  {
    name: 'field_report_2024_12_12.pdf',
    path: '/files/field_report_2024_12_12.pdf',
    size: 1258291,
    modified: '2024-12-12T10:00:00Z',
    type: 'file',
  },
  {
    name: 'crop_analysis.json',
    path: '/files/crop_analysis.json',
    size: 2048,
    modified: '2024-12-12T09:30:00Z',
    type: 'file',
  },
  {
    name: 'equipment_maintenance.txt',
    path: '/files/equipment_maintenance.txt',
    size: 1024,
    modified: '2024-12-12T08:45:00Z',
    type: 'file',
  },
];

const mockBackups = {
  current_backups: 3,
  archive_files: 12,
  total_size_gb: 15.6,
  backup_dir: '/backups',
  archive_dir: '/backups/archive',
};

const mockOperations = [
  {
    id: 'op_001',
    operation: 'file_ingest',
    status: 'completed',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    duration: 1.2,
    details: 'Processed 5 files from ingest folder',
  },
  {
    id: 'op_002',
    operation: 'backup_rotation',
    status: 'completed',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
    duration: 0.8,
    details: 'Rotated 2 backup files to archive',
  },
  {
    id: 'op_003',
    operation: 'storage_sync',
    status: 'completed',
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
    duration: 2.1,
    details: 'Synced 15 files to cloud storage',
  },
  {
    id: 'op_004',
    operation: 'health_check',
    status: 'completed',
    timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
    duration: 0.3,
    details: 'System health check passed',
  },
];

const mockServicesCatalog = [
  {
    id: 'backup_monitoring',
    name: 'Backup Monitoring',
    desc: 'Automated alerts and monitoring for backup status and health',
    category: 'Backup',
    price_tier: 'premium',
  },
  {
    id: 'dr_snapshots',
    name: 'DR Snapshots',
    desc: 'Periodic disaster recovery snapshots with cross-region replication',
    category: 'Backup',
    price_tier: 'premium',
  },
  {
    id: 'audit_enhanced',
    name: 'Enhanced Audit',
    desc: 'Long-term audit log retention and advanced compliance reporting',
    category: 'Compliance',
    price_tier: 'enterprise',
  },
  {
    id: 'dlp_scanner',
    name: 'DLP Scanner',
    desc: 'Data loss prevention scanning for sensitive information',
    category: 'Security',
    price_tier: 'enterprise',
  },
  {
    id: 'dashboards_pro',
    name: 'Pro Dashboards',
    desc: 'Advanced analytics dashboards with custom reporting',
    category: 'Analytics',
    price_tier: 'premium',
  },
  {
    id: 'support_sla',
    name: 'Priority Support',
    desc: '24/7 priority support with guaranteed response times',
    category: 'Support',
    price_tier: 'enterprise',
  },
];

const mockServicesStatusBigSky = {
  enabled: [],
  available: ['backup_monitoring', 'dr_snapshots', 'audit_enhanced', 'dlp_scanner', 'dashboards_pro', 'support_sla'],
};

const mockServicesStatusAcme = {
  enabled: ['backup_monitoring', 'dashboards_pro'],
  available: ['backup_monitoring', 'dr_snapshots', 'audit_enhanced', 'dlp_scanner', 'dashboards_pro', 'support_sla'],
};

const mockUser = {
  sub: 'user_123',
  email: 'user@bigskyag.farm',
  name: 'Demo User',
  roles: ['admin'],
  groups: ['bigsky-admin'],
};

// Helper function to get tenant from request
function getTenantFromRequest(request: Request): string {
  const tenant = request.headers.get('X-Tenant') || 'bigsky';
  return tenant;
}

// Helper function to get mock data based on tenant
function getMockDataByTenant(tenant: string, dataType: string) {
  switch (dataType) {
    case 'branding':
      return tenant === 'acme' ? mockBrandingAcme : mockBrandingBigSky;
    case 'features':
      return tenant === 'acme' ? mockFeaturesAcme : mockFeaturesBigSky;
    case 'summary':
      return tenant === 'acme' ? mockSummaryAcme : mockSummaryBigSky;
    case 'servicesStatus':
      return tenant === 'acme' ? mockServicesStatusAcme : mockServicesStatusBigSky;
    default:
      return null;
  }
}

export const handlers = [
  // Branding endpoint
  http.get('/branding', () => {
    return HttpResponse.json(mockBrandingBigSky);
  }),

  // Features endpoint
  http.get('/features', ({ request }) => {
    const tenant = getTenantFromRequest(request);
    const features = getMockDataByTenant(tenant, 'features');
    return HttpResponse.json(features);
  }),

  // Summary endpoint
  http.get('/reports/summary', ({ request }) => {
    const tenant = getTenantFromRequest(request);
    const summary = getMockDataByTenant(tenant, 'summary');
    return HttpResponse.json(summary);
  }),

  // Files endpoint
  http.get('/files', () => {
    return HttpResponse.json(mockFiles);
  }),

  // Backups endpoint
  http.get('/backups', () => {
    return HttpResponse.json(mockBackups);
  }),

  // Operations endpoint
  http.get('/operations', () => {
    return HttpResponse.json(mockOperations);
  }),

  // Services catalog endpoint
  http.get('/services/catalog', () => {
    return HttpResponse.json(mockServicesCatalog);
  }),

  // Services status endpoint
  http.get('/services/status', ({ request }) => {
    const tenant = getTenantFromRequest(request);
    const status = getMockDataByTenant(tenant, 'servicesStatus');
    return HttpResponse.json(status);
  }),

  // Services enable endpoint
  http.post('/services/enable', async ({ request }) => {
    const body = await request.json() as any;
    return HttpResponse.json({
      message: `Service ${body?.service_id || 'unknown'} enabled successfully`
    });
  }),

  // Services disable endpoint
  http.post('/services/disable', async ({ request }) => {
    const body = await request.json() as any;
    return HttpResponse.json({
      message: `Service ${body?.service_id || 'unknown'} disabled successfully`
    });
  }),

  // Auth user endpoint
  http.get('/auth/user', () => {
    return HttpResponse.json(mockUser);
  }),

  // Health check endpoint
  http.get('/health', () => {
    return HttpResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      checks: {
        environment: true,
        paths: true,
        credentials: true,
        dependencies: true,
      },
      version: '1.0.0',
    });
  }),

  // Backup creation endpoint
  http.post('/backups', async ({ request }) => {
    const body = await request.json();
    if (body.dry_run) {
      return HttpResponse.json({
        message: 'Dry run backup simulation completed',
        dry_run: true
      });
    }
    return HttpResponse.json({
      message: 'Backup created successfully',
      backup_id: 'backup_123'
    });
  }),

  // File upload endpoint
  http.post('/files', () => {
    return HttpResponse.json({
      message: 'File uploaded successfully'
    });
  }),
];
