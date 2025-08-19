"use client";
import { api } from "@/lib/trpc";
import { FadeIn } from "@/components/anim/FadeIn";
import { Loader } from "@/components/Loader";

export default function Home() {
  const { data, isLoading } = api.project.list.useQuery();

  if (isLoading) return <div className="p-6"><Loader /></div>;

  return (
    <div className="p-6 space-y-4">
      <FadeIn>
        <h1 className="text-2xl font-semibold">PaulyOps Starter</h1>
        <p className="text-sm opacity-70">tRPC + Drizzle + React Query wired up.</p>
      </FadeIn>
      <pre className="bg-black/5 p-4 rounded">{JSON.stringify(data ?? [], null, 2)}</pre>
    </div>
  );
}


