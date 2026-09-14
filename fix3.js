const fs = require('fs');
const code = "use client";
import { useEffect } from "react";
import { toast } from "sonner";

export function EasterEggManager() {
  useEffect(() => {
    // 1. Dev Console Secret
    console.log(
      "%c🔍 ExamScope",
      "color: #E91E63; font-size: 32px; font-weight: bold; text-shadow: 2px 2px 0 #000;"
    );
    console.log(
      "%cHello fellow dev! 👨‍💻 If you're looking for paper leaks in the source code, nice try. Now close this and go study!",
      "color: #A1A1AA; font-size: 14px;"
    );

    // 2. Secret Keyword / Konami
    let keyBuffer = "";
    const secret = "srmist";
    
    const handleKeyDown = (e) => {
      // Ignore if typing in an input field
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      keyBuffer += e.key.toLowerCase();
      if (keyBuffer.length > secret.length) {
        keyBuffer = keyBuffer.slice(-secret.length);
      }
      
      if (keyBuffer === secret) {
        toast("🌪️ Do a barrel roll!", { duration: 3000 });
        
        // Barrel roll animation
        document.body.style.transition = "transform 1s ease-in-out";
        document.body.style.transform = "rotate(360deg)";
        
        setTimeout(() => {
          // Instantly reset rotation without animating back
          document.body.style.transition = "none";
          document.body.style.transform = "none";
        }, 1000);
        
        keyBuffer = ""; // Reset
      }
    };
    
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return null;
}
;
fs.writeFileSync('src/components/ambient/EasterEggManager.tsx', code);
