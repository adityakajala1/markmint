import {
  mockDashboardStats,
  mockCourseInfo,
  mockTopicStats,
  mockQuestions,
  mockPredictions,
  mockTopicFrequencies,
  mockMarksDistribution,
  mockUnitDistribution,
  mockQuestionTypes,
  mockHeatmapData,
  mockHistoricalTrends,
  mockMarksPattern,
  mockUnitWeights,
  mockConfidenceGroups,
  mockQuestionFamilies,
  mockStudyPlan
} from './mock-data';
import type {
  DashboardStats,
  CourseInfo,
  TopicStat,
  Question,
  Prediction,
  TopicFrequency,
  MarksDistribution,
  UnitDistribution,
  QuestionTypeBreakdown,
  HeatmapCell,
  HistoricalTrend,
  MarksPattern,
  UnitWeight,
  ConfidenceGroup,
  QuestionFamily,
  StudyPlan,
  FilterState
} from './types';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function getDashboardStats(): Promise<DashboardStats> {
  await delay(500);
  return mockDashboardStats;
}

export async function getCourseInfo(): Promise<CourseInfo> {
  await delay(300);
  return mockCourseInfo;
}

export async function getTopicStats(): Promise<TopicStat[]> {
  await delay(400);
  return mockTopicStats;
}

export async function getQuestions(filters?: Partial<FilterState>): Promise<Question[]> {
  await delay(600);
  let questions = [...mockQuestions];
  
  if (filters?.unit) {
    questions = questions.filter(q => q.unit === filters.unit);
  }
  if (filters?.topic) {
    questions = questions.filter(q => q.topic.toLowerCase().includes(filters.topic!.toLowerCase()));
  }
  if (filters?.marks) {
    questions = questions.filter(q => q.marks === filters.marks);
  }
  if (filters?.year) {
    questions = questions.filter(q => q.year === filters.year);
  }
  if (filters?.questionType) {
    questions = questions.filter(q => q.type.includes(filters.questionType!));
  }
  if (filters?.search) {
    questions = questions.filter(q => q.text.toLowerCase().includes(filters.search!.toLowerCase()));
  }
  
  return questions;
}

export async function getPredictions(): Promise<Prediction[]> {
  await delay(700);
  return mockPredictions;
}

export async function getTopicFrequencies(): Promise<TopicFrequency[]> {
  await delay(300);
  return mockTopicFrequencies;
}

export async function getMarksDistribution(): Promise<MarksDistribution[]> {
  await delay(300);
  return mockMarksDistribution;
}

export async function getUnitDistribution(): Promise<UnitDistribution[]> {
  await delay(300);
  return mockUnitDistribution;
}

export async function getQuestionTypes(): Promise<QuestionTypeBreakdown[]> {
  await delay(300);
  return mockQuestionTypes;
}

export async function getHeatmapData(): Promise<HeatmapCell[]> {
  await delay(400);
  return mockHeatmapData;
}

export async function getHistoricalTrends(): Promise<HistoricalTrend[]> {
  await delay(400);
  return mockHistoricalTrends;
}

export async function getMarksPattern(): Promise<MarksPattern[]> {
  await delay(400);
  return mockMarksPattern;
}

export async function getUnitWeights(): Promise<UnitWeight[]> {
  await delay(300);
  return mockUnitWeights;
}

export async function getConfidenceGroups(): Promise<ConfidenceGroup[]> {
  await delay(300);
  return mockConfidenceGroups;
}

export async function getQuestionFamilies(): Promise<QuestionFamily> {
  await delay(500);
  return mockQuestionFamilies;
}

export async function getStudyPlan(): Promise<StudyPlan> {
  await delay(800);
  return mockStudyPlan;
}
