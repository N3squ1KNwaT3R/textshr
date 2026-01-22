import type { NextConfig } from "next";

const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/session/:path*',
        destination: 'http://session_service:8000/api/session/:path*',
      },
      {
        source: '/api/text/verify',
        destination: 'http://text_service:8000/api/text/verify',
      },

      {
        source: '/api/text/text_correction',
        destination: 'http://ai_service:8000/api/v1/text/text_correction',
      },
      {
        source: '/api/text/text_summarization',
        destination: 'http://ai_service:8000/api/v1/text/text_summarization',
      },

      {
        source: '/api/text',
        destination: 'http://text_service:8000/api/text/', 
      },
      {
        source: '/api/text/',
        destination: 'http://text_service:8000/api/text/', 
      },
      {
        source: '/api/text/:path*',
        destination: 'http://text_service:8000/api/v1/text/:path*', 
      },
      {
        source: '/api/ai/:path*',
        destination: 'http://ai_service:8000/api/v1/ai/:path*',
      },
    ];
  },
  turbopack:{},
  webpack: (config: { watchOptions: { poll: number; aggregateTimeout: number; }; }) => {
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
    };
    return config;
  },
};

export default nextConfig;