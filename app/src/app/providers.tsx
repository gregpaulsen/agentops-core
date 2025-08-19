"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { api } from "@/lib/trpc";
import { httpBatchLink } from "@trpc/client";
import { ReactNode, useState } from "react";
import superjson from "superjson";

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    api.createClient({ 
      links: [httpBatchLink({ 
        url: "/api/trpc",
        transformer: superjson
      })]
    })
  );
  return (
    <api.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </api.Provider>
  );
}


