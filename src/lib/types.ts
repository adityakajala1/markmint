export interface TopicStat {
  topic: string;
  frequency: number;
  confidence: number;
  unit: number;
}

export interface Question {
  id: string;
  text: string;
  topic: string;
  unit: number;
  marks: number;
  year: number;
  type: string[];
  difficulty: number;
  confidence: number;
  source?: string;
}

export interface Prediction {
  topic: string;
  probability: number;
  confidence: number;
  evidence: {
    papers_present: number;
    total_papers: number;
    long_answer_count: number;
  };
  historicalAppearances: number[];
}

export interface DashboardStats {
  papersAnalyzed: number;
  totalQuestions: number;
  topicsDetected: number;
  predictionConfidence: number;
}

export interface CourseInfo {
  id: string;
  name: string;
  code: string;
  semester: number;
  examType: string;
  academicYear: string;
  department: string;
}

export interface TopicFrequency {
  topic: string;
  frequency: number;
  year?: number;
}

export interface MarksDistribution {
  marks: number;
  count: number;
  label: string;
}

export interface UnitDistribution {
  unit: number;
  name: string;
  weight: number;
  questionCount: number;
}

export interface QuestionTypeBreakdown {
  type: string;
  count: number;
  percentage: number;
}

export interface HeatmapCell {
  topic: string;
  year: number;
  frequency: number;
}

export interface HistoricalTrend {
  year: number;
  [topic: string]: number;
}

export interface MarksPattern {
  year: number;
  '2marks': number;
  '5marks': number;
  '10marks': number;
  '15marks': number;
}

export interface UnitWeight {
  unit: number;
  name: string;
  weight: number;
  topicCount: number;
}

export interface ConfidenceGroup {
  level: 'high' | 'medium' | 'low';
  topics: string[];
  evidenceCount: number;
  description: string;
}

export interface QuestionFamily {
  id: string;
  label: string;
  type: 'root' | 'topic' | 'subtopic' | 'question-type';
  children?: QuestionFamily[];
  questions?: Question[];
}

export interface StudyPlanInput {
  timeAvailable: number;
  targetMarks: number;
  currentMastery: number;
}

export interface StudyDay {
  day: number;
  tasks: StudyTask[];
}

export interface StudyTask {
  topic: string;
  hours: number;
  type: 'study' | 'practice' | 'mock-test' | 'revision';
  priority: 'high' | 'medium' | 'low';
}

export interface StudyPlan {
  totalDays: number;
  totalHours: number;
  days: StudyDay[];
  recommendations: string[];
}

export type FilterState = {
  unit: number | null;
  topic: string | null;
  marks: number | null;
  year: number | null;
  questionType: string | null;
  search: string;
};
