# ExamScope Context

## WHAT EXAMSCOPE IS
ExamScope is an exam-intelligence platform.
It is NOT intended to be another generic college study bank.
The core idea is: "Understand the exam, not just the questions."

ExamScope analyzes historical examination data to identify:
- recurring topics
- question families
- conceptual repetition
- structural repetition
- marks distribution
- question types
- difficulty
- unit weighting
- historical trends
- recent trends
- emerging topics
- declining topics
- exam-specific patterns

It then combines this historical evidence with the student's current course resources to provide evidence-backed exam insights.

## CURRENT DEVELOPMENT STAGE
We are building the WEBSITE first. The mobile app will come later. Do NOT prioritize mobile functionality right now.

## CURRENT TEAM SPLIT
- Developer 1: Backend / data / intelligence / API (this conversation)
- Developer 2: Frontend / website / UI / UX

## CURRENT BACKEND
The backend/intelligence system has already been developed through seven phases:
1. Paper ingestion
2. Question extraction
3. Question classification
4. Question-family detection
5. Exam DNA analysis
6. Evidence-backed predictions
7. REST API

## PRIMARY DATA SOURCE
The initial large historical dataset comes from: https://app.services.scraper.tech/
A scraper/ingestion system (`thehelpers/`) is being developed to collect publicly accessible examination resources.
Only publicly accessible resources should be processed. Do not bypass authentication, CAPTCHAs, paywalls, anti-bot protections, or access controls.
The scraper should preserve source URLs and metadata.

## HISTORICAL EXAM DATA
Relevant historical examination papers should be processed through:
document → extraction → question detection → question classification → question-family detection → historical analysis → Exam DNA → trend analysis → prediction
Each question should retain provenance (exam, year, semester, subject, exam type, question ID, marks, source document).

## STUDENT RESOURCES
Students should also be able to upload their own course resources. Supported resources may include syllabus, PDF, PPT, DOC, lecture notes, assignments, question banks, lab material, study material, reference material. The system should classify uploaded resources into source types. A student-uploaded historical examination paper should enter the historical exam analysis pipeline.

## SOURCE EVIDENCE MUST REMAIN SEPARATE
Different resources represent different types of evidence.
- Historical exam: Evidence of what was actually asked.
- Syllabus: Evidence of what the course officially covers.
- Lecture material: Evidence of what was taught/emphasized.
- Assignments: Evidence of possible instructor emphasis.
- Question bank: Evidence of potentially emphasized questions.
- Notes/reference material: Contextual information.

IMPORTANT: An assignment mentioning "AVL Trees" must NOT increase the historical frequency of AVL Trees. A historical exam containing an AVL Trees question DOES increase historical frequency. Do not mix these sources into unexplained statistics.

## COURSE CONTEXT
ExamScope should eventually understand relationships across sources, but the system must preserve source type, document, provenance, and evidence strength.

## RECENCY-AWARE ANALYSIS
Historical papers must NOT all have equal predictive weight. Maintain separate analytical views:
- Long-term pattern: Uses the full historical dataset.
- Recent pattern: Prioritizes recent examination cycles.
- Recency-weighted pattern: Newer exams contribute more than older exams using a defensible weighting methodology.

## TREND DETECTION
ExamScope should detect increasing, decreasing, stable, emerging, and declining topics, changing question types, changing marks distribution, changing difficulty, changing unit weighting, and changing question-family recurrence.

## OLD PAPERS
Old papers should NOT be discarded simply because they are old. They remain useful for long-term context, persistent patterns, and detecting genuinely emerging patterns.

## SYLLABUS CHANGES
Where possible, identify syllabus versions. Associate examinations with the syllabus version relevant to them. If the syllabus changes significantly, old evidence should not automatically be treated as directly applicable to the current syllabus.

## EXAM TYPE SEPARATION
Do not automatically combine CT, midterm, end-semester, supplementary, or practical/lab exams. Exam types may be compared, but their underlying statistics must remain distinguishable.

## PREDICTIONS
ExamScope provides evidence-backed assessments. It must NOT pretend to know the exact future exam. Every prediction should ideally expose prediction, confidence, historical frequency, recent frequency, recency-weighted evidence, sample size, supporting evidence, source types, syllabus relevance, and limitations.

## DATA SUFFICIENCY
Prediction confidence must account for dataset size (insufficient, limited, moderate, strong). 

## EVIDENCE TRACEABILITY
Every significant analytical finding must be traceable to its underlying evidence.

## PRIVACY
Student-uploaded documents are private to the relevant student/workspace unless explicitly shared.

## RAW PAPERS
The goal is NOT to publicly redistribute scraped examination PDFs. The website should primarily expose analysis, trends, patterns, question families, evidence, Exam DNA, and predictions.

## WEBSITE
The frontend should eventually allow students to select a course/exam, view Exam DNA, explore historical trends, topics, question families, view evidence and predictions, upload their own resources, and understand current course context.

## CURRENT PRODUCT PRINCIPLE
ExamScope should understand: WHAT HAS BEEN ASKED + WHAT HAS CHANGED + WHAT IS CURRENTLY BEING TAUGHT + WHAT PATTERNS ARE EMERGING + WHY THE SYSTEM BELIEVES THAT. This principle takes priority over adding flashy features.
