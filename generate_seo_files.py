import os

# 1. Custom 404 Page
not_found_code = """import Link from "next/link";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

export const metadata = {
  title: "404 - Page Not Found | MarkMint",
  description: "The page you are looking for does not exist.",
};

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center text-center px-4 pt-24 pb-32">
        <h1 className="text-8xl font-black text-foreground tracking-tighter mb-4">404</h1>
        <h2 className="text-2xl font-bold mb-6">Page Not Found</h2>
        <p className="text-muted-foreground mb-8 max-w-md">
          The page you are looking for has been moved, deleted, or possibly never existed.
        </p>
        <Link 
          href="/"
          className="px-8 py-3 bg-foreground text-background font-medium rounded-md hover:bg-foreground/90 transition-colors"
        >
          Return Home
        </Link>
      </main>
      <Footer />
    </div>
  );
}
"""
with open('src/app/not-found.tsx', 'w', encoding='utf-8') as f:
    f.write(not_found_code)

# 2. robots.ts
robots_code = """import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/api/"],
    },
    sitemap: "https://markmint.com/sitemap.xml",
  };
}
"""
with open('src/app/robots.ts', 'w', encoding='utf-8') as f:
    f.write(robots_code)

# 3. sitemap.ts
sitemap_code = """import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://markmint.com";
  
  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1,
    },
    {
      url: `${baseUrl}/calculator`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${baseUrl}/mintai`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.9,
    },
    {
      url: `${baseUrl}/developers`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
  ];
}
"""
with open('src/app/sitemap.ts', 'w', encoding='utf-8') as f:
    f.write(sitemap_code)

# 4. Open Graph Image (Dynamic)
og_code = """import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "MarkMint";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#0A0A0A",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "#F3F0E8",
        }}
      >
        <div style={{ fontSize: 120, fontWeight: 900, letterSpacing: "-0.05em", display: "flex" }}>
          MarkMint
        </div>
        <div style={{ fontSize: 40, marginTop: 20, color: "#a1a1aa", display: "flex" }}>
          SRMIST AI & GPA Tracker
        </div>
      </div>
    ),
    { ...size }
  );
}
"""
with open('src/app/opengraph-image.tsx', 'w', encoding='utf-8') as f:
    f.write(og_code)

