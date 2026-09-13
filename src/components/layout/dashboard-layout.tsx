"use client";

import { useState } from "react";
import { Navbar } from "./navbar";
import { Sidebar } from "./sidebar";
import { MobileDrawer } from "./mobile-drawer";
import { Footer } from "./footer";

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <Navbar onMenuClick={() => setIsMobileMenuOpen(true)} />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        
        <main className="flex-1 overflow-y-auto flex flex-col">
          <div className="container mx-auto p-6 max-w-7xl flex-1">
            {children}
          </div>
          <Footer />
        </main>
      </div>

      <MobileDrawer 
        isOpen={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)} 
      />
    </div>
  );
}
