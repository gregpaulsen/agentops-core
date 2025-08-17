import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Public paths that don't require authentication
const publicPaths = [
  '/auth/login',
  '/auth/callback',
  '/public',
  '/api/health',
];

// Check if path is public
function isPublicPath(pathname: string): boolean {
  return publicPaths.some(path => pathname.startsWith(path));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Allow public paths
  if (isPublicPath(pathname)) {
    return NextResponse.next();
  }
  
  // Check for authentication (simple token check for now)
  const token = request.cookies.get('auth_token')?.value || 
                request.headers.get('authorization')?.replace('Bearer ', '');
  
  // For development with mocks, allow access
  const useMocks = process.env.NEXT_PUBLIC_USE_MOCKS === 'true';
  if (useMocks) {
    return NextResponse.next();
  }
  
  // If no token, redirect to login
  if (!token) {
    const loginUrl = new URL('/auth/login', request.url);
    return NextResponse.redirect(loginUrl);
  }
  
  // Add tenant header for SSR
  const tenant = request.nextUrl.searchParams.get('tenant') || 
                 process.env.NEXT_PUBLIC_TENANT || 
                 'bigsky';
  
  const response = NextResponse.next();
  response.headers.set('X-Tenant', tenant);
  
  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
