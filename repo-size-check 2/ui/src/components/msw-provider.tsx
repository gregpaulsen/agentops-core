'use client';

import { useEffect } from 'react';

export function MSWProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (process.env.NEXT_PUBLIC_USE_MOCKS === 'true') {
      // Start MSW worker
      const startWorker = async () => {
        if (typeof window !== 'undefined') {
          const { worker } = await import('@/mocks/browser');
          await worker.start({
            onUnhandledRequest: 'bypass',
          });
        }
      };
      
      startWorker();
    }
  }, []);

  return <>{children}</>;
}
