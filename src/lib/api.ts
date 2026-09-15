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

// Real Backend Endpoints
export async function getCourses() {
  return fetchAPI("/courses/");
}

export async function getCourse(id: string | number) {
  return fetchAPI(`/courses/${id}`);
}

export async function getPredictions(subject: string) {
  return fetchAPI(`/predictions/${subject}`);
}

export async function getExamPredictions(id: string | number) {
  return fetchAPI(`/predictions/${id}`);
}

export async function getExamQuestions(
  id: string | number,
  page: number = 1,
  size: number = 50
) {
  return fetchAPI(`/exams/${id}/questions?page=${page}&size=${size}`);
}

export async function getExamDNA(course_id: string | number) {
  return fetchAPI(`/analysis/dna?course_id=${course_id}`);
}

export async function getStudyPlan(subject: string) {
  return fetchAPI(`/study/${subject}`);
}

export async function getPractice(subject: string) {
  return fetchAPI(`/practice/${subject}`);
}

// Global dashboard stats (if backend provides a summary, else we'll fetch courses and use that)
export async function getDashboardStats() {
  try {
    return await fetchAPI("/stats/");
  } catch (e) {
    // Fallback if no global stats endpoint exists
    return null;
  }
}
