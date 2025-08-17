'use client';

import { useAuth } from '@/lib/auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/components/theme-provider';
import { LogIn, Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth();
  const { branding } = useTheme();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && !loading) {
      router.push('/');
    }
  }, [isAuthenticated, loading, router]);

  const handleLogin = () => {
    login('google');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="text-center py-8">
            <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-600" />
            <p className="mt-4">Loading...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 h-12 w-12 rounded-lg bg-gradient-to-br from-green-500 to-green-700 flex items-center justify-center">
            <span className="text-white font-bold text-lg">
              {branding?.tenant_name?.charAt(0) || 'P'}
            </span>
          </div>
          <CardTitle className="text-2xl">
            Welcome to {branding?.tenant_name || 'PaulyOps'}
          </CardTitle>
          <p className="text-gray-600 mt-2">
            Sign in to access your platform
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button 
            onClick={handleLogin}
            className="w-full flex items-center justify-center space-x-2"
            size="lg"
          >
            <LogIn className="h-4 w-4" />
            <span>Sign in with Google</span>
          </Button>
          
          <div className="text-center text-sm text-gray-500">
            <p>By signing in, you agree to our terms of service</p>
            <p className="mt-1">{branding?.legal_footer}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
