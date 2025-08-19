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

class FigmaMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'figma-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.figmaToken = process.env.FIGMA_PERSONAL_TOKEN;
    this.fileKey = process.env.FIGMA_FILE_KEY;
    this.baseURL = 'https://api.figma.com/v1';

    this.setupTools();
  }

  setupTools() {
    this.server.setRequestHandler(async (request) => {
      if (request.method === 'tools/call') {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'figma.pull_tokens':
            return this.handlePullTokens(args);
          case 'figma.component_to_react':
            return this.handleComponentToReact(args);
          case 'figma.assets.download':
            return this.handleDownloadAssets(args);
          case 'figma.list_components':
            return this.handleListComponents(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      }
    });
  }

  async makeFigmaRequest(endpoint) {
    const response = await axios.get(`${this.baseURL}${endpoint}`, {
      headers: {
        'X-Figma-Token': this.figmaToken
      }
    });
    return response.data;
  }

  async handlePullTokens(args) {
    const { outputPath = 'tailwind.config.ts' } = args;
    
    try {
      // Get file data
      const fileData = await this.makeFigmaRequest(`/files/${this.fileKey}`);
      
      // Extract design tokens
      const tokens = this.extractDesignTokens(fileData);
      
      // Generate Tailwind config
      const tailwindConfig = this.generateTailwindConfig(tokens);
      
      // Write to file
      const fullPath = path.join(process.cwd(), outputPath);
      await fs.writeFile(fullPath, tailwindConfig);

      return {
        content: [
          {
            type: 'text',
            text: `✅ Design tokens pulled and saved to ${outputPath}!\n\nTokens found:\n${JSON.stringify(tokens, null, 2)}\n\nTailwind config:\n\`\`\`typescript\n${tailwindConfig}\n\`\`\``
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to pull tokens: ${error.message}`);
    }
  }

  extractDesignTokens(fileData) {
    const tokens = {
      colors: {},
      spacing: {},
      typography: {}
    };

    // Extract colors from styles
    if (fileData.styles) {
      Object.values(fileData.styles).forEach(style => {
        if (style.styleType === 'FILL') {
          tokens.colors[style.name] = this.extractColorValue(style);
        }
      });
    }

    // Extract from document
    this.extractTokensFromNode(fileData.document, tokens);

    return tokens;
  }

  extractTokensFromNode(node, tokens) {
    if (node.type === 'RECTANGLE' && node.fills) {
      const color = this.extractColorValue(node.fills[0]);
      if (color) {
        tokens.colors[node.name] = color;
      }
    }

    if (node.type === 'TEXT' && node.style) {
      tokens.typography[node.name] = {
        fontSize: node.style.fontSize,
        fontWeight: node.style.fontWeight,
        fontFamily: node.style.fontFamily
      };
    }

    if (node.children) {
      node.children.forEach(child => this.extractTokensFromNode(child, tokens));
    }
  }

  extractColorValue(fill) {
    if (fill.type === 'SOLID' && fill.color) {
      const { r, g, b } = fill.color;
      return `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`;
    }
    return null;
  }

  generateTailwindConfig(tokens) {
    return `import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ...${JSON.stringify(tokens.colors, null, 8)}
      },
      spacing: {
        ...${JSON.stringify(tokens.spacing, null, 8)}
      },
      fontFamily: {
        ...${JSON.stringify(tokens.typography, null, 8)}
      }
    },
  },
  plugins: [],
}

export default config`;
  }

  async handleComponentToReact(args) {
    const { componentName, outputPath = 'src/components' } = args;
    
    try {
      // Get component data
      const componentData = await this.makeFigmaRequest(`/files/${this.fileKey}/components`);
      
      // Find the component
      const component = Object.values(componentData.meta.components).find(
        comp => comp.name === componentName
      );
      
      if (!component) {
        throw new Error(`Component '${componentName}' not found`);
      }

      // Generate React component
      const reactComponent = this.generateReactComponent(component, componentName);
      
      // Write to file
      const fullPath = path.join(process.cwd(), outputPath, `${componentName}.tsx`);
      await fs.mkdir(path.dirname(fullPath), { recursive: true });
      await fs.writeFile(fullPath, reactComponent);

      return {
        content: [
          {
            type: 'text',
            text: `✅ React component generated for '${componentName}'!\n\nFile: ${fullPath}\n\nComponent:\n\`\`\`tsx\n${reactComponent}\n\`\`\``
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to generate React component: ${error.message}`);
    }
  }

  generateReactComponent(component, name) {
    const className = name.replace(/[^a-zA-Z0-9]/g, '');
    
    return `import React from 'react';
import { cn } from '@/lib/utils';

interface ${className}Props {
  className?: string;
  children?: React.ReactNode;
}

export function ${className}({ className, children, ...props }: ${className}Props) {
  return (
    <div 
      className={cn(
        // Add your Tailwind classes here based on Figma design
        "flex items-center justify-center",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export default ${className};`;
  }

  async handleDownloadAssets(args) {
    const { selection, outputPath = 'public/icons' } = args;
    
    try {
      // Get image URLs
      const imageData = await this.makeFigmaRequest(
        `/images/${this.fileKey}?ids=${selection}&format=svg`
      );
      
      const downloads = [];
      
      for (const [id, url] of Object.entries(imageData.images)) {
        if (url) {
          const response = await axios.get(url, { responseType: 'arraybuffer' });
          const fileName = `${id}.svg`;
          const fullPath = path.join(process.cwd(), outputPath, fileName);
          
          await fs.mkdir(path.dirname(fullPath), { recursive: true });
          await fs.writeFile(fullPath, response.data);
          
          downloads.push(fileName);
        }
      }

      return {
        content: [
          {
            type: 'text',
            text: `✅ Assets downloaded to ${outputPath}!\n\nDownloaded files:\n${downloads.map(f => `• ${f}`).join('\n')}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to download assets: ${error.message}`);
    }
  }

  async handleListComponents(args) {
    try {
      const componentData = await this.makeFigmaRequest(`/files/${this.fileKey}/components`);
      
      const components = Object.values(componentData.meta.components).map(comp => 
        `• ${comp.name} (${comp.key})`
      );

      return {
        content: [
          {
            type: 'text',
            text: `📋 Available components:\n\n${components.join('\n')}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to list components: ${error.message}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Figma MCP server running...');
  }
}

const server = new FigmaMCPServer();
server.run().catch(console.error);
