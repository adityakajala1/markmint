code = '''"use client";

import { useState, useEffect, useRef } from "react";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { PageHeader } from "@/components/layout/page-header";
import { getCourses, getStudyPlan, uploadStudyNotes, updateStudyProgress } from "@/lib/api";
import { BackendCourse } from "@/lib/types";
import { BookOpen, Target, Zap, ShieldCheck, Database, Loader2, AlertCircle, FileText, Upload, CheckCircle2, FileUp, Archive, GraduationCap } from "lucide-react";
import { motion } from "framer-motion";

export default function StudyIntelligencePage() {
  const [courses, setCourses] = useState<BackendCourse[]>([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedCourseObj, setSelectedCourseObj] = useState<BackendCourse | null>(null);
  
  const [loading, setLoading] = useState(false);
  const [studyData, setStudyData] = useState<any>(null);
  const [error, setError] = useState("");

  // Upload states
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [uploadError, setUploadError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

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
    setUploadResult(null);
    setUploadError("");
    
    try {
      const courseObj = courses.find(c => c.course_id === selectedCourse || (c as any).id === selectedCourse);
      setSelectedCourseObj(courseObj || null);
      const subject = courseObj ? courseObj.course_name || courseObj.course_id || selectedCourse : selectedCourse;
      
      const data = await getStudyPlan(subject);
      setStudyData(data);
    } catch (err: any) {
      if (err.status === 404 || err.status === 400) {
        setStudyData({ empty: true });
      } else {
        setError(err.message || "Failed to load study plan.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResourceClick = async (topicName: string, resourceId: string) => {
    if (!selectedCourseObj) return;
    try {
      await updateStudyProgress(selectedCourseObj.course_id, {
        topic: topicName,
        action: "view_resource",
        resource_id: resourceId
      });
      // Optionally refresh plan or locally mark as viewed
    } catch (err) {
      console.error("Failed to update progress", err);
    }
  };

  const handleTopicComplete = async (topicName: string) => {
    if (!selectedCourseObj) return;
    try {
      await updateStudyProgress(selectedCourseObj.course_id, {
        topic: topicName,
        action: "complete_topic"
      });
      // Optionally refresh plan to update progress %
      const subject = selectedCourseObj.course_name || selectedCourseObj.course_id;
      const data = await getStudyPlan(subject);
      setStudyData(data);
    } catch (err) {
      console.error("Failed to complete topic", err);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedCourseObj) return;

    setUploading(true);
    setUploadError("");
    setUploadResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("course_id", selectedCourseObj.course_id);
    formData.append("course_name", selectedCourseObj.course_name);

    try {
      const result = await uploadStudyNotes(formData);
      setUploadResult(result);
      
      // Refresh study plan to show the new uploaded resources
      const subject = selectedCourseObj.course_name || selectedCourseObj.course_id;
      const data = await getStudyPlan(subject);
      setStudyData(data);
    } catch (err: any) {
      setUploadError(err.message || "Upload failed. Please try again.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const renderResourceBadge = (source: string) => {
    switch(source?.toLowerCase()) {
      case "studique":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-accent/20 text-accent"><Database className="w-3 h-3"/> Studique</span>;
      case "pyq":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-muted/20 text-muted-foreground"><Archive className="w-3 h-3"/> PYQ</span>;
      case "student":
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-500"><Upload className="w-3 h-3"/> Your Note</span>;
      default:
        return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-primary/20 text-primary"><BookOpen className="w-3 h-3"/> MarkMint</span>;
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
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 text-foreground">
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
                className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:border-primary text-foreground transition-colors appearance-none"
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
                className="w-full md:w-auto bg-primary text-primary-foreground font-medium rounded-md px-8 py-2 hover:bg-primary/90 transition-colors disabled:opacity-50 flex items-center gap-2 justify-center"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                Load Intelligence
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
          <div className="flex flex-col justify-center items-center py-20 min-h-[400px] border border-border rounded-xl bg-card/50">
            <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
            <p className="text-sm text-muted-foreground">Analyzing priorities and resources...</p>
          </div>
        ) : studyData && studyData.empty ? (
          <div className="flex flex-col justify-center items-center py-20 min-h-[400px] border border-dashed border-border rounded-xl text-center px-4 bg-card/30">
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
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Predicted Topics</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-foreground font-mono">{studyData.topics?.length || 0}</span>
                </div>
              </div>
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Overall Probability</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-primary font-mono">{studyData.overall_probability ? Math.round(studyData.overall_probability * 100) + '%' : 'N/A'}</span>
                </div>
              </div>
              <div className="bg-card border border-border rounded-xl p-5 hover:border-border/80 transition-colors">
                <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-2">Study Progress</p>
                <div className="flex items-end gap-2">
                  <span className="text-2xl font-bold text-foreground font-mono">{studyData.progress || '0%'}</span>
                </div>
              </div>
            </div>

            {/* Topic Breakdown & Uploads */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <h3 className="font-bold text-lg flex items-center gap-2 text-foreground">
                  <Target className="w-5 h-5 text-primary" />
                  Priority Study Targets
                </h3>
                
                {studyData.topics && studyData.topics.length > 0 ? studyData.topics.map((topic: any, idx: number) => (
                  <div key={idx} className="bg-card border border-border rounded-xl p-5">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-lg font-bold text-foreground mb-1">{topic.name || 'Unknown Topic'}</h4>
                        <div className="flex items-center gap-2 text-xs font-medium">
                          <span className={\px-2 py-0.5 rounded-sm \\}>
                            {topic.priority || 'Medium'} Priority
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-mono font-bold text-foreground">{topic.probability ? Math.round(topic.probability * 100) : 0}%</div>
                        <div className="text-[10px] uppercase tracking-wider text-muted-foreground">Probability</div>
                      </div>
                    </div>
                    
                    {topic.reason && (
                      <div className="mt-4 text-sm text-muted-foreground bg-background rounded-md p-3 border border-border/50">
                        <strong className="text-foreground block mb-1 text-xs uppercase tracking-wider">Why study this?</strong>
                        {topic.reason}
                        {topic.historyCount && <div className="mt-2 text-xs opacity-70">Appeared in {topic.historyCount} past papers.</div>}
                      </div>
                    )}

                    {topic.resources && topic.resources.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-border/50">
                        <h5 className="text-xs font-bold text-foreground uppercase tracking-wider mb-3 flex items-center gap-2"><GraduationCap className="w-4 h-4"/> Resources</h5>
                        <ul className="space-y-2">
                          {topic.resources.map((res: any, ridx: number) => (
                            <li key={ridx} className="flex items-center justify-between p-2 rounded-md hover:bg-background transition-colors border border-transparent hover:border-border/50">
                              <div className="flex items-center gap-3 overflow-hidden">
                                <FileText className="w-4 h-4 text-muted-foreground shrink-0" />
                                <a 
                                  href={res.url || '#'} 
                                  target="_blank"
                                  onClick={() => handleResourceClick(topic.name, res.id || \es-\\)}
                                  className="text-sm font-medium hover:text-primary transition-colors truncate"
                                >
                                  {res.title || 'Study Material'}
                                </a>
                                {renderResourceBadge(res.source)}
                              </div>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div className="mt-4 pt-4 flex justify-end">
                      <button 
                        onClick={() => handleTopicComplete(topic.name)}
                        className="text-xs font-medium px-4 py-2 bg-background border border-border rounded-md hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-colors flex items-center gap-2"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                        Mark Completed
                      </button>
                    </div>
                  </div>
                )) : (
                  <div className="p-8 border border-dashed border-border rounded-xl text-center text-muted-foreground">
                    No predicted topics found in this plan.
                  </div>
                )}
              </div>

              {/* Sidebar Resources & Upload */}
              <div className="space-y-6">
                
                {/* Upload Notes Widget */}
                <div className="bg-card border border-border rounded-xl p-5">
                  <h3 className="font-bold text-lg flex items-center gap-2 text-foreground mb-4">
                    <FileUp className="w-5 h-5 text-primary" />
                    Upload Notes
                  </h3>
                  <p className="text-xs text-muted-foreground mb-4">
                    Upload your own PDFs or notes. We'll process them and map them directly to your priority topics.
                  </p>
                  
                  <div className="space-y-4">
                    <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-border rounded-lg cursor-pointer hover:bg-background/50 hover:border-primary/50 transition-colors">
                      <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        {uploading ? (
                          <Loader2 className="w-8 h-8 text-primary animate-spin mb-2" />
                        ) : (
                          <Upload className="w-8 h-8 text-muted-foreground mb-2" />
                        )}
                        <p className="text-sm text-muted-foreground font-medium">
                          {uploading ? "Processing PDF..." : "Click to upload PDF"}
                        </p>
                      </div>
                      <input 
                        ref={fileInputRef}
                        type="file" 
                        accept=".pdf" 
                        className="hidden" 
                        onChange={handleFileUpload}
                        disabled={uploading}
                      />
                    </label>

                    {uploadError && (
                      <div className="text-xs text-red-500 bg-red-500/10 p-2 rounded border border-red-500/20">
                        {uploadError}
                      </div>
                    )}

                    {uploadResult && (
                      <div className="text-xs text-green-600 dark:text-green-400 bg-green-500/10 p-3 rounded border border-green-500/20">
                        <strong className="block mb-1 flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3" /> Successfully Processed!
                        </strong>
                        Mapped to {uploadResult.mapped_topics?.length || 0} topics.
                      </div>
                    )}
                  </div>
                </div>

                {/* Global Resources Summary */}
                {studyData.student_resources && studyData.student_resources.length > 0 && (
                  <div className="bg-card border border-border rounded-xl p-5">
                    <h3 className="font-bold text-lg flex items-center gap-2 text-foreground border-b border-border pb-3 mb-3">
                      <Archive className="w-5 h-5 text-foreground" />
                      Your Library
                    </h3>
                    <ul className="space-y-3">
                      {studyData.student_resources.map((res: any, idx: number) => (
                        <li key={idx} className="flex items-start gap-3 text-sm">
                          <FileText className="w-4 h-4 mt-0.5 text-primary shrink-0" />
                          <div>
                            <a href={res.url || '#'} className="hover:text-primary font-medium transition-colors line-clamp-2">
                              {res.title || 'Student Uploaded Notes'}
                            </a>
                            <div className="mt-1 text-[10px] text-muted-foreground uppercase tracking-wider">
                              Uploaded {new Date().toLocaleDateString()}
                            </div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
'''
with open('src/app/study-plan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
