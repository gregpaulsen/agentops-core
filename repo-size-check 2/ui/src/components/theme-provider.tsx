'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { useBranding } from '@/lib/query';
import { loadTheme, applyTheme, type ThemeContext } from '@/lib/theme';
import { Branding } from '@/lib/schemas';

const ThemeContext = createContext<ThemeContext>({
  branding: null,
  loading: true,
  error: null,
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [themeState, setThemeState] = useState<ThemeContext>({
    branding: null,
    loading: true,
    error: null,
  });

  const { data: branding, isLoading, error } = useBranding();

  useEffect(() => {
    if (branding) {
      applyTheme(branding);
      setThemeState({
        branding,
        loading: false,
        error: null,
      });
    } else if (error) {
      setThemeState({
        branding: null,
        loading: false,
        error: error.message,
      });
    } else if (!isLoading) {
      setThemeState({
        branding: null,
        loading: false,
        error: null,
      });
    }
  }, [branding, isLoading, error]);

  return (
    <ThemeContext.Provider value={themeState}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
