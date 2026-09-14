"use client";

import { useState } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { Send, Leaf, CornerDownLeft } from "lucide-react";

export default function MintAiPage() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [messages, setMessages] = useState<{role: 'user' | 'ai', content: string}[]>([]);

  const handleSend = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!prompt.trim()) return;
    
    setMessages([...messages, { role: 'user', content: prompt }]);
    setPrompt("");
    setIsGenerating(true);
    
    // Simulate generation time to show the skeleton
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: "I am currently analyzing the SRMIST historical paper dataset for this query. I will have the probability distribution ready for you shortly." 
      }]);
      setIsGenerating(false);
    }, 2500);
  };

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground relative overflow-hidden">
      <Navbar />
      
      <main className="flex-1 w-full max-w-4xl mx-auto px-6 md:px-10 pt-8 pb-32 flex flex-col h-full">
        
        {/* Chat History */}
        <div className="flex-1 overflow-y-auto min-h-[50vh] flex flex-col space-y-8 pb-8">
          
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 my-auto opacity-70">
              <Leaf className="w-16 h-16 text-accent mb-4" strokeWidth={1} />
              <h2 className="text-2xl font-bold">How can I help you prepare?</h2>
              <p className="text-muted-foreground max-w-md text-sm">
                Ask me to predict an upcoming paper, generate a study plan, or summarize important PYQs for your branch.
              </p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {msg.role === 'ai' && (
                  <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center shrink-0">
                    <Leaf className="w-4 h-4 text-accent" strokeWidth={2} />
                  </div>
                )}
                <div className={`px-5 py-3 rounded-2xl max-w-[80%] ${msg.role === 'user' ? 'bg-accent text-white' : 'bg-card border border-border'}`}>
                  <p className="text-sm leading-relaxed">{msg.content}</p>
                </div>
              </div>
            ))
          )}

          {/* SKELETON PULSE - Appears while generating */}
          {isGenerating && (
            <div className="flex gap-4 justify-start">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center shrink-0">
                <Leaf className="w-4 h-4 text-accent" strokeWidth={2} />
              </div>
              <div className="px-5 py-4 rounded-2xl bg-card border border-border w-full max-w-[60%] flex flex-col gap-3">
                <div className="w-3/4 h-3 bg-muted rounded-full animate-pulse" />
                <div className="w-full h-3 bg-muted rounded-full animate-pulse" />
                <div className="w-5/6 h-3 bg-muted rounded-full animate-pulse" />
              </div>
            </div>
          )}
        </div>

        {/* Chat Input */}
        <div className="mt-auto sticky bottom-8">
          <form 
            onSubmit={handleSend}
            className="relative flex items-center bg-card border border-border rounded-xl shadow-xl overflow-hidden focus-within:border-accent/50 transition-colors"
          >
            <input 
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask MintAi about your upcoming exams..."
              className="w-full bg-transparent border-none py-4 pl-4 pr-16 text-sm focus:outline-none"
              disabled={isGenerating}
            />
            <button 
              type="submit" 
              disabled={!prompt.trim() || isGenerating}
              className="absolute right-2 p-2 bg-accent/10 hover:bg-accent text-accent hover:text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <CornerDownLeft className="w-4 h-4" />
            </button>
          </form>
          <p className="text-center text-[10px] text-muted-foreground mt-3">
            MintAi can make mistakes. Always cross-check predictions with official syllabus materials.
          </p>
        </div>
      </main>
    </div>
  );
}
