import { PrismaClient } from '@prisma/client'

declare global {
  var __prisma: PrismaClient | undefined
}

export const prisma = globalThis.__prisma || new PrismaClient()

if (process.env.NODE_ENV !== 'production') {
  globalThis.__prisma = prisma
}

// Safe hot-reload guard for development
if (process.env.NODE_ENV === 'development') {
  prisma.$connect()
    .then(() => console.log('✅ Prisma connected'))
    .catch((e) => console.error('❌ Prisma connection failed:', e))
}

export default prisma
