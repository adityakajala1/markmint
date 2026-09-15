"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { toast } from "sonner";

export function HangingLamp() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "dark" ? "light" : "dark";
    setTheme(newTheme);
    
    if (newTheme === "dark") {
      toast("Switched to Aditya", { duration: 1000, style: { fontSize: "13px", padding: "8px 14px", minHeight: "36px", width: "fit-content", marginLeft: "auto" } });
    } else {
      toast("Switched to Naman", { duration: 1000, style: { fontSize: "13px", padding: "8px 14px", minHeight: "36px", width: "fit-content", marginLeft: "auto" } });
    }
  };

  if (!mounted) return <div className="w-[28px] h-[40px] ml-2" />;

  return (
    <div 
      className="relative flex flex-col items-center justify-center cursor-pointer group"
      onClick={toggleTheme}
      title="Toggle Theme"
    >
      {/* SVG Vintage Wall Lamp - Scaled down for Navbar */}
      <svg 
        width="28" 
        height="40" 
        viewBox="0 0 140 200" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg" 
        className="transform origin-center transition-transform duration-300 group-hover:scale-110 group-active:scale-95"
      >
        {/* Wall Mount Plate */}
        <rect x="130" y="10" width="10" height="120" rx="2" fill="currentColor" className="text-[#123327] dark:text-[#E9E8E1]/20" />
        
        {/* Main Ornate Bracket */}
        <path 
          d="M 130 25 C 70 25, 50 60, 50 100 C 50 120, 80 130, 100 110 C 110 100, 105 85, 95 85" 
          stroke="currentColor" 
          strokeWidth="6" 
          strokeLinecap="round" 
          fill="none"
          className="text-[#123327] dark:text-[#E9E8E1]/20"
        />
        {/* Secondary Bracket Swirl */}
        <path 
          d="M 130 80 C 100 80, 90 100, 100 120 C 110 130, 125 125, 125 110" 
          stroke="currentColor" 
          strokeWidth="3" 
          strokeLinecap="round" 
          fill="none"
          className="text-[#123327] dark:text-[#E9E8E1]/20"
        />
        
        {/* Lamp Connector */}
        <line x1="50" y1="100" x2="50" y2="115" stroke="currentColor" strokeWidth="4" className="text-[#123327] dark:text-[#E9E8E1]/20" />
        
        {/* Lantern Cap */}
        <path d="M 25 130 L 75 130 L 60 115 L 40 115 Z" fill="currentColor" className="text-[#0B1110] dark:text-[#1A2421]" />
        <path d="M 20 135 L 80 135 L 75 130 L 25 130 Z" fill="currentColor" className="text-[#123327] dark:text-[#2A3431]" />
        
        {/* Lantern Glass Body */}
        <path d="M 25 135 L 75 135 L 65 180 L 35 180 Z" fill="currentColor" className="text-[#F3F0E8] dark:text-[#F3F0E8]/10" />
        {/* Glass Panes / Frame */}
        <path d="M 32 135 L 42 180 M 68 135 L 58 180" stroke="currentColor" strokeWidth="2" className="text-[#123327] dark:text-[#E9E8E1]/40" />
        
        {/* Lantern Bottom */}
        <path d="M 35 180 L 65 180 L 60 190 L 40 190 Z" fill="currentColor" className="text-[#0B1110] dark:text-[#1A2421]" />
        <circle cx="50" cy="195" r="4" fill="currentColor" className="text-[#123327] dark:text-[#2A3431]" />
      </svg>
      
      {/* Dynamic Glow Effect - Scaled Down */}
      <div className="absolute top-[65%] right-[50%] translate-x-1/2 w-4 h-4 bg-amber-500/40 dark:bg-amber-100/30 rounded-full blur-md pointer-events-none transition-colors duration-500" />
    </div>
  );
}