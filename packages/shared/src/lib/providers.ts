export type ProviderType = 'gdrive' | 'dropbox' | 's3' | 'local'

export interface ProviderConfig {
  name: ProviderType
  priority: number
  enabled: boolean
}

const providers: ProviderConfig[] = [
  { name: 'gdrive', priority: 1, enabled: true },
  { name: 'dropbox', priority: 2, enabled: true },
  { name: 's3', priority: 3, enabled: true },
  { name: 'local', priority: 4, enabled: true },
]

export function currentProvider(): ProviderType {
  const primary = providers.find(p => p.enabled && p.priority === 1)
  return primary?.name || 'local'
}

export function fallbackProvider(): ProviderType {
  const fallback = providers.find(p => p.enabled && p.priority > 1)
  return fallback?.name || 'local'
}

export function getProviderByPriority(priority: number): ProviderType | null {
  const provider = providers.find(p => p.enabled && p.priority === priority)
  return provider?.name || null
}

export function enableProvider(name: ProviderType, enabled: boolean = true) {
  const provider = providers.find(p => p.name === name)
  if (provider) {
    provider.enabled = enabled
  }
}

export function setProviderPriority(name: ProviderType, priority: number) {
  const provider = providers.find(p => p.name === name)
  if (provider) {
    provider.priority = priority
  }
}

export function getAvailableProviders(): ProviderType[] {
  return providers
    .filter(p => p.enabled)
    .sort((a, b) => a.priority - b.priority)
    .map(p => p.name)
}
