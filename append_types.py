
with open('src/lib/types.ts', 'a', encoding='utf-8') as f:
    f.write('''\n
export interface StudyResource {
  id?: string;
  title: string;
  url: string;
  source: 'local' | 'studique' | 'student' | 'pyq' | string;
  type?: string;
  description?: string;
}

export interface StudyTopicPlan {
  name: string;
  probability: number;
  priority: 'High' | 'Medium' | 'Low' | string;
  reason: string;
  resources: StudyResource[];
  historyCount?: number;
  evidence_details?: string;
}

export interface StudyPlanResponse {
  course_name: string;
  overall_probability?: number;
  topics: StudyTopicPlan[];
  resources?: StudyResource[];
  student_resources?: StudyResource[];
  progress?: string | number;
  empty?: boolean;
}

export interface StudyUploadResponse {
  status: string;
  document_id: string;
  mapped_topics: string[];
  message?: string;
}
''')

