import 'dotenv/config';
import { StdioServerTransport, Server } from '@modelcontextprotocol/sdk/server';
import fs from 'fs';
import path from 'path';
import { log } from '../shared/logger';

const { RIVE_ASSETS_DIR = "../app/public/rive" } = process.env as Record<string, string | undefined>;

function ensureDir(d: string) { fs.mkdirSync(d, { recursive: true }); }

const server = new Server(
  { name: "rive-mcp", version: "0.0.1" },
  {
    tools: {
      rive_list: {
        description: "List available .riv files in assets dir.",
        inputSchema: { type: "object", properties: {} },
        handler: async () => {
          const dir = path.resolve(RIVE_ASSETS_DIR!);
          ensureDir(dir);
          const files = fs.readdirSync(dir).filter(f => f.endsWith('.riv'));
          return { content: [{ type: "text", text: JSON.stringify(files, null, 2) }] } as any;
        }
      },
      rive_download: {
        description: "Placeholder to save a named .riv from a URL into assets dir.",
        inputSchema: {
          type: "object",
          properties: { name: { type: "string" }, url: { type: "string" } },
          required: ["name","url"]
        },
        handler: async ({ name, url }: any) => {
          const dir = path.resolve(RIVE_ASSETS_DIR!);
          ensureDir(dir);
          const out = path.join(dir, `${name}.riv`);
          fs.writeFileSync(out, `RIVE_PLACEHOLDER for ${name} from ${url}\n`, 'utf8');
          log("Wrote", out);
          return { content: [{ type: "text", text: `Saved placeholder to ${out}` }] } as any;
        }
      }
    }
  }
);

const transport = new StdioServerTransport();
server.connect(transport);


