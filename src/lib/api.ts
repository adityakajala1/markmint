const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// ==========================================
// TEMP MOCK DATA (For UI Development Only)
// ==========================================
const MOCK_COURSES = [
  { course_id: "CS101", course_code: "CS101", course_name: "Operating Systems", name: "Operating Systems", code: "CS101" },
  { course_id: "CS102", course_code: "CS102", course_name: "Database Systems", name: "Database Systems", code: "CS102" }
];

const MOCK_STUDY_PLAN = {
  course_name: "Operating Systems",
  overall_probability: 0.84,
  progress: "25%",
  topics: [
    {
      name: "Process Scheduling Algorithms",
      probability: 0.92,
      priority: "High",
      reason: "High volatility and historically appears in 80% of CT2 assessments.",
      historyCount: 12,
      resources: [
        { id: "res1", title: "Round Robin Scheduling Breakdown", url: "#", source: "studique" },
        { id: "res2", title: "2021 Previous Year Question", url: "#", source: "pyq" }
      ]
    },
    {
      name: "Deadlock Avoidance (Banker's Algorithm)",
      probability: 0.75,
      priority: "Medium",
      reason: "Appeared in last year's end semester. Moderate chance of recurrence.",
      historyCount: 5,
      resources: [
        { id: "res3", title: "Banker's Algo Reference", url: "#", source: "local" }
      ]
    }
  ],
  student_resources: [
    { id: "s1", title: "My OS Unit 2 Notes.pdf", url: "#", source: "student" }
  ]
};

const shouldUseMocks = () => process.env.NEXT_PUBLIC_USE_MOCKS === "true";


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

export async function getStudyPriorities(course_name: string) {
  return fetchAPI(`/study/priorities/${course_name}`);
}

export async function getStudyPlan(course_name: string) {
  return fetchAPI(`/study/plan/${course_name}`);
}

export async function getStudyResources(course_name: string, topic_name: string) {
  return fetchAPI(`/study/resources/${course_name}/${topic_name}`);
}

export async function uploadStudyNotes(formData: FormData) {
  if (shouldUseMocks() || process.env.NODE_ENV === "development") {
    return new Promise(resolve => setTimeout(() => {
      resolve({ status: "success", document_id: "mock_doc_123", mapped_topics: ["Process Scheduling Algorithms"] });
    }, 1500));
  }
  const res = await fetch(`${API_BASE}/study/uploads`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    throw new Error(`Upload failed: ${res.status}`);
  }
  return res.json();
}

export async function updateStudyProgress(course_id: string, data: any) {
  if (shouldUseMocks() || process.env.NODE_ENV === "development") {
    return new Promise(resolve => setTimeout(() => resolve({ status: "success" }), 300));
  }
  return fetchAPI(`/study/progress/${course_id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
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
