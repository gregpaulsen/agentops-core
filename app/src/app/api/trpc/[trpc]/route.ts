import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/server/routers";
export const runtime = "nodejs";
const handler = (req: Request) => fetchRequestHandler({ endpoint: "/api/trpc", req, router: appRouter });
export { handler as GET, handler as POST };


