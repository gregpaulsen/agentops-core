#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import axios from 'axios';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(__dirname, '.env.mcp') });

class RiveMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'rive-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.riveToken = process.env.RIVE_API_TOKEN;
    this.baseURL = 'https://api.rive.app/v1';

    this.setupTools();
  }

  setupTools() {
    this.server.setRequestHandler(async (request) => {
      if (request.method === 'tools/call') {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'rive.list':
            return this.handleList(args);
          case 'rive.download':
            return this.handleDownload(args);
          case 'rive.search':
            return this.handleSearch(args);
          case 'rive.list_local':
            return this.handleListLocal(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      }
    });
  }

  async makeRiveRequest(endpoint, params = {}) {
    const headers = {};
    if (this.riveToken) {
      headers['Authorization'] = `Bearer ${this.riveToken}`;
    }

    const response = await axios.get(`${this.baseURL}${endpoint}`, {
      headers,
      params
    });
    return response.data;
  }

  async handleList(args) {
    const { tag, limit = 20 } = args;
    
    try {
      const params = { limit };
      if (tag) params.tag = tag;

      const data = await this.makeRiveRequest('/assets', params);
      
      const assets = data.assets?.map(asset => 
        `• ${asset.name} (${asset.id}) - ${asset.tags?.join(', ') || 'No tags'}`
      ) || [];

      return {
        content: [
          {
            type: 'text',
            text: `📋 Rive assets${tag ? ` with tag '${tag}'` : ''}:\n\n${assets.join('\n')}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to list Rive assets: ${error.message}`);
    }
  }

  async handleDownload(args) {
    const { name, outputPath = 'public/rive' } = args;
    
    try {
      // First, search for the asset
      const searchData = await this.makeRiveRequest('/assets', { 
        search: name,
        limit: 1 
      });
      
      if (!searchData.assets || searchData.assets.length === 0) {
        throw new Error(`Asset '${name}' not found`);
      }

      const asset = searchData.assets[0];
      
      // Download the .riv file
      const response = await axios.get(asset.downloadUrl, {
        responseType: 'arraybuffer'
      });
      
      const fileName = `${asset.name.replace(/[^a-zA-Z0-9]/g, '_')}.riv`;
      const fullPath = path.join(process.cwd(), outputPath, fileName);
      
      await fs.mkdir(path.dirname(fullPath), { recursive: true });
      await fs.writeFile(fullPath, response.data);

      return {
        content: [
          {
            type: 'text',
            text: `✅ Rive asset downloaded: ${fileName}\n\nFile: ${fullPath}\n\nAsset info:\n• Name: ${asset.name}\n• ID: ${asset.id}\n• Tags: ${asset.tags?.join(', ') || 'None'}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to download Rive asset: ${error.message}`);
    }
  }

  async handleSearch(args) {
    const { query, limit = 10 } = args;
    
    try {
      const data = await this.makeRiveRequest('/assets', { 
        search: query,
        limit 
      });
      
      const results = data.assets?.map(asset => 
        `• ${asset.name} (${asset.id}) - ${asset.description || 'No description'}`
      ) || [];

      return {
        content: [
          {
            type: 'text',
            text: `🔍 Search results for '${query}':\n\n${results.join('\n')}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to search Rive assets: ${error.message}`);
    }
  }

  async handleListLocal(args) {
    const { assetsPath = 'public/rive' } = args;
    
    try {
      const fullPath = path.join(process.cwd(), assetsPath);
      
      try {
        const files = await fs.readdir(fullPath);
        const riveFiles = files.filter(file => file.endsWith('.riv'));
        
        if (riveFiles.length === 0) {
          return {
            content: [
              {
                type: 'text',
                text: `📁 No .riv files found in ${assetsPath}`
              }
            ]
          };
        }

        const fileList = riveFiles.map(file => `• ${file}`).join('\n');

        return {
          content: [
            {
              type: 'text',
              text: `📁 Local Rive assets in ${assetsPath}:\n\n${fileList}`
            }
          ]
        };
      } catch (error) {
        if (error.code === 'ENOENT') {
          return {
            content: [
              {
                type: 'text',
                text: `📁 Directory ${assetsPath} does not exist`
              }
            ]
          };
        }
        throw error;
      }
    } catch (error) {
      throw new Error(`Failed to list local Rive assets: ${error.message}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Rive MCP server running...');
  }
}

const server = new RiveMCPServer();
server.run().catch(console.error);
