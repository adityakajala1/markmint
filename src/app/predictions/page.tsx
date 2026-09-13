"use client";

import { useEffect, useState } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { PageHeader } from "@/components/layout/page-header";
import { PredictionCard } from "@/components/ui/prediction-card";
import { getPredictions } from "@/lib/api";
import { Prediction } from "@/lib/types";
import { AlertTriangle, Loader2, RefreshCcw, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const loadPredictions = async () => {
    setLoading(true);
    setError(false);
    try {
      const data = await getPredictions();
      setPredictions(data);
    } catch (err) {
      console.error("Failed to load predictions:", err);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPredictions();
  }, []);

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />
      
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-8">
        <PageHeader 
          title="Predictions" 
          description="Evidence-backed predictions for your next exam" 
        />

        <div className="mb-8 p-4 rounded-xl glass border-l-4 border-l-warning flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-warning shrink-0 mt-0.5" />
          <p className="text-sm text-muted-foreground leading-relaxed">
            These predictions are probabilistic estimates based on historical patterns. They are not guarantees. 
            Use them as study guidance, not certainties.
          </p>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-64 rounded-2xl glass animate-pulse border border-border/50" />
            ))}
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center h-64 glass rounded-2xl border border-destructive/20 gap-4">
            <p className="text-destructive font-medium">Failed to load predictions</p>
            <button 
              onClick={loadPredictions}
              className="flex items-center gap-2 px-4 py-2 bg-destructive/10 text-destructive rounded-lg hover:bg-destructive/20 transition-colors"
            >
              <RefreshCcw className="w-4 h-4" /> Try Again
            </button>
          </div>
        ) : (
          <>
            <motion.div 
              variants={containerVariants}
              initial="hidden"
              animate="show"
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12"
            >
              {predictions.map((prediction) => (
                <motion.div key={prediction.id} variants={itemVariants}>
                  <PredictionCard prediction={prediction} />
                </motion.div>
              ))}
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass rounded-2xl p-6 border border-border/50"
            >
              <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                Analysis Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-background/50 rounded-xl border border-border/50">
                  <p className="text-sm text-muted-foreground mb-1">Source Material</p>
                  <p className="text-xl font-bold text-foreground">50+ Papers</p>
                </div>
                <div className="p-4 bg-background/50 rounded-xl border border-border/50">
                  <p className="text-sm text-muted-foreground mb-1">Time Span</p>
                  <p className="text-xl font-bold text-foreground">Last 10 Years</p>
                </div>
                <div className="p-4 bg-background/50 rounded-xl border border-border/50">
                  <p className="text-sm text-muted-foreground mb-1">Avg Confidence</p>
                  <p className="text-xl font-bold text-primary">78%</p>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
