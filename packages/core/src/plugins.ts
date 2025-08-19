import { z } from 'zod'

export type ToolDescriptor = {
  name: string
  slug: string
  version: string
  capabilities: string[]
  routes?: { setupPath?: string }
}

export interface JobRunner {
  enqueue<T>(queue: string, payload: T): Promise<string>
  getStatus(id: string): Promise<"queued" | "running" | "done" | "error">
}

export interface SecretStore {
  get(key: string, orgId?: string): Promise<string | null>
  set(key: string, value: string, orgId?: string): Promise<void>
}

// Plugin registration schema
export const toolDescriptorSchema = z.object({
  name: z.string().min(1),
  slug: z.string().min(1).regex(/^[a-z0-9-]+$/),
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  capabilities: z.array(z.string()).min(1),
  routes: z.object({
    setupPath: z.string().optional()
  }).optional()
})

export type ToolDescriptorSchema = z.infer<typeof toolDescriptorSchema>

// In-memory tool registry (in production, this would be persisted in the database)
const toolRegistry = new Map<string, ToolDescriptor>()

export const registerTool = (tool: ToolDescriptor): void => {
  // Validate the tool descriptor
  toolDescriptorSchema.parse(tool)
  
  // Store in registry
  toolRegistry.set(tool.slug, tool)
  
  console.log(`Tool registered: ${tool.name} (${tool.slug}) v${tool.version}`)
}

export const getTool = (slug: string): ToolDescriptor | undefined => {
  return toolRegistry.get(slug)
}

export const listTools = (): ToolDescriptor[] => {
  return Array.from(toolRegistry.values())
}

export const unregisterTool = (slug: string): boolean => {
  return toolRegistry.delete(slug)
}

// Default implementations for JobRunner and SecretStore
export class DefaultJobRunner implements JobRunner {
  async enqueue<T>(queue: string, payload: T): Promise<string> {
    const jobId = `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    // In a real implementation, this would add to a job queue
    console.log(`Job enqueued: ${jobId} on queue ${queue}`, payload)
    
    return jobId
  }
  
  async getStatus(id: string): Promise<"queued" | "running" | "done" | "error"> {
    // In a real implementation, this would check the job status
    console.log(`Checking status for job: ${id}`)
    return "queued"
  }
}

export class DefaultSecretStore implements SecretStore {
  private secrets = new Map<string, string>()
  
  async get(key: string, orgId?: string): Promise<string | null> {
    const fullKey = orgId ? `${orgId}:${key}` : key
    return this.secrets.get(fullKey) || null
  }
  
  async set(key: string, value: string, orgId?: string): Promise<void> {
    const fullKey = orgId ? `${orgId}:${key}` : key
    this.secrets.set(fullKey, value)
  }
}

// Export default instances
export const defaultJobRunner = new DefaultJobRunner()
export const defaultSecretStore = new DefaultSecretStore()
