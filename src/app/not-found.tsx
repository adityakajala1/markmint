import Link from "next/link";
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
