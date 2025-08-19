import 'dotenv/config';
import express from 'express';
import open from 'open';
import fetch from 'node-fetch';
import { StdioServerTransport, Server } from '@modelcontextprotocol/sdk/server';
import { log } from '../shared/logger';

const {
  GOOGLE_CLIENT_ID,
  GOOGLE_CLIENT_SECRET,
  GOOGLE_REDIRECT_URI,
  GOOGLE_SCOPES = 'https://www.googleapis.com/auth/userinfo.email'
} = process.env as Record<string, string | undefined>;

if (!GOOGLE_CLIENT_ID || !GOOGLE_CLIENT_SECRET || !GOOGLE_REDIRECT_URI) {
  console.error("Missing Google OAuth env vars. See .env.example");
  process.exit(1);
}

const app = express();
const PORT = 8787;
let lastToken: any = null;

app.get('/callback', async (req, res) => {
  const code = req.query.code as string;
  if (!code) return res.status(400).send("Missing code");
  try {
    const body = new URLSearchParams({
      code,
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      redirect_uri: GOOGLE_REDIRECT_URI,
      grant_type: 'authorization_code'
    });
    const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', body });
    const json = await r.json();
    lastToken = json;
    res.send(`<pre>Tokens received. You can close this window.</pre>`);
    log("Google tokens acquired.");
  } catch (e: any) {
    console.error(e);
    res.status(500).send("Auth exchange failed");
  }
});

app.listen(PORT, () => log(`OAuth callback listening on ${PORT}`));

const server = new Server(
  {
    name: "google-oauth-mcp",
    version: "0.0.1"
  },
  {
    tools: {
      get_google_tokens: {
        description: "Launch Google OAuth, request scopes, return access/refresh tokens.",
        inputSchema: {
          type: "object",
          properties: {
            scopes: { type: "string", description: "Space-separated scopes (optional)" }
          }
        },
        handler: async (input: any) => {
          const scopes = input?.scopes || GOOGLE_SCOPES;
          const params = new URLSearchParams({
            client_id: GOOGLE_CLIENT_ID!,
            redirect_uri: GOOGLE_REDIRECT_URI!,
            response_type: 'code',
            access_type: 'offline',
            prompt: 'consent',
            scope: scopes as string
          });
          const url = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
          await open(url);
          const waitFor = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
          for (let i = 0; i < 120; i++) {
            if (lastToken) break;
            await waitFor(500);
          }
          if (!lastToken) throw new Error("No token received yet. Complete consent in browser.");
          return { content: [{ type: "text", text: JSON.stringify(lastToken, null, 2) }] } as any;
        }
      }
    }
  }
);

const transport = new StdioServerTransport();
server.connect(transport);


