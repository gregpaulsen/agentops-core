import 'dotenv/config';
import { StdioServerTransport, Server } from '@modelcontextprotocol/sdk/server';
import { log } from '../shared/logger';
import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';

const { FIGMA_PERSONAL_TOKEN, FIGMA_FILE_KEY, TAILWIND_CONFIG_PATH = "../app/tailwind.config.ts", COMPONENTS_OUT_DIR = "../app/src/components" } = process.env as Record<string, string | undefined>;

if (!FIGMA_PERSONAL_TOKEN || !FIGMA_FILE_KEY) {
  console.error("Missing Figma env vars. See .env.example");
  process.exit(1);
}

async function figmaGet(route: string) {
  const r = await fetch(`https://api.figma.com/v1/${route}`, {
    headers: { 'X-Figma-Token': FIGMA_PERSONAL_TOKEN! }
  });
  if (!r.ok) throw new Error(`Figma ${route} failed: ${r.status}`);
  return r.json();
}

function writeFileSafe(p: string, content: string) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, content, 'utf8');
  log("Wrote", p);
}

const server = new Server(
  { name: "figma-mcp", version: "0.0.1" },
  {
    tools: {
      figma_pull_tokens: {
        description: "POC: Pulls file metadata; in a real impl, map tokens → Tailwind config.",
        inputSchema: { type: "object", properties: {} },
        handler: async () => {
          const data = await figmaGet(`files/${FIGMA_FILE_KEY}`);
          const out = path.resolve(TAILWIND_CONFIG_PATH!);
          const note = `\n// NOTE: tokens sync placeholder at ${new Date().toISOString()}\n`;
          fs.appendFileSync(out, note);
          return { content: [{ type: "text", text: "Appended token sync note to tailwind config (placeholder)." }] } as any;
        }
      },
      figma_component_to_react: {
        description: "Generate a minimal React component file from a named component (placeholder).",
        inputSchema: {
          type: "object",
          properties: { name: { type: "string" } },
          required: ["name"]
        },
        handler: async ({ name }: any) => {
          const body = `import React from 'react';
export default function ${name.replace(/[^A-Za-z0-9]/g,'')}(props: React.HTMLAttributes<HTMLDivElement>) {
  return <div {...props}>${name} component placeholder</div>;
}`;
          const out = path.resolve(COMPONENTS_OUT_DIR!, `${name}.tsx`);
          writeFileSafe(out, body);
          return { content: [{ type: "text", text: `Component written to ${out}` }] } as any;
        }
      }
    }
  }
);

const transport = new StdioServerTransport();
server.connect(transport);


