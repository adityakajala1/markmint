"use client";

import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import Link from "next/link";
import { Leaf, ShieldCheck } from "lucide-react";
import { toast } from "sonner";
import { useState, useEffect, useRef } from "react";

declare global {
  interface Window {
    leafTimer?: any;
    coughAudio?: HTMLAudioElement;
    snoopAudio?: HTMLAudioElement;
  }
}

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
  const [isTapped, setIsTapped] = useState(false);
  const [tilt, setTilt] = useState({ x: 0, y: 0 });
  const [dropped, setDropped] = useState(false);
  const todayDate = new Date().toISOString().split('T')[0].replace(/-/g, '.');

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Calculate rotation (max 10 degrees)
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -10;
    const rotateY = ((x - centerX) / centerX) * 10;
    
    setTilt({ x: rotateX, y: rotateY });
  };

  const handleMouseLeave = () => {
    setTilt({ x: 0, y: 0 });
  };

  return (
    <div className={`flex flex-col items-center pb-8 perspective-[1000px] transition-all duration-1000 ease-in ${
      dropped ? 'translate-y-[150vh] rotate-[-20deg] opacity-0 pointer-events-none' : ''
    }`}>
      {/* Interactive Lanyard Clip */}
      <div 
        className="flex flex-col items-center z-20 relative cursor-pointer group transition-transform hover:-translate-y-1"
        onClick={() => {
          setDropped(true);
          toast("Badge unclipped!", { icon: "📎" });
          setTimeout(() => setDropped(false), 2500);
        }}
        title="Unclip badge"
      >
        {/* Fabric strap */}
        <div className="w-5 h-8 bg-muted-foreground/20 rounded-t-sm shadow-inner group-hover:bg-accent/30 transition-colors" />
        {/* Metal ring */}
        <div className="w-6 h-6 rounded-full border-[3px] border-border/80 bg-background -mt-2 z-20 shadow-sm group-hover:border-accent/60 transition-colors" />
      </div>

      {/* Card */}
      <div
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{
          transform: `rotateX(${tilt.x}deg) rotateY(${tilt.y}deg)`,
          transformStyle: "preserve-3d"
        }}
        className={`relative w-[340px] sm:w-[380px] h-fit rounded-[1.5rem] overflow-hidden shadow-2xl bg-card transition-transform duration-200 ease-out -mt-3 ${
          index === 1 ? 'border-[1.5px] border-accent/40 shadow-accent/10' : 'border border-border/60'
        }`}
      >
        {/* Plastic Glare Overlay */}
        <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-white/20 dark:via-white/[0.02] dark:to-white/10 pointer-events-none z-50 mix-blend-overlay" />

        {/* Botanical background pattern */}
        <CardBotanical />

        {/* Header: Logo + Number */}
        <div className="relative flex items-start justify-between px-6 pt-12 pb-2">
          <div className="flex items-center gap-2.5">
            <Leaf className="w-5 h-5 text-accent" />
            <div>
              <p className="text-[15px] font-bold text-foreground leading-none">MarkMint</p>
              <p className="text-[10px] font-bold tracking-[0.18em] uppercase text-muted-foreground mt-0.5">Access Badge</p>
            </div>
          </div>
          <span className="text-xl font-bold text-muted-foreground/30 mt-1">{dev.number}</span>
        </div>

        {/* Official Details Row */}
        <div className="px-6 flex gap-6 mt-1 mb-4">
          <div>
            <p className="text-[8px] uppercase tracking-widest text-muted-foreground/70">Issue Date</p>
            <p className="text-[10px] font-mono font-medium">{todayDate}</p>
          </div>
          <div>
            <p className="text-[8px] uppercase tracking-widest text-muted-foreground/70">Clearance</p>
            <p className="text-[10px] font-mono font-medium text-accent">LEVEL 5</p>
          </div>
          <div>
            <p className="text-[8px] uppercase tracking-widest text-muted-foreground/70">Status</p>
            <p className="text-[10px] font-mono font-medium text-green-500">ACTIVE</p>
          </div>
        </div>

        {/* Photo + Skills */}
        <div className="relative flex items-start px-6 gap-5 mt-2">
          {/* Photo */}
          <div 
            className="relative w-[130px] h-[150px] sm:w-[150px] sm:h-[170px] flex-shrink-0 rounded-xl overflow-visible group cursor-pointer"
            onClick={() => setIsTapped(!isTapped)}
          >
            {/* Glow effect */}
            <div className={`absolute inset-0 bg-accent/40 rounded-xl blur-xl transition-opacity duration-700 -z-10 ${isTapped ? 'opacity-100' : 'opacity-0 md:group-hover:opacity-100'}`} />
            <div className="w-full h-full rounded-xl overflow-hidden border-2 border-border/50 bg-background/50 shadow-inner relative z-10">
              <img
                src={dev.avatar}
                alt={dev.name}
                className={`w-full h-full object-cover transition-all duration-700 ${isTapped ? 'grayscale-0 scale-105' : 'grayscale md:group-hover:grayscale-0 md:group-hover:scale-105'}`}
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
          <h3 className="text-2xl sm:text-3xl font-bold text-foreground leading-tight tracking-tight">{dev.name}</h3>
          <p className="text-[15px] sm:text-base font-bold text-accent mt-1 uppercase tracking-wide">{dev.role}</p>
          <p className="text-xs text-muted-foreground mt-1 italic">{dev.status}</p>
        </div>

        {/* Social Icons */}
        <div className="relative flex items-center gap-6 px-6 pt-3 pb-5">
          <Link href={dev.github} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`\${dev.name} GitHub`}>
            <GithubIcon />
          </Link>
          <Link href={dev.linkedin} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`\${dev.name} LinkedIn`}>
            <LinkedinIcon />
          </Link>
          <Link href={dev.instagram} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground transition-colors" aria-label={`\${dev.name} Instagram`}>
            <InstagramIcon />
          </Link>
        </div>

        {/* Footer: Barcode */}
        <div className="relative flex justify-end px-6 py-4 border-t border-border/50 bg-muted/10">
          <div className="flex flex-col items-end">
            <RealisticBarcode />
          </div>
        </div>
      </div>
    </div>
  );
}

