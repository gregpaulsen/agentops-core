import { router, publicProcedure } from "@/server/trpc";
import { z } from "zod";
import { searchGuides } from "@/server/youtube";

export const resourcesRouter = router({
  youtubeGuides: publicProcedure.input(z.object({ q: z.string().min(2) }))
    .query(({ input }) => searchGuides(input.q)),
});


