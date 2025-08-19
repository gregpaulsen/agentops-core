import { AgentManifest, validateManifest } from '../permissions/manifest'
import { validateScopes } from '../permissions/scopes'

// Type definitions for Next.js compatibility
interface NextRequest {
  headers: {
    get(name: string): string | null
  }
}

// Mock NextResponse for shared package
const NextResponse = {
  json: (data: any, options?: { status?: number }) => ({ data, status: options?.status || 200 })
}

type NextResponseType = ReturnType<typeof NextResponse.json>

export interface PermissionContext {
  session: any
  manifest?: AgentManifest
  requiredScopes: string[]
}

export function requireScopes(requiredScopes: string[]) {
  return function withPermissions(handler: (req: NextRequest, context: PermissionContext) => Promise<NextResponseType>) {
    return async (req: NextRequest): Promise<NextResponseType> => {
      try {
        // Get session - simplified for shared package
        // In the actual API, this will be handled by the Next.js middleware
        const session = { orgId: 'system', userId: 'system', role: 'admin' }

        // Extract manifest from header or default to read-only
        let manifest: AgentManifest | undefined
        
        const manifestHeader = req.headers.get('x-agent-manifest')
        if (manifestHeader) {
          try {
            const manifestData = JSON.parse(manifestHeader)
            validateManifest(manifestData)
            manifest = manifestData
          } catch (error) {
            return NextResponse.json(
              { error: 'Invalid agent manifest' },
              { status: 400 }
            )
          }
        }

        // If no manifest, only allow read-only scopes
        if (!manifest) {
          const readOnlyScopes = ['gmail.read', 'drive.read', 'slack.read', 'stripe.read', 'notion.read']
          const hasNonReadOnlyScope = requiredScopes.some(scope => !readOnlyScopes.includes(scope))
          
          if (hasNonReadOnlyScope) {
            return NextResponse.json(
              { error: 'Agent manifest required for this operation' },
              { status: 403 }
            )
          }
        }

        // Validate required scopes
        if (!validateScopes(requiredScopes)) {
          return NextResponse.json(
            { error: 'Invalid scopes requested' },
            { status: 400 }
          )
        }

        // Check if manifest has required scopes
        if (manifest) {
          const manifestScopes = manifest.connectors.flatMap(conn => conn.scopes)
          const hasAllRequiredScopes = requiredScopes.every(scope => manifestScopes.includes(scope))
          
          if (!hasAllRequiredScopes) {
            return NextResponse.json(
              { error: 'Insufficient permissions' },
              { status: 403 }
            )
          }
        }

        // Call the handler
        return handler(req, { session, manifest, requiredScopes })
      } catch (error: any) {
        return NextResponse.json(
          { error: 'Permission check failed' },
          { status: 500 }
        )
      }
    }
  }
}
