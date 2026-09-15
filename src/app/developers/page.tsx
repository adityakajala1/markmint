"use client";

import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import Link from "next/link";
import { Leaf } from "lucide-react";

interface Developer {
  name: string;
  role: string;
  status: string;
  avatar: string;
  github: string;
  linkedin: string;
  instagram: string;
  number: string;
  id: string;
  signature: string;
  skills: string[];
}

const developers: Developer[] = [
  {
    name: "Aditya Kajala",
    role: "Frontend Engineer",
    status: "Listening to music",
    avatar: "https://github.com/adityakajala1.png",
    github: "https://github.com/adityakajala1",
    linkedin: "https://www.linkedin.com/in/aditya-kajala-375b9b389/",
    instagram: "https://instagram.com/adipbx",
    number: "01",
    id: "MM - DEV - 01",
    signature: "Adityakajala",
    skills: ["Interface", "Motion", "Craft"],
  },
  {
    name: "Naman",
    role: "Backend Engineer",
    status: "Larping",
    avatar: "https://github.com/namanipie.png",
    github: "https://github.com/namanipie",
    linkedin: "https://www.linkedin.com/in/namannkumar",
    instagram: "https://instagram.com/nam4nn",
    number: "02",
    id: "MM - DEV - 02",
    signature: "Naman",
    skills: ["Logic", "Systems", "Intelligence"],
  }
];

function RealisticBarcode() {
  return (
    <svg viewBox="0 0 100 30" preserveAspectRatio="none" className="h-[22px] w-[120px] fill-muted-foreground/40 opacity-70">
      <rect x="0" y="0" width="2" height="30" />
      <rect x="3" y="0" width="1" height="30" />
      <rect x="5" y="0" width="3" height="30" />
      <rect x="9" y="0" width="1" height="30" />
      <rect x="11" y="0" width="2" height="30" />
      <rect x="15" y="0" width="1" height="30" />
      <rect x="18" y="0" width="4" height="30" />
      <rect x="23" y="0" width="1" height="30" />
      <rect x="25" y="0" width="2" height="30" />
      <rect x="29" y="0" width="3" height="30" />
      <rect x="33" y="0" width="1" height="30" />
      <rect x="36" y="0" width="2" height="30" />
      <rect x="39" y="0" width="1" height="30" />
      <rect x="42" y="0" width="3" height="30" />
      <rect x="47" y="0" width="2" height="30" />
      <rect x="50" y="0" width="1" height="30" />
      <rect x="53" y="0" width="2" height="30" />
      <rect x="57" y="0" width="4" height="30" />
      <rect x="62" y="0" width="1" height="30" />
      <rect x="64" y="0" width="2" height="30" />
      <rect x="68" y="0" width="1" height="30" />
      <rect x="71" y="0" width="3" height="30" />
      <rect x="75" y="0" width="1" height="30" />
      <rect x="78" y="0" width="2" height="30" />
      <rect x="81" y="0" width="1" height="30" />
      <rect x="84" y="0" width="3" height="30" />
      <rect x="89" y="0" width="1" height="30" />
      <rect x="92" y="0" width="2" height="30" />
      <rect x="95" y="0" width="1" height="30" />
      <rect x="98" y="0" width="2" height="30" />
    </svg>
  );
}

function GithubIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
  );
}
function LinkedinIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>
  );
}
function InstagramIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>
  );
}

/* Subtle botanical SVG leaves rendered inside the card background */
function CardBotanical() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-[0.04]">
      <svg viewBox="0 0 400 600" className="absolute -bottom-10 -right-10 w-[300px] h-[400px]" fill="none" stroke="currentColor" strokeWidth="0.5">
        <path d="M200 500 C180 420, 120 380, 80 300 C60 240, 100 180, 160 140 C180 120, 200 100, 200 60" />
        <path d="M200 500 C220 420, 280 380, 320 300 C340 240, 300 180, 240 140 C220 120, 200 100, 200 60" />
        <path d="M200 400 C160 360, 100 340, 60 280" />
        <path d="M200 400 C240 360, 300 340, 340 280" />
        <path d="M200 300 C170 270, 130 260, 90 220" />
        <path d="M200 300 C230 270, 270 260, 310 220" />
        <path d="M200 200 C180 180, 150 170, 120 140" />
        <path d="M200 200 C220 180, 250 170, 280 140" />
      </svg>
      <svg viewBox="0 0 400 600" className="absolute -top-20 -left-10 w-[250px] h-[350px] rotate-180" fill="none" stroke="currentColor" strokeWidth="0.5">
        <path d="M200 500 C180 420, 120 380, 80 300 C60 240, 100 180, 160 140" />
        <path d="M200 500 C220 420, 280 380, 320 300 C340 240, 300 180, 240 140" />
        <path d="M200 400 C160 360, 100 340, 60 280" />
        <path d="M200 400 C240 360, 300 340, 340 280" />
      </svg>
    </div>
  );
}

