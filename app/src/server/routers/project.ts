import { router, publicProcedure } from "@/server/trpc";
import { db } from "@/server/db";
import { projects } from "@/server/db/schema/projects";
import { z } from "zod";

export const projectRouter = router({
  list: publicProcedure.query(async () => db.select().from(projects)),
  create: publicProcedure.input(z.object({ orgId: z.string(), name: z.string().min(1) }))
    .mutation(async ({ input }) => db.insert(projects).values(input).returning()),
});


