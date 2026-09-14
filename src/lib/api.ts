const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetchAPI(path: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const err = new Error(`${res.status} ${res.statusText}`);
    (err as any).status = res.status;
    throw err;
  }
  return res.json();
}

export async function getCourse(id: string | number) {
  return fetchAPI(`/courses/${id}`);
}

export async function getExamQuestions(
  id: string | number,
  page: number = 1,
  size: number = 50
) {
  return fetchAPI(`/exams/${id}/questions?page=${page}&size=${size}`);
}

export async function getExamDNA(id: string | number) {
  return fetchAPI(`/exams/${id}/dna`);
}

export async function getExamPredictions(id: string | number) {
  return fetchAPI(`/exams/${id}/predictions`);
}

// Mocks for Dashboard and Course pages
export async function getDashboardStats() { return null; }
export async function getTopicFrequencies() { return []; }
export async function getMarksDistribution(courseId?: string) { return []; }
export async function getUnitDistribution() { return []; }
export async function getQuestionTypes() { return []; }

export async function getTopicFrequency(courseId: string) { return []; }
export async function getCourseInfo(courseId: string) { return getCourse(courseId); }
export async function getQuestions(params: { courseId: string }) { return { items: [], total: 0 }; }

export async function getHeatmapData(courseId: string) { return []; }
export async function getHistoricalTrends(courseId: string) { return []; }
export async function getMarksPattern(courseId: string) { return []; }
export async function getUnitWeights(courseId: string) { return []; }
export async function getConfidenceGroups(courseId: string) { return []; }
export async function getStudyPlan() { return { totalDays: 0, totalHours: 0, days: [], recommendations: [] }; }