function IDCard({ dev, index }: { dev: Developer; index: number }) {
  return (
    <div className="flex flex-col items-center pb-8">
      {/* Lanyard Strap */}
      <div className="flex flex-col items-center z-10 relative">
        {/* The strap going up */}
        <div className="w-8 h-6 bg-muted rounded-t-md border-x border-t border-border/50" />
        {/* The rounded clip */}
        <div className="w-12 h-5 bg-card rounded-b-[10px] border border-border/50 -mt-[1px]" />
      </div>

      {/* Card */}
      <div
        className={`relative w-[340px] sm:w-[380px] h-fit rounded-2xl overflow-hidden -mt-1 shadow-2xl bg-card transition-colors duration-300 ${
          index === 1 ? 'border border-accent/30' : 'border border-border/50'
        }`}
      >
        {/* Botanical background pattern */}
        <CardBotanical />

        {/* Header: Logo + Number */}
        <div className="relative flex items-start justify-between px-6 pt-6 pb-2">
          <div className="flex items-center gap-2.5">
            <Leaf className="w-5 h-5 text-accent" />
            <div>
              <p className="text-[15px] font-bold text-foreground leading-none">MarkMint</p>
              <p className="text-[10px] font-bold tracking-[0.18em] uppercase text-muted-foreground mt-0.5">Developer</p>
            </div>
          </div>
          <span className="text-xl font-bold text-muted-foreground/30 mt-1">{dev.number}</span>
        </div>

        {/* Photo + Skills */}
        <div className="relative flex items-start px-6 gap-5 mt-2">
          {/* Photo */}
          <div className="relative w-[150px] h-[170px] flex-shrink-0 rounded-xl overflow-visible group">
            {/* Glow effect - triggers on hover for desktop, active for mobile */}
            <div className="absolute inset-0 bg-accent/40 rounded-xl blur-xl opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity duration-700 -z-10" />
            <div className="w-full h-full rounded-xl overflow-hidden border border-border/50 bg-background/50 shadow-lg relative z-10">
              <img
                src={dev.avatar}
                alt={dev.name}
                className="w-full h-full object-cover grayscale group-hover:grayscale-0 group-active:grayscale-0 transition-all duration-700"
              />
            </div>
          </div>

          {/* Skills */}
          <div className="flex flex-col py-2">
            <div className="flex flex-col gap-2">
              {dev.skills.map((skill) => (
                <span
                  key={skill}
                  className="text-[11px] font-bold tracking-[0.14em] uppercase text-muted-foreground"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Name + Role */}
        <div className="relative px-6 pt-5 pb-2">
          <h3 className="text-2xl font-bold text-foreground leading-tight">{dev.name}</h3>
          <p className="text-[15px] font-bold text-accent mt-1">{dev.role}</p>
          <p className="text-xs text-muted-foreground mt-1 italic">{dev.status}</p>
        </div>

        {/* Social Icons */}
        <div className="relative flex items-center gap-6 px-6 pt-3 pb-5">
          <Link href={dev.github} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`${dev.name} GitHub`}>
            <GithubIcon />
          </Link>
          <Link href={dev.linkedin} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`${dev.name} LinkedIn`}>
            <LinkedinIcon />
          </Link>
          <Link href={dev.instagram} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`${dev.name} Instagram`}>
            <InstagramIcon />
          </Link>
        </div>

        {/* Footer: Leaf & Barcode */}
        <div className="relative flex items-end justify-between px-6 py-4 border-t border-border/50">
          <div 
            className="cursor-pointer group flex items-center justify-center p-2 -ml-2 rounded-full hover:bg-accent/10 transition-colors"
            onClick={() => {
              // Secret Easter Egg Idea 
              console.log("Leaf clicked!");
            }}
          >
            <img 
              src="/secret-leaf.png" 
              alt="Secret Leaf" 
              className="w-7 h-7 opacity-80 group-hover:opacity-100 group-hover:scale-110 group-hover:rotate-12 group-active:scale-95 transition-all duration-300 dark:brightness-110" 
            />
          </div>
          <div className="flex items-end gap-2">
            <RealisticBarcode />
            <span className="text-[9px] font-mono text-muted-foreground/40 ml-1 mb-0.5">{dev.id}</span>
          </div>
        </div>

      </div>
    </div>
  );
}

export default function DevelopersPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20">
      <Navbar />

      <main className="flex-1 w-full max-w-7xl mx-auto px-6 md:px-10 pt-12 pb-32">

        <div className="flex flex-col lg:flex-row gap-16 lg:gap-8 items-start">

          {/* Left: Title Block */}
          <div className="lg:w-[30%] flex flex-col items-start pt-6">
            <p className="text-[11px] tracking-[0.15em] uppercase text-muted-foreground/60 mb-3"
               style={{ fontStyle: 'italic' }}
            >
              Built by
            </p>
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-foreground leading-[1.05] mb-6">
              The <span className="italic font-serif">Duo</span>
            </h1>
            <div className="w-8 h-[2px] bg-accent" />
          </div>

          {/* Right: ID Cards */}
          <div className="lg:w-[70%] flex flex-col sm:flex-row gap-8 sm:gap-6 items-start justify-center pt-4 pb-12">
            {developers.map((dev, idx) => (
              <IDCard key={dev.name} dev={dev} index={idx} />
            ))}
          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
}
