import 'dotenv/config';
import { createClient } from '@supabase/supabase-js';
import { StdioServerTransport, Server } from '@modelcontextprotocol/sdk/server';
import { log } from '../shared/logger';
import fs from 'fs';
import path from 'path';

const { SUPABASE_URL, SUPABASE_SERVICE_ROLE, SCHEMA_OUT_DIR = "./schema", MIGRATIONS_OUT_DIR = "./migrations" } = process.env as Record<string, string | undefined>;

if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE) {
  console.error("Missing Supabase env vars. See .env.example");
  process.exit(1);
}
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE);

function writeFileSafe(p: string, content: string) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, content, 'utf8');
  log("Wrote", p);
}

const server = new Server(
  { name: "supabase-mcp", version: "0.0.1" },
  {
    tools: {
      db_create_table: {
        description: "Create a table via SQL. (POC: developer should review SQL before running.)",
        inputSchema: {
          type: "object",
          properties: { sql: { type: "string" } },
          required: ["sql"]
        },
        handler: async ({ sql }: any) => {
          const { error } = await supabase.rpc('exec_sql', { sql });
          if (error) throw new Error(error.message);
          return { content: [{ type: "text", text: "Table created (if SQL was valid)." }] } as any;
        }
      },
      db_generate_drizzle_schema: {
        description: "Emit a Drizzle schema file (skeleton) for a table.",
        inputSchema: {
          type: "object",
          properties: {
            tableName: { type: "string" },
            columns: { type: "array", items: { type: "object", properties: { name: {type:"string"}, type: {type:"string"}, optional:{type:"boolean"} }, required:["name","type"] } }
          },
          required: ["tableName", "columns"]
        },
        handler: async ({ tableName, columns }: any) => {
          const fields = columns.map((c: any) => `  ${c.name}: ${c.type}("${c.name}")${c.optional ? "" : ".notNull()"},`).join("\n");
          const body = `import { pgTable, text, integer, uuid, timestamp, boolean } from "drizzle-orm/pg-core";
export const ${tableName} = pgTable("${tableName}", {
${fields}
});`;
          const out = path.resolve(SCHEMA_OUT_DIR!, `${tableName}.ts`);
          writeFileSafe(out, body);
          return { content: [{ type: "text", text: `Schema written to ${out}` }] } as any;
        }
      },
      db_crud_scaffold: {
        description: "Generate a tRPC router skeleton for a table.",
        inputSchema: {
          type: "object",
          properties: { tableName: { type: "string" }, routerOutDir: { type: "string" } },
          required: ["tableName", "routerOutDir"]
        },
        handler: async ({ tableName, routerOutDir }: any) => {
          const router = `import { router, publicProcedure } from "@/server/trpc";
import { db } from "@/server/db";
import { ${tableName} } from "@/server/db/schema/${tableName}";
import { z } from "zod";

export const ${tableName}Router = router({
  list: publicProcedure.query(() => db.select().from(${tableName})),
  create: publicProcedure.input(z.any()).mutation(({ input }) => db.insert(${tableName}).values(input).returning()),
});`;
          const out = path.resolve(routerOutDir, `${tableName}.ts`);
          writeFileSafe(out, router);
          return { content: [{ type: "text", text: `Router written to ${out}` }] } as any;
        }
      }
    }
  }
);

const transport = new StdioServerTransport();
server.connect(transport);


