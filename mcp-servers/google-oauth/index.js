#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import express from 'express';
import { google } from 'googleapis';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '.env.mcp') });

class GoogleOAuthMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'google-oauth-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI || 'http://127.0.0.1:8787/callback'
    );

    this.setupTools();
    this.setupExpressServer();
  }

  setupExpressServer() {
    this.app = express();
    this.app.get('/callback', async (req, res) => {
      const { code } = req.query;
      if (code) {
        try {
          const { tokens } = await this.oauth2Client.getToken(code);
          await this.saveTokens(tokens);
          res.send(`
            <html>
              <body>
                <h1>✅ OAuth Success!</h1>
                <p>Tokens saved. You can close this window.</p>
                <script>window.close();</script>
              </body>
            </html>
          `);
        } catch (error) {
          res.send(`
            <html>
              <body>
                <h1>❌ OAuth Error</h1>
                <p>${error.message}</p>
              </body>
            </html>
          `);
        }
      }
    });
  }

  async saveTokens(tokens) {
    const tokenDir = path.join(process.env.HOME || process.env.USERPROFILE, '.mcp', 'google');
    await fs.mkdir(tokenDir, { recursive: true });
    await fs.writeFile(
      path.join(tokenDir, 'tokens.json'),
      JSON.stringify(tokens, null, 2)
    );
  }

  async loadTokens() {
    try {
      const tokenPath = path.join(process.env.HOME || process.env.USERPROFILE, '.mcp', 'google', 'tokens.json');
      const data = await fs.readFile(tokenPath, 'utf8');
      return JSON.parse(data);
    } catch {
      return null;
    }
  }

  setupTools() {
    this.server.setRequestHandler(async (request) => {
      if (request.method === 'tools/call') {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'get_google_tokens':
            return this.handleGetTokens(args);
          case 'refresh_google_tokens':
            return this.handleRefreshTokens(args);
          case 'list_google_scopes':
            return this.handleListScopes(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      }
    });
  }

  async handleGetTokens(args) {
    const { scopes = ['https://www.googleapis.com/auth/userinfo.email'] } = args;
    
    // Check if we have valid tokens
    const existingTokens = await this.loadTokens();
    if (existingTokens && existingTokens.expiry_date > Date.now()) {
      return {
        content: [
          {
            type: 'text',
            text: `✅ Found valid tokens! Access token: ${existingTokens.access_token.substring(0, 20)}...`
          }
        ]
      };
    }

    // Start OAuth flow
    const authUrl = this.oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: scopes,
      prompt: 'consent'
    });

    // Start local server if not running
    if (!this.serverInstance) {
      this.serverInstance = this.app.listen(8787, () => {
        console.log('OAuth callback server running on http://127.0.0.1:8787');
      });
    }

    // Open browser
    const { exec } = await import('child_process');
    exec(`open "${authUrl}"`);

    return {
      content: [
        {
          type: 'text',
          text: `🔐 OAuth flow initiated! Please complete the authorization in your browser.\n\nAuth URL: ${authUrl}\n\nTokens will be saved to ~/.mcp/google/tokens.json`
        }
      ]
    };
  }

  async handleRefreshTokens(args) {
    const tokens = await this.loadTokens();
    if (!tokens?.refresh_token) {
      throw new Error('No refresh token available. Please run get_google_tokens first.');
    }

    this.oauth2Client.setCredentials(tokens);
    const { credentials } = await this.oauth2Client.refreshAccessToken();
    await this.saveTokens(credentials);

    return {
      content: [
        {
          type: 'text',
          text: `✅ Tokens refreshed! New access token: ${credentials.access_token.substring(0, 20)}...`
        }
      ]
    };
  }

  async handleListScopes(args) {
    const scopes = [
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/gmail.modify',
      'https://www.googleapis.com/auth/drive.readonly',
      'https://www.googleapis.com/auth/drive.file',
      'https://www.googleapis.com/auth/calendar.readonly',
      'https://www.googleapis.com/auth/calendar.events'
    ];

    return {
      content: [
        {
          type: 'text',
          text: `Available Google OAuth scopes:\n\n${scopes.map(scope => `• ${scope}`).join('\n')}`
        }
      ]
    };
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Google OAuth MCP server running...');
  }
}

const server = new GoogleOAuthMCPServer();
server.run().catch(console.error);
