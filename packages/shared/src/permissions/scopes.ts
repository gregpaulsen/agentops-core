export const GMAIL_SCOPES = {
  'gmail.read': 'Read Gmail messages and metadata',
  'gmail.modify': 'Modify Gmail messages (send, delete, labels)',
  'gmail.compose': 'Compose and send emails',
  'gmail.labels': 'Manage Gmail labels'
} as const

export const DRIVE_SCOPES = {
  'drive.read': 'Read Google Drive files and metadata',
  'drive.write': 'Create and modify Google Drive files',
  'drive.delete': 'Delete Google Drive files',
  'drive.share': 'Share Google Drive files'
} as const

export const SLACK_SCOPES = {
  'slack.read': 'Read Slack messages and channels',
  'slack.post': 'Post messages to Slack channels',
  'slack.users': 'Read Slack user information',
  'slack.files': 'Upload and manage Slack files'
} as const

export const STRIPE_SCOPES = {
  'stripe.read': 'Read Stripe data (customers, payments, etc.)',
  'stripe.write': 'Create and modify Stripe resources',
  'stripe.refunds': 'Process refunds',
  'stripe.webhooks': 'Manage webhook endpoints'
} as const

export const NOTION_SCOPES = {
  'notion.read': 'Read Notion pages and databases',
  'notion.write': 'Create and modify Notion content',
  'notion.comments': 'Add and manage comments',
  'notion.users': 'Read Notion user information'
} as const

export const ALL_SCOPES = {
  ...GMAIL_SCOPES,
  ...DRIVE_SCOPES,
  ...SLACK_SCOPES,
  ...STRIPE_SCOPES,
  ...NOTION_SCOPES
} as const

export type Scope = keyof typeof ALL_SCOPES

export function getScopesForConnector(connector: string): string[] {
  switch (connector) {
    case 'gmail':
      return Object.keys(GMAIL_SCOPES)
    case 'drive':
      return Object.keys(DRIVE_SCOPES)
    case 'slack':
      return Object.keys(SLACK_SCOPES)
    case 'stripe':
      return Object.keys(STRIPE_SCOPES)
    case 'notion':
      return Object.keys(NOTION_SCOPES)
    default:
      return []
  }
}

export function validateScopes(scopes: string[]): boolean {
  return scopes.every(scope => scope in ALL_SCOPES)
}
