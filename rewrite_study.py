import re

code = """\"use client\";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { PageHeader } from "@/components/layout/page-header";
import { getCourses, getStudyPlan } from "@/lib/api";
import { BackendCourse } from "@/lib/types";
import { BookOpen, Target, Zap, Clock, ShieldCheck, Database, Loader2, AlertCircle, FileText, Upload, GraduationCap } from "lucide-react";
import { motion } from "framer-motion";

export default function StudyIntelligencePage() {
  const [courses, setCourses] = useState<BackendCourse[]>([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [loading, setLoading] = useState(false);
  const [studyData, setStudyData] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getCourses().then((data) => {
      const courseList = Array.isArray(data) ? data : (data.items || data.courses || []);
      setCourses(courseList);
    }).catch(err => {
      console.error("Failed to load courses", err);
    });
  }, []);

  const handleGenerate = async () => {
    if (!selectedCourse) return;
    setLoading(true);
    setError("");
    setStudyData(null);
    try {
      const courseObj = courses.find(c => c.course_id === selectedCourse || (c as any).id === selectedCourse);
      const subject = courseObj ? courseObj.course_name || courseObj.course_id || selectedCourse : selectedCourse;
      
      const data = await getStudyPlan(subject);
      setStudyData(data);
    } catch (err: any) {
      if (err.status === 404) {
        setStudyData({ empty: true });
      } else {
        setError(err.message || "Failed to load study plan.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background selection:bg-accent/20">
      <Navbar />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8 space-y-8">
        <PageHeader 
          title="Study Intelligence" 
          description="AI-generated study schedules and resource recommendations based on exam patterns." 
        />

        {/* Configuration Section */}
        <div className="bg-card rounded-2xl p-6 border border-border">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Zap className="w-5 h-5 text-accent" /> Configure Your Intelligence Plan
          </h2>
          
          <div className="flex flex-col md:flex-row gap-6 mb-6">
            <div className="flex-1">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 block">
                Select Course
              </label>
              <select 
                value={selectedCourse}
                onChange={(e) => setSelectedCourse(e.target.value)}
                className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-accent transition-colors appearance-none"
              >
                <option value="" disabled>Select a course</option>
                {courses.map((c: any) => (
                  <option key={c.course_id || c.id} value={c.course_id || c.id}>
                    {c.course_code || c.code} - {c.course_name || c.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="flex items-end">
              <button 
                onClick={handleGenerate}
                disabled={loading || !selectedCourse}
                className="w-full md:w-auto bg-foreground text-background font-medium rounded-md px-8 py-2 hover:bg-foreground/90 transition-colors disabled:opacity-50 flex items-center gap-2 justify-center"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                Generate Plan
              </button>
            </div>
          </div>
        </div>

        {/* Plan Output */}
        {error ? (
          <div className="h-full min-h-[400px] border border-red-500/20 bg-red-500/5 rounded-xl flex flex-col items-center justify-center text-center p-8">
            <AlertCircle className="w-10 h-10 text-red-500 mb-4 opacity-80" />
            <h3 className="text-lg font-bold text-red-500 mb-2">Failed to load</h3>
            <p className="text-sm text-red-400 max-w-sm">{error}</p>
          </div>
        ) : loading ? (
          <div className="flex flex-col justify-center items-center py-20 min-h-[400px] border border-border rounded-xl">
            <Loader2 className="w-10 h-10 animate-spin text-accent mb-4" />
            <p className="text-sm text-muted-foreground">Generating study intelligence...</p>
          </div>
        ) : studyData && studyData.empty ? (
          <div className="flex flex-col justify-center items-center py-20 min-h-[400px] border border-dashed border-border rounded-xl text-center px-4">
            <Database className="w-10 h-10 text-muted-foreground mb-4 opacity-30" />
            <h3 className="text-lg font-bold text-foreground mb-2">No Study Plan Available</h3>
            <p className="text-sm text-muted-foreground max-w-sm">
              The backend does not have study intelligence configured for this course yet. Check back later or select another course.
            </p>
          </div>
        ) : studyData ? (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Dashboard Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Predicted Topics</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-foreground">{studyData.topics?.length || 0}</span>
                </div>
              </div>
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Overall Probability</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-accent">{studyData.overall_probability ? Math.round(studyData.overall_probability * 100) + '%' : 'N/A'}</span>
                </div>
              </div>
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Recommended Resources</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-foreground">{studyData.resources?.length || 0}</span>
                </div>
              </div>
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Study Progress</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-success">{studyData.progress || '0%'}</span>
                </div>
              </div>
            </div>

            {/* Topic Breakdown */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <h3 className="font-bold text-lg flex items-center gap-2">
                  <Target className="w-5 h-5 text-accent" />
                  Priority Study Targets
                </h3>
                
                {studyData.topics && studyData.topics.length > 0 ? studyData.topics.map((topic: any, idx: number) => (
                  <div key={idx} className="bg-card border border-border rounded-xl p-5">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-lg font-bold text-foreground mb-1">{topic.name || 'Unknown Topic'}</h4>
                        <div className="flex items-center gap-2 text-xs font-medium px-2 py-1 bg-accent/10 text-accent rounded-md inline-flex">
                          Priority: {topic.priority || 'Medium'}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-mono font-bold text-foreground">{topic.probability ? Math.round(topic.probability * 100) : 0}%</div>
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Probability</div>
                      </div>
                    </div>
                    {topic.reason && (
                      <div className="mt-3 text-sm text-muted-foreground border-l-2 border-border pl-3">
                        {topic.reason}
                      </div>
                    )}
                  </div>
                )) : (
                  <div className="p-8 border border-dashed border-border rounded-xl text-center text-muted-foreground">
                    No predicted topics found in this plan.
                  </div>
                )}
              </div>

              {/* Sidebar Resources */}
              <div className="space-y-6">
                <h3 className="font-bold text-lg flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-accent" />
                  Resources
                </h3>
                
                <div className="bg-card border border-border rounded-xl p-5 space-y-4">
                  <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 border-b border-border pb-2">
                    <GraduationCap className="w-4 h-4" /> Recommended
                  </h4>
                  {studyData.resources && studyData.resources.length > 0 ? (
                    <ul className="space-y-3">
                      {studyData.resources.map((res: any, idx: number) => (
                        <li key={idx} className="flex items-start gap-3 text-sm text-muted-foreground">
                          <FileText className="w-4 h-4 mt-0.5 text-accent" />
                          <a href={res.url || '#'} className="hover:text-accent underline-offset-2 hover:underline">{res.title || 'Study Material'}</a>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-xs text-muted-foreground italic">No recommended resources available.</p>
                  )}
                  
                  <h4 className="text-sm font-semibold text-foreground flex items-center gap-2 border-b border-border pb-2 pt-4">
                    <Upload className="w-4 h-4" /> Student Uploaded
                  </h4>
                  {studyData.student_resources && studyData.student_resources.length > 0 ? (
                    <ul className="space-y-3">
                      {studyData.student_resources.map((res: any, idx: number) => (
                        <li key={idx} className="flex items-start gap-3 text-sm text-muted-foreground">
                          <FileText className="w-4 h-4 mt-0.5" />
                          <a href={res.url || '#'} className="hover:text-foreground underline-offset-2 hover:underline">{res.title || 'Notes'}</a>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-xs text-muted-foreground italic">No student uploads yet.</p>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
"""

with open("src/app/study-plan/page.tsx", "w", encoding="utf-8") as f:
    f.write(code)
