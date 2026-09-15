import type { Metadata } from "next";
import { Geist, Geist_Mono, Dancing_Script } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
import { CommandPalette } from "@/components/ui/command-palette";
import { GlobalFeatures } from "@/components/ui/GlobalFeatures";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const dancingScript = Dancing_Script({
  variable: "--font-dancing",
  subsets: ["latin"],
  weight: ["400", "700"],
});

import { ThemeProvider } from "@/components/theme-provider";
import { EasterEggManager } from "@/components/ambient/EasterEggManager";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_BASE_URL || "https://markmint.com"),
  title: "MarkMint | Predict exams & track GPA for SRMIST",
  description: "MintAi predicts your CT, FT, and End Sem question papers. Calculate your GPA instantly for 40+ engineering branches.",
  openGraph: {
    title: "MarkMint | SRMIST AI Assistant",
    description: "Generate structured study plans, filter PYQs, and predict exams with MintAi.",
    url: "https://markmint.com",
    siteName: "MarkMint",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "MarkMint | SRMIST AI Assistant",
    description: "MintAi predicts your CT, FT, and End Sem question papers.",
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} ${dancingScript.variable} h-full antialiased`} suppressHydrationWarning
    >
      <body className="min-h-full flex flex-col bg-background text-foreground relative">        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
        {children}
        <Toaster
          theme="dark"
          position="bottom-right"
          toastOptions={{
            style: {
              background: "#18181b",
              border: "1px solid #27272a",
              color: "#fafafa",
            },
          }}
        />
        <EasterEggManager />
        <GlobalFeatures />
      </ThemeProvider>
      </body>
    </html>
  );
}
