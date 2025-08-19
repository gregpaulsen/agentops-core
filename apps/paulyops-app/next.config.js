/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@paulyops/db', '@paulyops/core']
  },
  transpilePackages: ['@paulyops/ui', '@paulyops/db', '@paulyops/core']
}

module.exports = nextConfig
