"use client";

import { useState, useEffect } from "react";
import { MessageSquare, X, ArrowUp, CheckCircle, AlertCircle } from "lucide-react";

export function GlobalFeatures() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [showTopBtn, setShowTopBtn] = useState(false);
  const [showCookie, setShowCookie] = useState(false);
  
  // Contact Modal
  const [showContact, setShowContact] = useState(false);
  const [formState, setFormState] = useState<"idle" | "error" | "success">("idle");
  const [formData, setFormData] = useState({ email: "", message: "" });

  useEffect(() => {
    // UTM Tracking (#14)
    const params = new URLSearchParams(window.location.search);
    const utmSource = params.get("utm_source");
    if (utmSource) localStorage.setItem("utm_source", utmSource);

    // Cookie Banner Check (#2)
    if (!localStorage.getItem("cookie_consent")) {
      setShowCookie(true);
    }

    // Scroll Progress & Top Button (#8, #4)
    const handleScroll = () => {
      const totalScroll = document.documentElement.scrollTop;
      const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scroll = totalScroll / windowHeight;
      setScrollProgress(scroll * 100);
      setShowTopBtn(totalScroll > 300);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const acceptCookies = () => {
    localStorage.setItem("cookie_consent", "true");
    setShowCookie(false);
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Form Error State (#16)
    if (!formData.email.includes("@") || formData.message.length < 5) {
      setFormState("error");
      return;
    }
    
    // Form Success State (#15)
    setFormState("success");
    setTimeout(() => {
      setShowContact(false);
      setFormState("idle");
      setFormData({ email: "", message: "" });
    }, 2000);
  };

  return (
    <>
      {/* Scroll Progress Bar (#8) */}
      <div 
        className="fixed top-0 left-0 h-1 bg-accent z-[100] transition-all duration-150 no-print"
        style={{ width: `${scrollProgress}%` }}
      />

      {/* Floating Action Buttons */}
      <div className="fixed bottom-6 right-6 flex flex-col gap-3 z-50 no-print items-end">
        {/* Top Button (#4) */}
        <button
          onClick={scrollToTop}
          className={`p-3 bg-card border border-border rounded-md shadow-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-all ${showTopBtn ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10 pointer-events-none'}`}
          aria-label="Scroll to top"
        >
          <ArrowUp className="w-5 h-5" />
        </button>

        {/* Floating Contact (#20) */}
        <button
          onClick={() => setShowContact(true)}
          className="p-3 bg-foreground text-background rounded-md shadow-lg hover:bg-foreground/90 transition-all"
          aria-label="Open contact form"
        >
          <MessageSquare className="w-5 h-5" />
        </button>
      </div>

      {/* Cookie Banner (#2) */}
      {showCookie && (
        <div className="fixed bottom-6 left-6 max-w-sm bg-card border border-border p-4 rounded-md shadow-xl z-50 flex flex-col gap-3 no-print">
          <p className="text-sm text-muted-foreground">We use essential cookies to ensure this site functions properly. We do not track your personal data.</p>
          <div className="flex justify-end gap-3">
            <button onClick={() => setShowCookie(false)} className="text-xs font-medium hover:underline text-muted-foreground">Decline</button>
            <button onClick={acceptCookies} className="text-xs font-medium bg-foreground text-background px-3 py-1.5 rounded-md hover:bg-foreground/90">Accept</button>
          </div>
        </div>
      )}

      {/* Contact Modal (#17, #20) */}
      {showContact && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-[100] flex items-center justify-center p-4 no-print">
          <div className="bg-card border border-border rounded-md w-full max-w-md p-6 shadow-2xl relative">
            <button onClick={() => setShowContact(false)} className="absolute top-4 right-4 text-muted-foreground hover:text-foreground">
              <X className="w-5 h-5" />
            </button>
            
            <h2 className="text-xl font-bold mb-6">Contact Us</h2>
            
            {formState === "success" ? (
              <div className="flex flex-col items-center justify-center py-8 text-center gap-3">
                <CheckCircle className="w-12 h-12 text-accent" />
                <p className="font-medium text-foreground">Message sent successfully!</p>
              </div>
            ) : (
              <form onSubmit={handleContactSubmit} className="flex flex-col gap-4">
                <div>
                  <label className="text-sm font-medium mb-1 block">Email</label>
                  <input 
                    type="email" 
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium mb-1 block">Message</label>
                  <textarea 
                    rows={4}
                    value={formData.message}
                    onChange={(e) => setFormData({...formData, message: e.target.value})}
                    className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors resize-none"
                  />
                </div>
                
                {formState === "error" && (
                  <div className="flex items-center gap-2 text-red-500 text-sm bg-red-500/10 p-2 rounded-md">
                    <AlertCircle className="w-4 h-4" />
                    <span>Please provide a valid email and message.</span>
                  </div>
                )}
                
                <button type="submit" className="w-full bg-foreground text-background rounded-md py-2 text-sm font-medium hover:bg-foreground/90 transition-colors mt-2">
                  Send Message
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </>
  );
}
