import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      // Figma MCP will append token sync notes here
    },
  },
  plugins: [],
};
export default config;


