import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/session/:path*",
        destination: "http://127.0.0.1:80/session/session/:path*",
      },
      {
        source: "/api/text/:path*",
        destination: "http://127.0.0.1:80/text/:path*/", 
      },
    ];
  },
};

export default nextConfig;