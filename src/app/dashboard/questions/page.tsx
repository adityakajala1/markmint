"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, X, Filter } from "lucide-react";
import { PageHeader } from "@/components/layout/page-header";
import { QuestionCard } from "@/components/ui/question-card";
import { getQuestions } from "@/lib/api";
import { Question } from "@/lib/types";
import { cn } from "@/lib/utils";

export default function QuestionExplorerPage() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(null);

  // Filters
  const [unit, setUnit] = useState("All");
  const [topic, setTopic] = useState("");
  const [marks, setMarks] = useState("All");
  const [year, setYear] = useState("All");
  const [type, setType] = useState("All");
  const [search, setSearch] = useState("");

  useEffect(() => {
    const fetchQs = async () => {
      setLoading(true);
      try {
        const res = await getQuestions({});
        setQuestions(res.data || res as any);
      } catch (err) {
        console.error("Failed to fetch questions", err);
      } finally {
        setLoading(false);
      }
    };
    fetchQs();
  }, []);

  const filteredQuestions = questions.filter(q => {
    if (unit !== "All" && q.unit !== unit) return false;
    if (topic && !q.topic.toLowerCase().includes(topic.toLowerCase())) return false;
    if (marks !== "All" && q.marks.toString() !== marks) return false;
    if (year !== "All" && q.year.toString() !== year) return false;
    if (type !== "All" && q.questionType !== type) return false;
    if (search && !q.text.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const clearFilters = () => {
    setUnit("All");
    setTopic("");
    setMarks("All");
    setYear("All");
    setType("All");
    setSearch("");
  };

  return (
    <div className="container mx-auto py-8 space-y-6 px-4 sm:px-6 lg:px-8 max-w-7xl">
      <PageHeader 
        title="Question Explorer" 
        description="Search and filter all extracted questions" 
      />

      {/* Filter Bar */}
      <div className="glass rounded-2xl p-4 sm:p-5 border border-border">
        <div className="flex flex-wrap gap-4 items-end">
          <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
            <label className="text-xs font-medium text-muted-foreground">Unit</label>
            <select 
              value={unit} 
              onChange={e => setUnit(e.target.value)}
              className="bg-secondary text-foreground border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow"
            >
              <option value="All">All Units</option>
              <option value="Unit 1">Unit 1</option>
              <option value="Unit 2">Unit 2</option>
              <option value="Unit 3">Unit 3</option>
              <option value="Unit 4">Unit 4</option>
              <option value="Unit 5">Unit 5</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
            <label className="text-xs font-medium text-muted-foreground">Topic</label>
            <input 
              type="text" 
              placeholder="e.g. Normalization"
              value={topic}
              onChange={e => setTopic(e.target.value)}
              className="bg-secondary text-foreground border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow w-full"
            />
          </div>

          <div className="flex flex-col gap-1.5 flex-1 min-w-[100px]">
            <label className="text-xs font-medium text-muted-foreground">Marks</label>
            <select 
              value={marks} 
              onChange={e => setMarks(e.target.value)}
              className="bg-secondary text-foreground border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow"
            >
              <option value="All">All</option>
              <option value="2">2</option>
              <option value="5">5</option>
              <option value="10">10</option>
              <option value="15">15</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5 flex-1 min-w-[100px]">
            <label className="text-xs font-medium text-muted-foreground">Year</label>
            <select 
              value={year} 
              onChange={e => setYear(e.target.value)}
              className="bg-secondary text-foreground border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow"
            >
              <option value="All">All</option>
              <option value="2024">2024</option>
              <option value="2023">2023</option>
              <option value="2022">2022</option>
              <option value="2021">2021</option>
              <option value="2020">2020</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5 flex-1 min-w-[150px]">
            <label className="text-xs font-medium text-muted-foreground">Type</label>
            <select 
              value={type} 
              onChange={e => setType(e.target.value)}
              className="bg-secondary text-foreground border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow"
            >
              <option value="All">All Types</option>
              <option value="Theory">Theory</option>
              <option value="Implementation">Implementation</option>
              <option value="Application">Application</option>
              <option value="Analysis">Analysis</option>
              <option value="Design">Design</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5 flex-1 min-w-[200px]">
            <label className="text-xs font-medium text-muted-foreground">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input 
                type="text" 
                placeholder="Search questions..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="bg-secondary text-foreground border border-border rounded-lg pl-9 pr-3 py-2 text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-shadow w-full"
              />
            </div>
          </div>

          <button 
            onClick={clearFilters}
            className="px-4 py-2 bg-secondary hover:bg-secondary/80 text-foreground border border-border rounded-lg text-sm font-medium transition-colors flex items-center gap-2 h-[38px]"
          >
            <Filter className="w-4 h-4" />
            Clear
          </button>
        </div>
      </div>

      {/* Results Header */}
      <div className="text-sm text-muted-foreground font-medium">
        Showing {filteredQuestions.length} of {questions.length} questions
      </div>

      {/* Questions Grid */}
      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Loading questions...</div>
      ) : filteredQuestions.length === 0 ? (
        <div className="py-20 text-center glass rounded-xl border border-border">
          <h3 className="text-lg font-semibold text-foreground mb-2">No questions found</h3>
          <p className="text-muted-foreground text-sm">Try adjusting your filters to find what you're looking for.</p>
          <button 
            onClick={clearFilters}
            className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Clear all filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
          {filteredQuestions.map(q => (
            <div key={q.id} onClick={() => setSelectedQuestion(q)} className="cursor-pointer">
              <QuestionCard question={q} />
            </div>
          ))}
        </div>
      )}

      {/* Drawer */}
      <AnimatePresence>
        {selectedQuestion && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedQuestion(null)}
              className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed inset-y-0 right-0 w-full max-w-md bg-card border-l border-border z-50 shadow-2xl flex flex-col"
            >
              <div className="p-4 sm:p-6 border-b border-border flex items-center justify-between bg-card/50 backdrop-blur-md">
                <h2 className="text-lg font-semibold">Question Details</h2>
                <button 
                  onClick={() => setSelectedQuestion(null)}
                  className="p-2 hover:bg-secondary rounded-full transition-colors"
                >
                  <X className="w-5 h-5 text-muted-foreground" />
                </button>
              </div>
              <div className="p-4 sm:p-6 overflow-y-auto flex-1 space-y-6">
                <div className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    <span className="px-2.5 py-1 bg-primary/10 text-primary text-xs font-semibold rounded-md border border-primary/20">
                      {selectedQuestion.marks} Marks
                    </span>
                    <span className="px-2.5 py-1 bg-secondary text-secondary-foreground text-xs font-semibold rounded-md border border-border">
                      {selectedQuestion.year}
                    </span>
                    <span className="px-2.5 py-1 bg-secondary text-secondary-foreground text-xs font-semibold rounded-md border border-border">
                      {selectedQuestion.questionType}
                    </span>
                  </div>
                  
                  <div className="prose prose-invert max-w-none">
                    <p className="text-base leading-relaxed text-foreground whitespace-pre-wrap font-medium">
                      {selectedQuestion.text}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <DetailItem label="Unit" value={selectedQuestion.unit} />
                  <DetailItem label="Topic" value={selectedQuestion.topic} />
                  <DetailItem label="Difficulty" value={selectedQuestion.difficulty || "N/A"} />
                  <DetailItem label="Confidence" value={selectedQuestion.confidence ? `${selectedQuestion.confidence}%` : "N/A"} />
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="glass p-3 rounded-lg border border-border">
      <div className="text-xs text-muted-foreground mb-1">{label}</div>
      <div className="text-sm font-semibold text-foreground">{value}</div>
    </div>
  );
}
