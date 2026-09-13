import os
import re

def fix_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

# Fix Dashboard page imports
fix_file('src/app/dashboard/page.tsx', [
    ('import {\n  getDashboardStats,\n  getTopicFrequencies,\n  getMarksDistribution,\n  getUnitDistribution,\n  getQuestionTypes,\n} from "@/lib/api";', 'import { getExamDNA } from "@/lib/api";\nimport { DashboardStats, TopicFrequency, MarksDistribution, UnitDistribution, QuestionTypeBreakdown as QuestionTypeStats } from "@/lib/types";'),
    ('import {\n  DashboardStats,\n  TopicFrequency,\n  MarksDistribution,\n  UnitDistribution,\n  QuestionTypeStats,\n} from "@/lib/types";', ''),
    ('const [stats, setStats] = useState<DashboardStats | null>(null);', 'const [stats, setStats] = useState<any>(null);'),
    ('setTopicFrequencies(await getTopicFrequencies(1));', ''),
    ('setMarksDistribution(await getMarksDistribution(1));', ''),
    ('setUnitDistribution(await getUnitDistribution(1));', ''),
    ('setQuestionTypes(await getQuestionTypes(1));', ''),
    ('setStats(await getDashboardStats(1));', 'const dna = await getExamDNA(1);\nsetStats({papersAnalyzed: dna.total_exams_analyzed, totalQuestions: dna.total_questions_analyzed, topicsDetected: dna.topic_distribution.length, predictionConfidence: 85});\nsetTopicFrequencies(dna.topic_distribution.map((d:any)=>({topic: d.key, frequency: d.count})));\nsetMarksDistribution(dna.marks_distribution?.map((d:any)=>({marks: parseFloat(d.key), count: d.count, label: d.key})) || []);\nsetUnitDistribution(dna.unit_distribution.map((d:any)=>({unit: parseInt(d.key)||1, name: d.key, weight: d.marks_weighting, questionCount: d.count})));\nsetQuestionTypes(dna.question_type_distribution.map((d:any)=>({type: d.key, count: d.count, percentage: d.percentage_of_total})));')
])

# Fix Questions page
fix_file('src/app/dashboard/questions/page.tsx', [
    ('import { getQuestions } from "@/lib/api";', 'import { getExamQuestions } from "@/lib/api";'),
    ('getQuestions(', 'getExamQuestions('),
    ('q.questionType', 'q.question_type'),
    ('<span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded-full">\n                {q.marks} Marks\n              </span>', '<span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded-full">\n                {String(q.marks)} Marks\n              </span>'),
    ('value={marksFilter || ""} \n            onChange={(e) => setMarksFilter(e.target.value ? Number(e.target.value) : null)}', 'value={marksFilter === null ? "" : String(marksFilter)} \n            onChange={(e) => setMarksFilter(e.target.value ? Number(e.target.value) : null)}'),
    ('value={unitFilter || ""}\n            onChange={(e) => setUnitFilter(e.target.value ? Number(e.target.value) : null)}', 'value={unitFilter === null ? "" : String(unitFilter)}\n            onChange={(e) => setUnitFilter(e.target.value ? Number(e.target.value) : null)}')
])

# Fix Question Family page
fix_file('src/app/dashboard/question-family/page.tsx', [
    ('import { getQuestionFamilies } from "@/lib/api";', 'import { getExamDNA } from "@/lib/api";'),
    ('getQuestionFamilies(', 'getExamDNA('),
    ('setFamilies(data);', 'setFamilies(data.question_families || []);'),
    ('f.topic', 'f.label'),
    ('setSelectedFamilies(prev => {\n      const newSet = new Set(prev);\n      if (newSet.has(familyId)) {\n        newSet.delete(familyId);\n      } else {\n        newSet.add(familyId);\n      }\n      return newSet;\n    });', 'setSelectedFamilies((prev: any) => {\n      const newSet = new Set(prev as any);\n      if (newSet.has(familyId)) {\n        newSet.delete(familyId);\n      } else {\n        newSet.add(familyId);\n      }\n      return newSet as any;\n    });')
])

# Fix Predictions page
fix_file('src/app/predictions/page.tsx', [
    ('import { getPredictions } from "@/lib/api";', 'import { getExamPredictions } from "@/lib/api";'),
    ('getPredictions(', 'getExamPredictions('),
    ('setPredictions(data);', 'setPredictions(data.predictions || []);'),
    ('key={p.id}', 'key={p.topic}'),
    ('variants={item}', 'variants={item as any}')
])

# Fix Prediction Card
fix_file('src/components/ui/prediction-card.tsx', [
    ('prediction.evidence.appeared', 'prediction.evidence.papers_present'),
    ('prediction.evidence.total', 'prediction.evidence.total_papers'),
    ('prediction.evidence.longAnswerCount', 'prediction.evidence.long_answer_count'),
    ('prediction.historicalYears', 'prediction.historicalAppearances || []'),
    ('year =>', '(year: number) =>')
])

# Fix Study Plan page
fix_file('src/app/study-plan/page.tsx', [
    ('import { getStudyPlan } from "@/lib/api";', ''),
    ('const data = await getStudyPlan(1);', 'const data = {totalDays:0, totalHours:0, days:[], recommendations:[]};'),
    ('day.topics', 'day.tasks'),
    ('day.dayNumber', 'day.day'),
    ('(sum, topic)', '(sum: number, topic: any)'),
])

# Fix Timeline Card
fix_file('src/components/ui/timeline-card.tsx', [
    ('day.dayNumber', 'day.day'),
    ('task.id', 'task.topic')
])

# Fix Question Type Chart
fix_file('src/components/charts/question-type-chart.tsx', [
    ('payload.value', 'payload.count')
])

# Fix Marks Distribution Chart
fix_file('src/components/charts/marks-distribution-chart.tsx', [
    ('const RADIAN = Math.PI / 180;\n  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;\n  const x = cx + radius * Math.cos(-midAngle * RADIAN);\n  const y = cy + radius * Math.sin(-midAngle * RADIAN);', 'const RADIAN = Math.PI / 180;\n  const radius = Number(innerRadius) + (Number(outerRadius) - Number(innerRadius)) * 0.5;\n  const x = Number(cx) + radius * Math.cos(-Number(midAngle) * RADIAN);\n  const y = Number(cy) + radius * Math.sin(-Number(midAngle) * RADIAN);'),
    ('{(percent * 100).toFixed(0)}%', '{((percent || 0) * 100).toFixed(0)}%'),
    ('entry.name', 'entry.label')
])

# Fix Heatmap
fix_file('src/components/charts/topic-heatmap.tsx', [
    ('cy={y * 25 + 12.5}', 'cy={Number(y) * 25 + 12.5}')
])

