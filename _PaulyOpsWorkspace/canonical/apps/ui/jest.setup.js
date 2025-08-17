// Production hardening: Jest setup for comprehensive testing
import '@testing-library/jest-dom'

// Production hardening: mock environment variables
process.env.NODE_ENV = 'test'
process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/paulyops_test'
process.env.REDIS_URL = 'redis://localhost:6379'
process.env.JWT_SECRET = 'test-jwt-secret'
process.env.ENCRYPTION_KEY = 'test-encryption-key'
process.env.SESSION_SECRET = 'test-session-secret'
process.env.STRIPE_SECRET_KEY = 'sk_test_123'
process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test_123'

// Production hardening: mock crypto for consistent testing
Object.defineProperty(global, 'crypto', {
  value: {
    randomUUID: () => 'test-uuid-' + Math.random().toString(36).substr(2, 9),
    getRandomValues: (arr) => {
      for (let i = 0; i < arr.length; i++) {
        arr[i] = Math.floor(Math.random() * 256)
      }
      return arr
    },
    randomBytes: (size) => {
      const bytes = new Uint8Array(size)
      for (let i = 0; i < size; i++) {
        bytes[i] = Math.floor(Math.random() * 256)
      }
      return bytes
    }
  }
})

// Production hardening: mock console methods for cleaner test output
const originalConsoleError = console.error
const originalConsoleWarn = console.warn
const originalConsoleLog = console.log

beforeAll(() => {
  // Suppress console output during tests unless explicitly needed
  console.error = jest.fn()
  console.warn = jest.fn()
  console.log = jest.fn()
})

afterAll(() => {
  // Restore console methods
  console.error = originalConsoleError
  console.warn = originalConsoleWarn
  console.log = originalConsoleLog
})

// Production hardening: mock fetch for API testing
global.fetch = jest.fn()

// Production hardening: mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    prefetch: jest.fn(),
  }),
  useSearchParams: () => new URLSearchParams(),
  usePathname: () => '/',
}))

// Production hardening: mock Next.js auth
jest.mock('@/lib/auth', () => ({
  auth: jest.fn(() => ({
    user: {
      id: 'test-user-id',
      email: 'test@example.com',
      name: 'Test User'
    },
    orgId: 'test-org-id'
  }))
}))

// Production hardening: mock Redis for testing
jest.mock('@/lib/redis', () => ({
  getRedis: jest.fn(() => ({
    ping: jest.fn(() => Promise.resolve('PONG')),
    set: jest.fn(() => Promise.resolve('OK')),
    get: jest.fn(() => Promise.resolve('test-value')),
    setex: jest.fn(() => Promise.resolve('OK')),
    del: jest.fn(() => Promise.resolve(1)),
    incr: jest.fn(() => Promise.resolve(1)),
    expire: jest.fn(() => Promise.resolve(1)),
    info: jest.fn(() => Promise.resolve('used_memory:123456')),
    quit: jest.fn(() => Promise.resolve('OK')),
  })),
  closeRedis: jest.fn(() => Promise.resolve()),
}))

// Production hardening: mock Prisma for testing
jest.mock('@/lib/db', () => ({
  prisma: {
    $connect: jest.fn(),
    $disconnect: jest.fn(),
    $queryRaw: jest.fn(() => Promise.resolve([{ health: 1 }])),
    organization: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    user: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    organizationMember: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    role: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agent: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agentCatalog: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agentVersion: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agentInstall: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    orgPreference: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    storageConfig: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    securityConfig: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agentConfig: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    auditLog: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
    agentEvent: {
      create: jest.fn(),
      findFirst: jest.fn(),
      findUnique: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      deleteMany: jest.fn(),
    },
  }
}))

// Production hardening: mock file system operations
jest.mock('fs/promises', () => ({
  mkdir: jest.fn(() => Promise.resolve()),
  writeFile: jest.fn(() => Promise.resolve()),
  rm: jest.fn(() => Promise.resolve()),
  chmod: jest.fn(() => Promise.resolve()),
}))

// Production hardening: mock path operations
jest.mock('path', () => ({
  join: jest.fn((...args) => args.join('/')),
  resolve: jest.fn((...args) => args.join('/')),
}))

// Production hardening: mock child process
jest.mock('child_process', () => ({
  execSync: jest.fn(() => Buffer.from('success')),
}))

// Production hardening: test utilities
global.testUtils = {
  // Mock organization data
  mockOrganization: {
    id: 'test-org-id',
    name: 'Test Organization',
    slug: 'test-organization',
    industry: 'agriculture',
    size: '1-10',
    metadata: {
      setupWizard: true,
      generatedAt: new Date().toISOString(),
      version: '1.0.0'
    }
  },
  
  // Mock user data
  mockUser: {
    id: 'test-user-id',
    email: 'test@example.com',
    name: 'Test User'
  },
  
  // Mock onboarding data
  mockOnboardingData: {
    organization: {
      name: 'Test Corp',
      industry: 'finance',
      complianceLevel: 'soc2',
      size: '51-200'
    },
    storage: {
      providers: ['google-drive', 'dropbox'],
      backupStrategy: 'hybrid',
      retentionDays: 365
    },
    security: {
      rbacModel: 'granular',
      auditLogging: true,
      dataRetention: 2555,
      encryptionLevel: 'enhanced'
    },
    agents: {
      defaultAgents: ['file-processor', 'data-analyzer'],
      autoRouting: true,
      confidenceThreshold: 0.9,
      monitoringEnabled: true
    }
  },
  
  // Mock agent package
  mockAgentPackage: Buffer.from(`
    MANIFEST:{"id":"test-agent","name":"Test Agent","version":"1.0.0","capabilities":["file_processing"],"permissions":["read_files"],"entryPoint":"index.js","configSchema":{},"minPlatformVersion":"1.0.0","tags":[],"category":"utility","pricing":{"model":"free"},"security":{"sandboxed":true,"networkAccess":false,"fileSystemAccess":false,"requiresApproval":false},"metadata":{}}
    END_MANIFEST
    // Agent code here
  `),
  
  // Helper to reset all mocks
  resetMocks: () => {
    jest.clearAllMocks()
    jest.resetModules()
  },
  
  // Helper to create mock Prisma responses
  mockPrismaResponse: (model, method, response) => {
    const mockModel = require('@/lib/db').prisma[model]
    mockModel[method].mockResolvedValue(response)
  },
  
  // Helper to create mock Prisma errors
  mockPrismaError: (model, method, error) => {
    const mockModel = require('@/lib/db').prisma[model]
    mockModel[method].mockRejectedValue(error)
  }
}

// Production hardening: global test timeout
jest.setTimeout(30000)

// Production hardening: test environment setup
beforeEach(() => {
  // Reset all mocks before each test
  jest.clearAllMocks()
  
  // Reset fetch mock
  if (global.fetch) {
    (global.fetch as jest.Mock).mockClear()
  }
  
  // Setup default mock responses
  global.testUtils.resetMocks()
})

// Production hardening: test cleanup
afterEach(() => {
  // Clean up any remaining mocks
  jest.clearAllMocks()
})
