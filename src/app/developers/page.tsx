"use client";

import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";


interface Developer {
  name: string;
  role: string;
  avatar: string;
  status: string;
  github: string;
  linkedin: string;
  instagram: string;
}

const developers: Developer[] = [
  {
    name: "Aditya Kajala",
    role: "Frontend Engineer",
    avatar: "https://github.com/adityakajala1.png",
    status: "Listening to music",
    github: "https://github.com/adityakajala1",
    linkedin: "https://www.linkedin.com/in/aditya-kajala-375b9b389/",
    instagram: "https://instagram.com/adipbx"
  },
  {
    name: "Naman",
    role: "Backend Engineer",
    avatar: "https://github.com/namanipie.png",
    status: "Larping",
    github: "https://github.com/namanipie",
    linkedin: "https://linkedin.com/in/namankumar",
    instagram: "https://instagram.com/nam4nn"
  }
];

function DeveloperCard({ dev }: { dev: Developer }) {
  const [isAngry, setIsAngry] = useState(false);

  const handleInteraction = () => {
    setIsAngry(true);
    toast(dev.status, {
      duration: 1200,
      position: "top-center"
    });
    
    setTimeout(() => {
      setIsAngry(false);
    }, 1200);
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-8 flex flex-col items-center text-center gap-5 hover:border-accent/30 transition-colors">
      <img 
        src={dev.avatar} 
        alt={dev.name} 
        className={`w-32 h-32 rounded-full border-4 border-background shadow-lg transition-transform duration-300 cursor-pointer ${isAngry ? 'scale-125' : 'hover:scale-110'}`}
        onMouseEnter={handleInteraction}
        onClick={handleInteraction}
      />
      <div>
        <h3 className="text-xl font-bold text-foreground">{dev.name}</h3>
        <p className="text-sm font-medium text-accent mt-1">{dev.role}</p>
      </div>
      
      {/* Social Links */}
      <div className="flex items-center gap-4 mt-2">
        <Link 
          href={dev.github} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-foreground transition-colors p-2 hover:bg-accent/10 rounded-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
        </Link>
        <Link 
          href={dev.linkedin} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-foreground transition-colors p-2 hover:bg-accent/10 rounded-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
        </Link>
        <Link 
          href={dev.instagram} 
          target="_blank" 
          rel="noopener noreferrer"
          className="text-muted-foreground hover:text-foreground transition-colors p-2 hover:bg-accent/10 rounded-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-5 h-5"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
        </Link>
      </div>
    </div>
  );
}

export default function DevelopersPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20">
      <Navbar />
      
      <main className="flex-1 flex flex-col items-center justify-center w-full max-w-5xl mx-auto px-6 md:px-10 pt-8 pb-32">
        <div className="text-center mb-16">
          <p className="text-[11px] font-semibold tracking-[0.2em] uppercase text-muted-foreground mb-6">
            The Duo
          </p>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-foreground leading-[1.1] mb-8">
            <span className="text-accent">Built, designed, engineered </span>and<span className="text-accent"> maintained</span> by :
          </h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-3xl">
          {developers.map((dev) => (
            <DeveloperCard key={dev.name} dev={dev} />
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
}
