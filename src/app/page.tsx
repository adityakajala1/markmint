"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { 
  Brain, 
  BarChart3, 
  GitBranch, 
  Target, 
  Calendar, 
  Dna,
  Upload,
  Cpu,
  Sparkles,
  ArrowRight
} from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";

const fadeUpVariant = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans overflow-hidden">
      <Navbar />

      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative min-h-screen flex items-center justify-center pt-20 pb-32 px-4 sm:px-6 lg:px-8">
          {/* Background decoration */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/5 rounded-full blur-3xl pointer-events-none" />
          
          <motion.div 
            className="max-w-4xl mx-auto text-center z-10"
            variants={staggerContainer}
            initial="hidden"
            animate="visible"
          >
            <motion.h1 
              variants={fadeUpVariant}
              className="text-6xl md:text-8xl font-bold tracking-tight mb-6"
            >
              Exam<span className="text-primary">DNA</span>
            </motion.h1>
            
            <motion.h2 
              variants={fadeUpVariant}
              className="text-2xl md:text-3xl text-muted-foreground mb-8 font-medium"
            >
              Reverse-engineering the way exams are made.
            </motion.h2>
            
            <motion.p 
              variants={fadeUpVariant}
              className="text-lg md:text-xl text-muted-foreground mb-12 max-w-2xl mx-auto leading-relaxed"
            >
              Analyze previous year papers, discover patterns, and predict what&apos;s coming next. Built for students who study smart.
            </motion.p>
            
            <motion.div 
              variants={fadeUpVariant}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link 
                href="/dashboard"
                className="w-full sm:w-auto px-8 py-4 bg-primary hover:bg-primary/90 text-primary-foreground rounded-full font-semibold transition-all shadow-[0_0_20px_rgba(167,139,250,0.3)] hover:shadow-[0_0_30px_rgba(167,139,250,0.5)] flex items-center justify-center gap-2"
              >
                Analyze Papers <ArrowRight size={18} />
              </Link>
              <Link 
                href="/dashboard"
                className="w-full sm:w-auto px-8 py-4 bg-transparent border border-border hover:border-muted-foreground text-foreground rounded-full font-semibold transition-all flex items-center justify-center"
              >
                View Demo
              </Link>
            </motion.div>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8 relative">
          <div className="max-w-6xl mx-auto">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.5 }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-5xl font-bold mb-6">Everything you need to decode your exams</h2>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { icon: Brain, title: "Pattern Recognition", desc: "AI-powered analysis identifies recurring patterns across years of exam papers." },
                { icon: BarChart3, title: "Topic Frequency", desc: "See exactly which topics appear most often and how marks are distributed." },
                { icon: GitBranch, title: "Question Families", desc: "Discover how questions evolve and relate to each other over time." },
                { icon: Target, title: "Smart Predictions", desc: "Evidence-backed predictions show what's likely to appear in your next exam." },
                { icon: Calendar, title: "Study Plans", desc: "Personalized study schedules based on exam patterns and your available time." },
                { icon: Dna, title: "Exam DNA", desc: "The complete genetic blueprint of how your course is examined." },
              ].map((feature, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-50px" }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  className="glass hover:glass-hover p-6 rounded-2xl border border-border bg-card/50 backdrop-blur-md transition-all group"
                >
                  <div className="w-12 h-12 rounded-xl bg-secondary flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-colors">
                    <feature.icon className="text-primary" size={24} />
                  </div>
                  <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-muted-foreground leading-relaxed">{feature.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-5xl font-bold">How it works</h2>
            </motion.div>

            <div className="relative">
              {/* Connecting line */}
              <div className="absolute left-8 md:left-[50px] top-10 bottom-10 border-l-2 border-primary/30 z-0 hidden md:block"></div>
              <div className="absolute left-8 top-10 bottom-10 border-l-2 border-primary/30 z-0 md:hidden"></div>

              <div className="space-y-12">
                {[
                  { icon: Upload, title: "Upload Papers", desc: "Upload previous year question papers in any format. Our OCR extracts every question." },
                  { icon: Cpu, title: "AI Analysis", desc: "Advanced algorithms analyze patterns, classify topics, and map question relationships." },
                  { icon: Sparkles, title: "Get Insights", desc: "Access your personalized dashboard with predictions, trends, and study recommendations." },
                ].map((step, i) => (
                  <motion.div 
                    key={i}
                    initial={{ opacity: 0, x: -30 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true, margin: "-50px" }}
                    transition={{ duration: 0.5, delay: i * 0.2 }}
                    className="relative z-10 flex flex-col md:flex-row gap-6 md:gap-10 items-start md:items-center"
                  >
                    <div className="w-16 h-16 rounded-full bg-background border-2 border-primary flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(167,139,250,0.2)]">
                      <step.icon className="text-primary" size={28} />
                    </div>
                    <div className="glass p-6 rounded-2xl flex-grow border border-border bg-card/50">
                      <h3 className="text-xl font-bold mb-2">
                        <span className="text-primary mr-2">0{i + 1}.</span> {step.title}
                      </h3>
                      <p className="text-muted-foreground">{step.desc}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Dashboard Preview Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="text-center mb-16"
            >
              <h2 className="text-3xl md:text-5xl font-bold">Powerful analytics at your fingertips</h2>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 40 }}
              whileInView={{ opacity: 1, scale: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.7, ease: "easeOut" }}
              className="glass rounded-2xl border border-border bg-card/80 backdrop-blur-xl p-4 md:p-8 shadow-2xl overflow-hidden relative"
            >
              {/* Fake Dashboard Header */}
              <div className="flex items-center justify-between border-b border-border pb-6 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 rounded-full bg-[#ef4444]" />
                  <div className="w-3 h-3 rounded-full bg-[#eab308]" />
                  <div className="w-3 h-3 rounded-full bg-[#22c55e]" />
                </div>
                <div className="text-sm text-muted-foreground font-mono">dashboard / overview</div>
              </div>

              {/* Fake Stat Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {[
                  { label: "Papers Analyzed", value: "12" },
                  { label: "Questions Extracted", value: "487" },
                  { label: "Topics Identified", value: "34" },
                  { label: "Prediction Confidence", value: "78%", color: "text-[#22c55e]" },
                ].map((stat, i) => (
                  <div key={i} className="bg-secondary/50 border border-border rounded-xl p-4">
                    <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{stat.label}</div>
                    <div className={`text-2xl font-bold ${stat.color || "text-foreground"}`}>{stat.value}</div>
                  </div>
                ))}
              </div>

              {/* Fake Charts Area */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 bg-secondary/30 border border-border rounded-xl p-6 h-64 flex flex-col justify-end gap-2 relative overflow-hidden">
                  <div className="absolute top-4 left-4 text-sm text-muted-foreground">Topic Distribution Trends</div>
                  <div className="flex items-end gap-2 w-full h-40 opacity-70">
                    {[40, 70, 45, 90, 60, 85, 30, 50, 75, 100, 65, 80].map((h, i) => (
                      <div key={i} className="flex-1 bg-gradient-to-t from-accent to-primary rounded-t-sm" style={{ height: `${h}%` }}></div>
                    ))}
                  </div>
                </div>
                
                <div className="bg-secondary/30 border border-border rounded-xl p-6 h-64 flex flex-col items-center justify-center relative">
                  <div className="absolute top-4 left-4 text-sm text-muted-foreground">Next Exam Readiness</div>
                  <div className="w-32 h-32 rounded-full border-8 border-border border-t-primary border-r-primary border-b-primary flex items-center justify-center transform -rotate-45">
                    <span className="text-2xl font-bold transform rotate-45 text-foreground">82%</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-primary/5 pointer-events-none" />
          <div className="max-w-4xl mx-auto text-center relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to decode your exams?</h2>
              <p className="text-xl text-muted-foreground mb-10">Start analyzing your papers today and study smarter.</p>
              <Link 
                href="/dashboard"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-foreground hover:bg-foreground/90 text-background rounded-full font-bold text-lg transition-all transform hover:scale-105"
              >
                Get Started <ArrowRight size={20} />
              </Link>
            </motion.div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
