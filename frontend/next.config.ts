import type { NextConfig } from "next";

const nextConfig = {
  async rewrites() {
    return [
      // 1. СЕСІЇ (Не чіпаємо)
      {
        source: '/api/session/:path*',
        destination: 'http://session_service:8000/api/session/:path*',
      },

      // 2. AI ЗАПИТИ (Додаємо ПЕРЕД текстом, щоб вони мали пріоритет)
      // Ми направляємо їх на ai_service:8000, як каже твій Docker
      {
        source: '/api/text/text_correction',
        destination: 'http://ai_service:8000/api/v1/text/text_correction',
      },
      {
        source: '/api/text/text_summarization',
        destination: 'http://ai_service:8000/api/v1/text/text_summarization',
      },

      // 3. ТЕКСТ АПІ (Твоя робоча логіка)
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
      // Це правило /api/ai/ на всякий випадок, якщо будеш стукати прямо в AI
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