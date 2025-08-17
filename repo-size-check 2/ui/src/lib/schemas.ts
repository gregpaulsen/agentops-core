import { z } from 'zod';

// Branding Schema
export const BrandingSchema = z.object({
  tenant_id: z.string(),
  tenant_name: z.string(),
  logo_url: z.string(),
  primary_color: z.string(),
  secondary_color: z.string(),
  email_sender: z.string(),
  legal_footer: z.string(),
});

export type Branding = z.infer<typeof BrandingSchema>;

// Feature Flags Schema
export const FeatureFlagsSchema = z.object({
  ENABLE_SSO: z.boolean(),
  ENABLE_AUDIT_LOG: z.boolean(),
  ENABLE_SCIM: z.boolean(),
  ENABLE_DLP: z.boolean(),
  ENABLE_RATE_LIMITS: z.boolean(),
  ENABLE_DASHBOARDS_PRO: z.boolean(),
});

export type FeatureFlags = z.infer<typeof FeatureFlagsSchema>;

// Limits Schema
export const LimitsSchema = z.object({
  MAX_USERS: z.number(),
  MAX_STORAGE_GB: z.number(),
  MAX_API_QPS: z.number(),
  MAX_AI_TOKENS_PER_DAY: z.number(),
});

export type Limits = z.infer<typeof LimitsSchema>;

// Features Schema
export const FeaturesSchema = z.object({
  tenant_id: z.string(),
  plan: z.string(),
  feature_flags: FeatureFlagsSchema,
  limits: LimitsSchema,
});

export type Features = z.infer<typeof FeaturesSchema>;

// File Schema
export const FileSchema = z.object({
  name: z.string(),
  path: z.string(),
  size: z.number(),
  modified: z.string(),
  type: z.string(),
});

export type File = z.infer<typeof FileSchema>;

// Backup Schema
export const BackupSchema = z.object({
  current_backups: z.number(),
  archive_files: z.number(),
  total_size_gb: z.number(),
  backup_dir: z.string(),
  archive_dir: z.string(),
});

export type Backup = z.infer<typeof BackupSchema>;

// Operation Schema
export const OperationSchema = z.object({
  id: z.string(),
  operation: z.string(),
  status: z.string(),
  timestamp: z.string(),
  duration: z.number(),
  details: z.string(),
});

export type Operation = z.infer<typeof OperationSchema>;

// Recent Activity Schema
export const RecentActivitySchema = z.object({
  type: z.string(),
  description: z.string(),
  timestamp: z.string(),
});

export type RecentActivity = z.infer<typeof RecentActivitySchema>;

// Stats Schema
export const StatsSchema = z.object({
  total_files: z.number(),
  total_backups: z.number(),
  storage_used_gb: z.number(),
  storage_limit_gb: z.number(),
  operations_today: z.number(),
  last_backup: z.string(),
});

export type Stats = z.infer<typeof StatsSchema>;

// Summary Report Schema
export const SummaryReportSchema = z.object({
  tenant: z.string(),
  plan: z.string(),
  status: z.string(),
  stats: StatsSchema,
  recent_activity: z.array(RecentActivitySchema),
  feature_flags: FeatureFlagsSchema,
  limits: LimitsSchema,
});

export type SummaryReport = z.infer<typeof SummaryReportSchema>;

// Health Check Schema
export const HealthCheckSchema = z.object({
  status: z.string(),
  timestamp: z.string(),
  checks: z.object({
    environment: z.boolean(),
    paths: z.boolean(),
    credentials: z.boolean(),
    dependencies: z.boolean(),
  }),
  version: z.string(),
});

export type HealthCheck = z.infer<typeof HealthCheckSchema>;

// User Info Schema
export const UserInfoSchema = z.object({
  sub: z.string(),
  email: z.string(),
  name: z.string(),
  roles: z.array(z.string()),
  groups: z.array(z.string()),
});

export type UserInfo = z.infer<typeof UserInfoSchema>;

// Auth Response Schema
export const AuthResponseSchema = z.object({
  message: z.string(),
  access_token: z.string(),
  token_type: z.string(),
  expires_in: z.number(),
});

export type AuthResponse = z.infer<typeof AuthResponseSchema>;

// Managed Services Schemas
export const ServiceCatalogItemSchema = z.object({
  id: z.string(),
  name: z.string(),
  desc: z.string(),
  category: z.string().optional(),
  price_tier: z.string().optional(),
});

export type ServiceCatalogItem = z.infer<typeof ServiceCatalogItemSchema>;

export const ServicesStatusSchema = z.object({
  enabled: z.array(z.string()),
  available: z.array(z.string()),
});

export type ServicesStatus = z.infer<typeof ServicesStatusSchema>;

export const ServiceToggleRequestSchema = z.object({
  service_id: z.string(),
});

export type ServiceToggleRequest = z.infer<typeof ServiceToggleRequestSchema>;
