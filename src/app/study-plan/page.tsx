"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { PageHeader } from "@/components/layout/page-header";
import { TimelineCard } from "@/components/ui/timeline-card";
import { getStudyPlan } from "@/lib/api";
import { StudyPlan } from "@/lib/types";
import { Calendar, Target, Zap, Lightbulb, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

export default function StudyPlanPage() {
  const [days, setDays] = useState(14);
  const [targetMarks, setTargetMarks] = useState(80);
  const [mastery, setMastery] = useState(40);
  
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [loading, setLoading] = useState(true);

  const loadPlan = async () => {
    setLoading(true);
    try {
      // In a real app, you would pass these parameters to the API
      const data = await getStudyPlan();
      setPlan(data);
    } catch (err) {
      console.error("Failed to load study plan:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlan();
  }, []); // Load initial plan

  const handleGenerate = () => {
    loadPlan();
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />
      
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8 space-y-8">
        <PageHeader 
          title="Study Plan" 
          description="AI-generated study schedule based on exam patterns" 
        />

        {/* Configuration Section */}
        <div className="glass rounded-2xl p-6 border border-border/50">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Zap className="w-5 h-5 text-accent" /> Configure Your Plan
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-sm font-medium text-foreground flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-muted-foreground" /> Time Available
                </label>
                <span className="text-sm text-primary font-bold">{days} days</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="30" 
                value={days}
                onChange={(e) => setDays(parseInt(e.target.value))}
                className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-sm font-medium text-foreground flex items-center gap-2">
                  <Target className="w-4 h-4 text-muted-foreground" /> Target Marks
                </label>
                <span className="text-sm text-accent font-bold">{targetMarks} marks</span>
              </div>
              <input 
                type="range" 
                min="40" 
                max="100" 
                value={targetMarks}
                onChange={(e) => setTargetMarks(parseInt(e.target.value))}
                className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-sm font-medium text-foreground flex items-center gap-2">
                  <Zap className="w-4 h-4 text-muted-foreground" /> Current Mastery
                </label>
                <span className="text-sm text-success font-bold">{mastery}%</span>
              </div>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={mastery}
                onChange={(e) => setMastery(parseInt(e.target.value))}
                className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button 
              onClick={handleGenerate}
              disabled={loading}
              className="bg-primary text-primary-foreground font-medium rounded-xl px-6 py-3 hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading && <Loader2 className="w-4 h-4 animate-spin" />}
              Generate Plan
            </button>
          </div>
        </div>

        {/* Plan Output */}
        {loading && !plan ? (
          <div className="flex justify-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        ) : plan ? (
          <div className="space-y-8">
            <div className="flex flex-wrap gap-4 p-4 glass rounded-xl border border-border/50 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">Duration:</span>
                <span className="font-semibold">{plan.days.length} days</span>
              </div>
              <div className="w-px h-4 bg-border hidden sm:block"></div>
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">Total Study Time:</span>
                <span className="font-semibold">
                  {plan.days.reduce((acc, day) => acc + day.topics.reduce((sum, topic) => sum + topic.estimatedMinutes, 0), 0) / 60} hours
                </span>
              </div>
              <div className="w-px h-4 bg-border hidden sm:block"></div>
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground">Topics Covered:</span>
                <span className="font-semibold">
                  {plan.days.reduce((acc, day) => acc + day.topics.length, 0)} topics
                </span>
              </div>
            </div>

            <motion.div 
              initial="hidden"
              animate="show"
              variants={{
                hidden: { opacity: 0 },
                show: { opacity: 1, transition: { staggerChildren: 0.1 } }
              }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {plan.days.map((day) => (
                <motion.div 
                  key={day.dayNumber}
                  variants={{
                    hidden: { opacity: 0, scale: 0.95 },
                    show: { opacity: 1, scale: 1, transition: { type: "spring", stiffness: 300, damping: 24 } }
                  }}
                >
                  <TimelineCard day={day} />
                </motion.div>
              ))}
            </motion.div>

            {plan.recommendations.length > 0 && (
              <div className="glass rounded-2xl p-6 border border-border/50">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-warning" /> 
                  Recommendations
                </h3>
                <ul className="space-y-3">
                  {plan.recommendations.map((rec, index) => (
                    <li key={index} className="flex items-start gap-3 p-3 rounded-lg bg-background/50 border border-border/30">
                      <Lightbulb className="w-4 h-4 text-warning shrink-0 mt-0.5" />
                      <span className="text-sm text-foreground">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
