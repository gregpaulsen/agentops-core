import { z } from 'zod'

export const connectorSchema = z.enum(['gmail', 'drive', 'slack', 'stripe', 'notion'])

export const connectorConfigSchema = z.object({
  connector: connectorSchema,
  scopes: z.array(z.string()).min(1)
})

export const agentManifestSchema = z.object({
  name: z.string().min(1),
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  description: z.string().optional(),
  connectors: z.array(connectorConfigSchema).min(1),
  inputs: z.record(z.any()).optional(),
  outputs: z.record(z.any()).optional(),
  riskLevel: z.enum(['low', 'medium', 'high']).default('medium')
})

export type AgentManifest = z.infer<typeof agentManifestSchema>
export type ConnectorConfig = z.infer<typeof connectorConfigSchema>

export function validateManifest(manifest: unknown): asserts manifest is AgentManifest {
  agentManifestSchema.parse(manifest)
}

export function isValidManifest(manifest: unknown): manifest is AgentManifest {
  return agentManifestSchema.safeParse(manifest).success
}
