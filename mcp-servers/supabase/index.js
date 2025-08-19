#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { createClient } from '@supabase/supabase-js';
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '.env.mcp') });

class SupabaseMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'supabase-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE
    );

    this.db = drizzle(postgres(process.env.SUPABASE_URL, {
      ssl: 'require'
    }));

    this.setupTools();
  }

  setupTools() {
    this.server.setRequestHandler(async (request) => {
      if (request.method === 'tools/call') {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'db.create_table':
            return this.handleCreateTable(args);
          case 'db.generate_drizzle_schema':
            return this.handleGenerateDrizzleSchema(args);
          case 'db.apply_policies':
            return this.handleApplyPolicies(args);
          case 'db.crud_scaffold':
            return this.handleCrudScaffold(args);
          case 'db.list_tables':
            return this.handleListTables(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      }
    });
  }

  async handleCreateTable(args) {
    const { name, columns, enableRLS = true } = args;
    
    const columnDefs = columns.map(col => {
      let def = `${col.name} ${col.type}`;
      if (col.primaryKey) def += ' PRIMARY KEY';
      if (col.notNull) def += ' NOT NULL';
      if (col.default) def += ` DEFAULT ${col.default}`;
      return def;
    }).join(',\n  ');

    const sql = `
CREATE TABLE IF NOT EXISTS ${name} (
  ${columnDefs}
);

${enableRLS ? `ALTER TABLE ${name} ENABLE ROW LEVEL SECURITY;` : ''}
    `.trim();

    try {
      const { error } = await this.supabase.rpc('exec_sql', { sql });
      if (error) throw error;

      return {
        content: [
          {
            type: 'text',
            text: `✅ Table '${name}' created successfully!\n\nSQL:\n\`\`\`sql\n${sql}\n\`\`\``
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to create table: ${error.message}`);
    }
  }

  async handleGenerateDrizzleSchema(args) {
    const { tableName, outputPath = 'src/server/db/schema' } = args;
    
    // Get table info from Supabase
    const { data: columns, error } = await this.supabase
      .from('information_schema.columns')
      .select('*')
      .eq('table_name', tableName)
      .eq('table_schema', 'public');

    if (error) throw new Error(`Failed to get table info: ${error.message}`);

    const drizzleSchema = this.generateDrizzleSchema(tableName, columns);
    
    // Write to file
    const fullPath = path.join(process.cwd(), outputPath, `${tableName}.ts`);
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    await fs.writeFile(fullPath, drizzleSchema);

    return {
      content: [
        {
          type: 'text',
          text: `✅ Drizzle schema generated for '${tableName}'!\n\nFile: ${fullPath}\n\nSchema:\n\`\`\`typescript\n${drizzleSchema}\n\`\`\``
        }
      ]
    };
  }

  generateDrizzleSchema(tableName, columns) {
    const imports = [
      'import { pgTable, text, timestamp, uuid, boolean, integer, jsonb } from \'drizzle-orm/pg-core\'',
      'import { createInsertSchema, createSelectSchema } from \'drizzle-zod\'',
      'import { z } from \'zod\'',
      ''
    ].join('\n');

    const tableDef = `export const ${tableName} = pgTable('${tableName}', {
  ${columns.map(col => {
    const name = col.column_name;
    const type = this.mapPostgresType(col.data_type, col.udt_name);
    let def = `  ${name}: ${type}`;
    
    if (col.column_default) {
      def += `.default(${col.column_default})`;
    }
    if (col.is_nullable === 'NO') {
      def += '.notNull()';
    }
    
    return def;
  }).join(',\n  ')}
});`;

    const schemas = `
// Zod schemas for validation
export const insert${tableName.charAt(0).toUpperCase() + tableName.slice(1)}Schema = createInsertSchema(${tableName})
export const select${tableName.charAt(0).toUpperCase() + tableName.slice(1)}Schema = createSelectSchema(${tableName})

// Type exports
export type ${tableName.charAt(0).toUpperCase() + tableName.slice(1)} = z.infer<typeof select${tableName.charAt(0).toUpperCase() + tableName.slice(1)}Schema>
export type New${tableName.charAt(0).toUpperCase() + tableName.slice(1)} = z.infer<typeof insert${tableName.charAt(0).toUpperCase() + tableName.slice(1)}Schema>`;

    return imports + tableDef + schemas;
  }

  mapPostgresType(dataType, udtName) {
    switch (dataType) {
      case 'character varying':
      case 'text':
        return 'text';
      case 'timestamp':
        return 'timestamp';
      case 'uuid':
        return 'uuid';
      case 'boolean':
        return 'boolean';
      case 'integer':
      case 'bigint':
        return 'integer';
      case 'json':
      case 'jsonb':
        return 'jsonb';
      default:
        return 'text';
    }
  }

  async handleApplyPolicies(args) {
    const { tableName, policies } = args;
    
    const policySQLs = policies.map(policy => {
      return `
CREATE POLICY "${policy.name}" ON ${tableName}
FOR ${policy.operation || 'ALL'}
USING (${policy.condition});
      `.trim();
    });

    const sql = policySQLs.join('\n\n');

    try {
      const { error } = await this.supabase.rpc('exec_sql', { sql });
      if (error) throw error;

      return {
        content: [
          {
            type: 'text',
            text: `✅ Policies applied to '${tableName}'!\n\nSQL:\n\`\`\`sql\n${sql}\n\`\`\``
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to apply policies: ${error.message}`);
    }
  }

  async handleCrudScaffold(args) {
    const { tableName, outputPath = 'src/server/routers' } = args;
    
    const routerCode = this.generateTRPCRouter(tableName);
    
    // Write router file
    const fullPath = path.join(process.cwd(), outputPath, `${tableName}.ts`);
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    await fs.writeFile(fullPath, routerCode);

    return {
      content: [
        {
          type: 'text',
          text: `✅ tRPC router generated for '${tableName}'!\n\nFile: ${fullPath}\n\nRouter:\n\`\`\`typescript\n${routerCode}\n\`\`\``
        }
      ]
    };
  }

  generateTRPCRouter(tableName) {
    const className = tableName.charAt(0).toUpperCase() + tableName.slice(1);
    
    return `import { router, publicProcedure } from "../trpc";
import { z } from "zod";
import { db } from "../db";
import { ${tableName} } from "../db/schema/${tableName}";

export const ${tableName}Router = router({
  list: publicProcedure.query(() => 
    db.select().from(${tableName})
  ),
  
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(({ input }) => 
      db.select().from(${tableName}).where(eq(${tableName}.id, input.id))
    ),
  
  create: publicProcedure
    .input(z.object({
      // Add your input schema here
      name: z.string().min(1),
    }))
    .mutation(({ input }) => 
      db.insert(${tableName}).values(input).returning()
    ),
  
  update: publicProcedure
    .input(z.object({
      id: z.string().uuid(),
      // Add your update schema here
      name: z.string().min(1).optional(),
    }))
    .mutation(({ input }) => 
      db.update(${tableName})
        .set(input)
        .where(eq(${tableName}.id, input.id))
        .returning()
    ),
  
  delete: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(({ input }) => 
      db.delete(${tableName})
        .where(eq(${tableName}.id, input.id))
        .returning()
    ),
});`;
  }

  async handleListTables(args) {
    const { data: tables, error } = await this.supabase
      .from('information_schema.tables')
      .select('table_name')
      .eq('table_schema', 'public')
      .eq('table_type', 'BASE TABLE');

    if (error) throw new Error(`Failed to list tables: ${error.message}`);

    const tableList = tables.map(t => `• ${t.table_name}`).join('\n');

    return {
      content: [
        {
          type: 'text',
          text: `📋 Available tables:\n\n${tableList}`
        }
      ]
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Supabase MCP server running...');
  }
}

const server = new SupabaseMCPServer();
server.run().catch(console.error);