function FloatingLeaf() {
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const cough = new Audio("/cough.mp3");
      cough.preload = "auto";
      window.coughAudio = cough;
      
      const snoop = new Audio("/snoop.mp3");
      snoop.preload = "auto";
      window.snoopAudio = snoop;
    }
  }, []);

  const handleLeafClick = () => {
    const isHigh = document.documentElement.classList.contains('theme-high');
    if (window.leafTimer) clearTimeout(window.leafTimer);
    
    if (isHigh) {
      document.documentElement.classList.remove('theme-high');
      document.body.classList.add('smoke-clearing');
      
      if (window.coughAudio) {
        window.coughAudio.currentTime = 0;
        window.coughAudio.volume = 0.6;
        window.coughAudio.play().catch(e => console.log(e));
      } else {
        new Audio("/cough.mp3").play().catch(e => {});
      }
      toast("Too strong? Back to normal.", { icon: "😮‍💨" });
      
      setTimeout(() => document.body.classList.remove('smoke-clearing'), 2000);
    } else {
      document.documentElement.classList.add('theme-high');
      
      if (window.snoopAudio) {
        window.snoopAudio.currentTime = 0;
        window.snoopAudio.volume = 0.8;
        window.snoopAudio.play().catch(e => console.log(e));
      } else {
        new Audio("/snoop.mp3").play().catch(e => {});
      }
      toast.success("High Mode Activated 🌿", { icon: "🔥" });
      
      window.leafTimer = setTimeout(() => {
        if (document.documentElement.classList.contains('theme-high')) {
          document.documentElement.classList.remove('theme-high');
          document.body.classList.add('smoke-clearing');
          
          if (window.coughAudio) {
            window.coughAudio.currentTime = 0;
            window.coughAudio.volume = 0.6;
            window.coughAudio.play().catch(e => {});
          }
          toast("Too strong? Back to normal.", { icon: "😮‍💨" });
          
          setTimeout(() => document.body.classList.remove('smoke-clearing'), 2000);
        }
      }, 15000);
    }
  };

  return (
    <div className="floating-leaf-anim group" onClick={handleLeafClick}>
      <img 
        src="/secret-leaf.png" 
        alt="Secret Leaf" 
        className="w-10 h-10 opacity-60 hover:opacity-100 hover:scale-110 drop-shadow-lg transition-all duration-300 dark:brightness-110" 
      />
    </div>
  );
}

export default function DevelopersPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground selection:bg-accent/20">
      <FloatingLeaf />
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
