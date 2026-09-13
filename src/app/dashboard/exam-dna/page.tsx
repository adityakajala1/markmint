"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { PageHeader } from "@/components/layout/page-header";
import { TopicHeatmap } from "@/components/charts/topic-heatmap";
import { HistoricalTrendsChart } from "@/components/charts/historical-trends-chart";
import { MarksPatternChart } from "@/components/charts/marks-pattern-chart";
import { 
  getHeatmapData, 
  getHistoricalTrends, 
  getMarksPattern, 
  getUnitWeights, 
  getConfidenceGroups 
} from "@/lib/api";
import { HeatmapData, TrendData, UnitWeight, ConfidenceGroup } from "@/lib/types";
import { cn } from "@/lib/utils";
import { BarChart3, TrendingUp, Layers, Target, Activity } from "lucide-react";

export default function ExamDNAPage() {
  const [heatmap, setHeatmap] = useState<HeatmapData[]>([]);
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [marksPattern, setMarksPattern] = useState<TrendData[]>([]);
  const [unitWeights, setUnitWeights] = useState<UnitWeight[]>([]);
  const [confidenceGroups, setConfidenceGroups] = useState<ConfidenceGroup[]>([]);
  
  const [loading, setLoading] = useState(true);

  // Assuming a generic course ID for the dashboard view or from context
  const courseId = "CS301"; 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [hm, tr, mp, uw, cg] = await Promise.all([
          getHeatmapData(courseId),
          getHistoricalTrends(courseId),
          getMarksPattern(courseId),
          getUnitWeights(courseId),
          getConfidenceGroups(courseId)
        ]);
        setHeatmap(hm);
        setTrends(tr);
        setMarksPattern(mp);
        setUnitWeights(uw);
        setConfidenceGroups(cg);
      } catch (err) {
        console.error("Failed to fetch Exam DNA data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8 px-4 max-w-7xl space-y-8 animate-pulse">
        <div className="h-20 bg-card rounded-2xl border border-border"></div>
        <div className="h-[400px] bg-card rounded-2xl border border-border"></div>
        <div className="h-[350px] bg-card rounded-2xl border border-border"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 space-y-10 px-4 sm:px-6 lg:px-8 max-w-7xl">
      <PageHeader 
        title="Exam DNA" 
        description="The complete genetic blueprint of how your course is examined" 
      />

      <motion.div 
        variants={container} 
        initial="hidden" 
        animate="show" 
        className="space-y-10"
      >
        {/* Section 1: Topic Heatmap */}
        <motion.section variants={item} className="space-y-4">
          <ChartCard 
            title="Topic Heatmap" 
            description="Frequency of topics across years"
            icon={<Activity className="w-5 h-5 text-primary" />}
          >
            <div className="h-[450px]">
              <TopicHeatmap data={heatmap} />
            </div>
          </ChartCard>
        </motion.section>

        {/* Section 2 & 3: Trends & Patterns */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.section variants={item}>
            <ChartCard 
              title="Historical Trends" 
              description="How topic frequency changes over time"
              icon={<TrendingUp className="w-5 h-5 text-accent" />}
            >
              <div className="h-[350px]">
                <HistoricalTrendsChart data={trends} />
              </div>
            </ChartCard>
          </motion.section>

          <motion.section variants={item}>
            <ChartCard 
              title="Marks Pattern" 
              description="How marks allocation changes across years"
              icon={<BarChart3 className="w-5 h-5 text-warning" />}
            >
              <div className="h-[350px]">
                <MarksPatternChart data={marksPattern} />
              </div>
            </ChartCard>
          </motion.section>
        </div>

        {/* Section 4: Unit Weights */}
        <motion.section variants={item} className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Layers className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-bold">Unit Weights</h2>
          </div>
          <div className="glass rounded-2xl p-6 border border-border space-y-6">
            {unitWeights.map(unit => (
              <div key={unit.unit} className="space-y-2">
                <div className="flex justify-between items-end">
                  <div>
                    <h4 className="font-semibold text-foreground">{unit.name} <span className="text-muted-foreground text-sm font-normal">({unit.unit})</span></h4>
                    <div className="text-xs text-muted-foreground mt-0.5">{unit.topicCount} topics analyzed</div>
                  </div>
                  <span className="font-bold text-primary">{unit.weight}%</span>
                </div>
                <div className="h-2.5 w-full bg-secondary rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${unit.weight}%` }}
                    transition={{ duration: 1, delay: 0.2 }}
                    className="h-full bg-primary rounded-full relative"
                  >
                    <div className="absolute inset-0 bg-white/20 w-full h-full animate-pulse"></div>
                  </motion.div>
                </div>
              </div>
            ))}
          </div>
        </motion.section>

        {/* Section 5: Confidence Panel */}
        <motion.section variants={item} className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-6 h-6 text-primary" />
            <h2 className="text-2xl font-bold">Prediction Confidence</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {confidenceGroups.map((group, idx) => (
              <div 
                key={idx} 
                className={cn(
                  "glass rounded-2xl p-6 border-l-4 border-r border-y border-border flex flex-col gap-4",
                  group.level === "High" ? "border-l-success bg-success/5" :
                  group.level === "Medium" ? "border-l-warning bg-warning/5" :
                  "border-l-destructive bg-destructive/5"
                )}
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-lg">{group.level} Confidence</h3>
                  <span className={cn(
                    "px-2.5 py-1 text-xs font-bold rounded-full",
                    group.level === "High" ? "bg-success/20 text-success" :
                    group.level === "Medium" ? "bg-warning/20 text-warning" :
                    "bg-destructive/20 text-destructive"
                  )}>
                    {group.topics.length} Topics
                  </span>
                </div>
                
                <div className="flex-1 space-y-3">
                  {group.topics.map(t => (
                    <div key={t.id} className="flex flex-col gap-1 pb-3 border-b border-border/50 last:border-0 last:pb-0">
                      <span className="font-medium text-sm text-foreground/90">{t.name}</span>
                      <span className="text-xs text-muted-foreground">{t.evidenceCount} supporting evidences</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </motion.section>

      </motion.div>
    </div>
  );
}

function ChartCard({ title, description, icon, children }: { title: string, description: string, icon: React.ReactNode, children: React.ReactNode }) {
  return (
    <div className="glass rounded-2xl p-6 border border-border flex flex-col gap-4 h-full">
      <div>
        <h3 className="text-xl font-bold text-foreground flex items-center gap-2">
          {icon}
          {title}
        </h3>
        <p className="text-sm text-muted-foreground mt-1">{description}</p>
      </div>
      <div className="flex-1">
        {children}
      </div>
    </div>
  );
}
