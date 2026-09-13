"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { 
  BookOpen, Calendar, HelpCircle, Layers, Users, BarChart2, Hash
} from "lucide-react";
import { cn } from "@/lib/utils";
import { 
  getCourseInfo, 
  getQuestions, 
  getTopicFrequencies, 
  getMarksDistribution, 
  getHistoricalTrends, 
  getMarksPattern, 
  getHeatmapData, 
  getConfidenceGroups 
} from "@/lib/api";
import { 
  Course, 
  Question, 
  TopicFrequency, 
  MarksDistribution, 
  TrendData, 
  HeatmapData, 
  ConfidenceGroup 
} from "@/lib/types";
import { QuestionCard } from "@/components/ui/question-card";
import { TopicFrequencyChart } from "@/components/charts/topic-frequency-chart";
import { MarksDistributionChart } from "@/components/charts/marks-distribution-chart";
import { TopicHeatmap } from "@/components/charts/topic-heatmap";
import { HistoricalTrendsChart } from "@/components/charts/historical-trends-chart";
import { MarksPatternChart } from "@/components/charts/marks-pattern-chart";

type Tab = "Overview" | "Questions" | "Trends" | "Exam DNA";

export default function CoursePage() {
  const params = useParams();
  const courseId = params.id as string;
  const [activeTab, setActiveTab] = useState<Tab>("Overview");
  
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);

  // Tab Data States
  const [questions, setQuestions] = useState<Question[]>([]);
  const [topicFreq, setTopicFreq] = useState<TopicFrequency[]>([]);
  const [marksDist, setMarksDist] = useState<MarksDistribution[]>([]);
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [marksPattern, setMarksPattern] = useState<TrendData[]>([]);
  const [heatmap, setHeatmap] = useState<HeatmapData[]>([]);
  const [confidenceGroups, setConfidenceGroups] = useState<ConfidenceGroup[]>([]);
  
  const [tabLoading, setTabLoading] = useState(false);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const data = await getCourseInfo(courseId);
        setCourse(data);
      } catch (error) {
        console.error("Failed to load course", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCourse();
  }, [courseId]);

  useEffect(() => {
    const loadTabData = async () => {
      setTabLoading(true);
      try {
        if (activeTab === "Overview") {
          const [tf, md] = await Promise.all([
            getTopicFrequency(courseId),
            getMarksDistribution(courseId)
          ]);
          setTopicFreq(tf);
          setMarksDist(md);
        } else if (activeTab === "Questions") {
          const q = await getQuestions({ courseId });
          setQuestions(q.data || q as any); // Adapt to actual return type
        } else if (activeTab === "Trends") {
          const [tr, mp] = await Promise.all([
            getHistoricalTrends(courseId),
            getMarksPattern(courseId)
          ]);
          setTrends(tr);
          setMarksPattern(mp);
        } else if (activeTab === "Exam DNA") {
          const [hm, cg] = await Promise.all([
            getHeatmapData(courseId),
            getConfidenceGroups(courseId)
          ]);
          setHeatmap(hm);
          setConfidenceGroups(cg);
        }
      } catch (error) {
        console.error(`Failed to load ${activeTab} data`, error);
      } finally {
        setTabLoading(false);
      }
    };
    loadTabData();
  }, [activeTab, courseId]);

  if (loading) {
    return <div className="flex h-64 items-center justify-center text-muted-foreground">Loading course details...</div>;
  }

  if (!course) {
    return <div className="flex h-64 items-center justify-center text-destructive">Course not found.</div>;
  }

  const tabs: Tab[] = ["Overview", "Questions", "Trends", "Exam DNA"];

  return (
    <div className="container mx-auto py-8 space-y-8 px-4 sm:px-6 lg:px-8 max-w-7xl">
      {/* Header Section */}
      <div className="glass rounded-2xl p-6 sm:p-8 border border-border">
        <h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
          {course.courseName}
          <span className="text-muted-foreground text-2xl font-medium ml-3">({course.courseCode})</span>
        </h1>
        <div className="flex flex-wrap gap-3">
          <Badge icon={<Calendar className="w-4 h-4" />} text={`Semester ${course.semester}`} />
          <Badge icon={<BookOpen className="w-4 h-4" />} text={course.examType} />
          <Badge icon={<Layers className="w-4 h-4" />} text={course.academicYear} />
          <Badge icon={<Users className="w-4 h-4" />} text={course.department} />
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border flex overflow-x-auto no-scrollbar">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              "px-6 py-3 font-medium text-sm whitespace-nowrap transition-colors border-b-2",
              activeTab === tab 
                ? "border-primary text-primary bg-primary/10" 
                : "border-transparent text-muted-foreground hover:text-foreground hover:bg-secondary/50"
            )}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[500px] relative">
        <AnimatePresence mode="wait">
          {tabLoading ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 flex items-center justify-center text-muted-foreground"
            >
              Loading {activeTab}...
            </motion.div>
          ) : (
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === "Overview" && (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <StatCard title="Total Papers" value="12" icon={<BookOpen className="w-5 h-5 text-primary" />} />
                    <StatCard title="Questions" value="184" icon={<HelpCircle className="w-5 h-5 text-accent" />} />
                    <StatCard title="Core Topics" value="28" icon={<Layers className="w-5 h-5 text-success" />} />
                    <StatCard title="Prediction Confidence" value="86%" icon={<BarChart2 className="w-5 h-5 text-warning" />} />
                  </div>
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div className="glass rounded-2xl p-6 border border-border">
                      <h3 className="text-lg font-semibold mb-4">Topic Frequency</h3>
                      <div className="h-[300px]">
                        <TopicFrequencyChart data={topicFreq} />
                      </div>
                    </div>
                    <div className="glass rounded-2xl p-6 border border-border">
                      <h3 className="text-lg font-semibold mb-4">Marks Distribution</h3>
                      <div className="h-[300px]">
                        <MarksDistributionChart data={marksDist} />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "Questions" && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {questions.length > 0 ? (
                    questions.map((q) => (
                      <QuestionCard key={q.id} question={q} />
                    ))
                  ) : (
                    <div className="col-span-2 text-center text-muted-foreground py-12">No questions available.</div>
                  )}
                </div>
              )}

              {activeTab === "Trends" && (
                <div className="space-y-6">
                  <div className="glass rounded-2xl p-6 border border-border">
                    <h3 className="text-lg font-semibold mb-4">Historical Trends</h3>
                    <div className="h-[350px]">
                      <HistoricalTrendsChart data={trends} />
                    </div>
                  </div>
                  <div className="glass rounded-2xl p-6 border border-border">
                    <h3 className="text-lg font-semibold mb-4">Marks Pattern</h3>
                    <div className="h-[350px]">
                      <MarksPatternChart data={marksPattern} />
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "Exam DNA" && (
                <div className="space-y-6">
                  <div className="glass rounded-2xl p-6 border border-border">
                    <h3 className="text-lg font-semibold mb-2">Topic Heatmap</h3>
                    <p className="text-sm text-muted-foreground mb-4">Frequency of topics across years</p>
                    <div className="h-[400px]">
                      <TopicHeatmap data={heatmap} />
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold mt-8 mb-4">Prediction Confidence</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {confidenceGroups.map((group, idx) => (
                      <div 
                        key={idx} 
                        className={cn(
                          "rounded-xl p-5 border-l-4 border-r border-y border-border",
                          group.level === "High" ? "border-l-success bg-success/5" :
                          group.level === "Medium" ? "border-l-warning bg-warning/5" :
                          "border-l-destructive bg-destructive/5"
                        )}
                      >
                        <h4 className="font-semibold text-lg mb-2 flex items-center gap-2">
                          {group.level} Confidence
                        </h4>
                        <ul className="space-y-2">
                          {group.topics.map(t => (
                            <li key={t.id} className="text-sm flex justify-between">
                              <span className="text-foreground/90">{t.name}</span>
                              <span className="text-muted-foreground text-xs">{t.evidenceCount} evidences</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function Badge({ icon, text }: { icon: React.ReactNode; text: string }) {
  return (
    <div className="flex items-center gap-2 bg-secondary/50 text-secondary-foreground px-3 py-1.5 rounded-full text-sm border border-border">
      {icon}
      <span>{text}</span>
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="glass rounded-xl p-5 border border-border flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <span className="text-muted-foreground text-sm font-medium">{title}</span>
        {icon}
      </div>
      <span className="text-2xl font-bold text-foreground">{value}</span>
    </div>
  );
}
