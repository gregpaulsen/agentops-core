import pino from 'pino'
import { prisma } from './db'

// Request ID middleware for API routes
export function getRequestId(): string {
  return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

// Base logger configuration
const baseLogger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
})

// Create logger with context
export function createLogger(context: {
  orgId?: string
  userId?: string
  requestId?: string
}) {
  return baseLogger.child({
    orgId: context.orgId || 'unknown',
    userId: context.userId || 'unknown',
    requestId: context.requestId || getRequestId(),
  })
}

// Default logger instance
export const logger = createLogger({})

// Audit logging function
export async function audit(
  action: string,
  context: {
    orgId: string
    userId?: string
    entity?: string
    entityId?: string
    metadata?: Record<string, any>
  }
) {
  const { orgId, userId, entity, entityId, metadata } = context
  
  // Log to console
  logger.info({
    type: 'audit',
    action,
    entity,
    entityId,
    metadata,
  }, `AUDIT: ${action}`)
  
  // Write to database
  try {
    await prisma.auditLog.create({
      data: {
        orgId,
        userId,
        action,
        entity,
        entityId,
        metadata: metadata || {},
      },
    })
  } catch (error) {
    logger.error({ error }, 'Failed to write audit log to database')
  }
}

// Telemetry logging function
export async function telemetry(
  type: string,
  context: {
    orgId: string
    userId?: string
    payload?: Record<string, any>
  }
) {
  const { orgId, userId, payload } = context
  
  // Log to console
  logger.info({
    type: 'telemetry',
    telemetryType: type,
    payload,
  }, `TELEMETRY: ${type}`)
  
  // Write to database
  try {
    await prisma.telemetryEvent.create({
      data: {
        orgId,
        userId,
        type,
        payload: payload || {},
      },
    })
  } catch (error) {
    logger.error({ error }, 'Failed to write telemetry event to database')
  }
}
