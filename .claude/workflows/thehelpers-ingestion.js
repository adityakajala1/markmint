export const meta = {
  name: 'thehelpers-ingestion',
  description: 'Discover, build scraper, collect, and analyze academic resources from The Helper',
  phases: [
    { title: 'Discovery', detail: 'Map site structure and count resources' },
    { title: 'Architecture', detail: 'Design scraper module and integration' },
    { title: 'Implementation', detail: 'Build scraper components in parallel' },
    { title: 'Integration', detail: 'Connect to ExamScope pipeline' },
    { title: 'Execution', detail: 'Run initial crawl and report' }
  ]
}

// Phase 1: Site Discovery - understand the structure
phase('Discovery')
log('Discovering site structure and resource counts...')

const discoveryPrompt = `Inspect The Helper website (https://thehelpers.tech/) and discover:

1. All semester pages (1-8)
2. For semesters 3, 5, and 7 (sample): list all subjects
3. For 2-3 sample subjects: list all resources with their types

Important constraints:
- The site uses Next.js with client-side routing
- Resource pages like /semesters/3/data-structures-and-algorithm/pyq-nov-2024 returned 404 when accessed directly
- This means we need browser automation (Playwright/Selenium), not simple HTTP requests
- Resources likely link to Google Drive or similar hosting

Provide:
- Total semester count
- Estimated subject count per semester (based on samples)
- Resource types found (PYQ, CT papers, notes, etc.)
- Example resource metadata structure
- Confirmation that browser automation is required

Return a structured analysis.`

const discovery = await agent(discoveryPrompt, {
  label: 'site-discovery',
  schema: {
    type: 'object',
    properties: {
      total_semesters: { type: 'number' },
      sample_subjects: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            semester: { type: 'number' },
            subject: { type: 'string' },
            resources: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  title: { type: 'string' },
                  type: { type: 'string' },
                  url_pattern: { type: 'string' }
                },
                required: ['title', 'type', 'url_pattern']
              }
            }
          },
          required: ['semester', 'subject', 'resources']
        }
      },
      estimated_subjects_per_semester: { type: 'number' },
      estimated_total_resources: { type: 'number' },
      requires_browser_automation: { type: 'boolean' },
      resource_types_found: { type: 'array', items: { type: 'string' } },
      hosting_services: { type: 'array', items: { type: 'string' } }
    },
    required: ['total_semesters', 'sample_subjects', 'estimated_subjects_per_semester', 'estimated_total_resources', 'requires_browser_automation', 'resource_types_found']
  }
})

log(`Found ${discovery.total_semesters} semesters, ~${discovery.estimated_subjects_per_semester} subjects/semester, ~${discovery.estimated_total_resources} total resources`)

// Phase 2: Architecture Design - parallel design of components
phase('Architecture')
log('Designing scraper architecture and ExamScope integration...')

const architectureTasks = [
  {
    name: 'scraper-design',
    prompt: `Design the Playwright-based scraper module for The Helper.

Requirements:
- Navigate client-side routes using browser automation
- Discover semesters → subjects → resources
- Extract metadata: semester, subject, title, resource_type, year, exam_type
- Handle Google Drive links and public file URLs
- URL normalization and deduplication
- SHA-256 file hashing
- Retry logic and error handling
- Request rate limiting
- Progress tracking

Create a detailed module structure for thehelpers/ directory including:
- crawler.py (Playwright navigation)
- parser.py (metadata extraction from page content)
- classifier.py (resource type classification)
- downloader.py (file download with dedup)
- models.py (data models)
- storage.py (database integration)
- tests/ structure

Specify key classes, methods, and data flow.`
  },
  {
    name: 'integration-design',
    prompt: `Design the integration between The Helper scraper and ExamScope's existing analysis pipeline.

Current ExamScope pipeline:
- PDF upload → extraction → question detection → structuring → classification → similarity → analysis

Requirements:
- Reuse existing 7-phase implementation
- No duplicate analysis systems
- Idempotent ingestion (skip already-processed files)
- Maintain provenance (source URLs, metadata)
- Separate raw storage from analysis
- Support incremental updates

Design:
1. How scraped PDFs enter the existing pipeline
2. Where to store raw files vs structured data
3. How to track processing state
4. How to generate aggregate reports
5. Database schema additions needed`
  },
  {
    name: 'classification-rules',
    prompt: `Design robust classification rules for The Helper resources.

Resource types to classify:
- pyq (previous year questions)
- ct_paper (class test papers)
- semester_paper (semester exams)
- syllabus
- question_bank
- notes
- important_questions
- answer_key
- other

Input examples:
- "PYQ Nov 2024" → type: pyq, year: 2024, exam_type: semester
- "CT Papers 2025" → type: ct_paper, year: 2025, exam_type: ct
- "Question Bank" → type: question_bank
- "Unit 1 Notes" → type: notes
- "PYQ Master PDF" → type: pyq (compilation)

Design:
1. Pattern-based rules (regex, keywords)
2. Year extraction logic
3. Exam type inference
4. Handling edge cases and ambiguous titles
5. Priority/relevance scoring for ingestion`
  }
]

const architectureResults = await parallel(architectureTasks.map(task => () =>
  agent(task.prompt, {
    label: task.name,
    phase: 'Architecture',
    effort: 'medium'
  })
))

// Phase 3: Implementation - parallel component building
phase('Implementation')
log('Building scraper components in parallel...')

const implementationTasks = [
  {
    file: 'thehelpers/models.py',
    prompt: `Create thehelpers/models.py with Pydantic models for:
- DiscoveredResource (metadata from crawler)
- ClassifiedResource (after classification)
- DownloadedResource (with file hash, local path)
- IngestionRecord (tracking processing state)

Include all fields from the architecture design:
- source, semester, subject, title, resource_type, year, exam_type
- source_url, file_url, local_path, sha256
- discovery timestamp, classification confidence, etc.

Use existing ExamScope project structure (FastAPI, Pydantic, SQLAlchemy).`
  },
  {
    file: 'thehelpers/classifier.py',
    prompt: `Create thehelpers/classifier.py implementing the classification rules designed earlier.

Include:
- ResourceClassifier class
- classify(title: str) method returning (resource_type, year, exam_type, confidence)
- Pattern matching for each resource type
- Year extraction (2020-2026 range)
- Exam type inference (semester, ct, quiz, etc.)
- Robust handling of variations and typos

Use regex, keyword matching, and heuristics. Return confidence scores.`
  },
  {
    file: 'thehelpers/parser.py',
    prompt: `Create thehelpers/parser.py for extracting metadata from The Helper pages.

Include:
- parse_semester_page(html: str) → List[subject_names]
- parse_subject_page(html: str) → List[resource_metadata]
- extract_file_urls(html: str) → List[direct_urls]
- normalize_url(url: str) → str
- detect_google_drive_links(html: str) → List[drive_urls]

Handle both direct file links and intermediate viewer pages.
Extract resource titles exactly as shown.
Preserve original URLs for provenance.`
  },
  {
    file: 'thehelpers/crawler.py',
    prompt: `Create thehelpers/crawler.py with Playwright-based browser automation.

Include:
- TheHelperCrawler class
- async discover_semesters() → List[int]
- async discover_subjects(semester: int) → List[str]
- async discover_resources(semester: int, subject: str) → List[DiscoveredResource]
- Request rate limiting (1-2 sec delays)
- Error handling and retries (3 attempts)
- Progress callbacks
- robots.txt respect

Use async/await, context managers for browser lifecycle.
Log all navigation and extraction steps.`
  },
  {
    file: 'thehelpers/downloader.py',
    prompt: `Create thehelpers/downloader.py for downloading and deduplicating files.

Include:
- ResourceDownloader class
- async download(resource: DiscoveredResource) → DownloadedResource
- calculate_sha256(file_path: str) → str
- check_duplicate(sha256: str) → Optional[str]  # returns existing path if dup
- URL normalization before download
- Support for Google Drive public links
- Resume partial downloads
- Local storage organization: data/raw/{semester}/{subject}/{filename}

Track all downloads in a SQLite cache to avoid re-downloading.`
  },
  {
    file: 'thehelpers/storage.py',
    prompt: `Create thehelpers/storage.py for database integration with ExamScope.

Include:
- IngestionRepository class
- save_discovered_resource(resource: DiscoveredResource)
- mark_downloaded(resource_id: int, local_path: str, sha256: str)
- mark_processed(resource_id: int, exam_id: int)
- get_unprocessed_resources() → List[DownloadedResource]
- get_ingestion_stats() → Dict (counts by status, type, semester)

Integrate with existing ExamScope database (SQLAlchemy models).
Preserve full provenance chain: discovery → download → processing.`
  },
  {
    file: 'thehelpers/__init__.py',
    prompt: 'Create thehelpers/__init__.py with package exports for main classes and version info.'
  },
  {
    file: 'thehelpers/tests/test_classifier.py',
    prompt: `Create thehelpers/tests/test_classifier.py with pytest tests for:
- Classification of each resource type
- Year extraction edge cases
- Exam type inference
- Confidence scoring
- Handling malformed titles

Use realistic examples from The Helper site.`
  }
]

const implementationResults = await pipeline(
  implementationTasks,
  // Stage 1: Write each file
  async (task) => {
    const content = await agent(task.prompt, {
      label: `write-${task.file}`,
      phase: 'Implementation',
      effort: 'low'
    })
    return { file: task.file, content }
  }
)

log(`Implemented ${implementationResults.filter(Boolean).length} components`)

// Phase 4: Integration - connect to ExamScope
phase('Integration')
log('Creating integration layer and ingestion orchestrator...')

const integrationPrompt = `Create thehelpers/ingest.py - the main orchestrator that:

1. Runs the crawler to discover all resources
2. Classifies each resource
3. Downloads relevant exam resources (skip notes, etc. unless needed)
4. Feeds downloaded PDFs into ExamScope's existing pipeline:
   - Use existing PDF extraction service
   - Use existing question detection
   - Use existing classification
   - Use existing analysis

5. Tracks processing state to enable idempotent re-runs
6. Generates reports:
   - data/reports/corpus_report.json
   - data/reports/corpus_report.md

Include:
- async main() orchestration function
- run_discovery() → List[DiscoveredResource]
- classify_resources(resources) → List[ClassifiedResource]
- download_relevant(resources) → List[DownloadedResource]
- process_through_examscope(downloaded) → List[ProcessedResult]
- generate_reports(results)

CLI interface:
- python -m thehelpers.ingest discover
- python -m thehelpers.ingest download
- python -m thehelpers.ingest process
- python -m thehelpers.ingest full (all stages)
- python -m thehelpers.ingest report

Handle --dry-run, --limit, --semester flags.`

const ingestOrchestrator = await agent(integrationPrompt, {
  label: 'ingest-orchestrator',
  effort: 'medium'
})

// Phase 5: Execution Planning
phase('Execution')
log('Planning initial crawl execution...')

const executionPlanPrompt = `Based on the discovery results, create a detailed execution plan:

Discovery showed:
- ${discovery.total_semesters} semesters
- ~${discovery.estimated_subjects_per_semester} subjects per semester
- ~${discovery.estimated_total_resources} total resources
- Resource types: ${discovery.resource_types_found.join(', ')}

Create an execution plan that includes:

1. Proposed crawl scope:
   - Which semesters to crawl (all 8 or subset for initial dataset?)
   - Resource type priorities (PYQs > CT papers > semester papers > syllabi)
   - Estimated time per semester/subject

2. Data quality thresholds:
   - Minimum papers per subject for "sufficient data"
   - Confidence thresholds for classification
   - Duplicate detection strategy

3. Processing pipeline order:
   - Discovery → Classification → Download → ExamScope ingestion
   - Parallel vs sequential processing
   - Batch sizes

4. Report structure:
   - Dataset statistics
   - Subject coverage analysis
   - Question family detection readiness
   - Gaps and recommendations

5. Next steps after initial ingestion:
   - Frontend updates needed (if any)
   - Analysis queries to run
   - Validation checks

Return as a structured plan with estimated resource requirements.`

const executionPlan = await agent(executionPlanPrompt, {
  label: 'execution-plan',
  schema: {
    type: 'object',
    properties: {
      crawl_scope: {
        type: 'object',
        properties: {
          semesters_to_crawl: { type: 'array', items: { type: 'number' } },
          resource_priorities: { type: 'array', items: { type: 'string' } },
          estimated_duration_minutes: { type: 'number' }
        },
        required: ['semesters_to_crawl', 'resource_priorities', 'estimated_duration_minutes']
      },
      data_quality_thresholds: {
        type: 'object',
        properties: {
          min_papers_for_sufficient_data: { type: 'number' },
          min_classification_confidence: { type: 'number' },
          duplicate_strategy: { type: 'string' }
        },
        required: ['min_papers_for_sufficient_data', 'min_classification_confidence']
      },
      processing_strategy: {
        type: 'object',
        properties: {
          parallelism: { type: 'string' },
          batch_size: { type: 'number' }
        },
        required: ['parallelism', 'batch_size']
      },
      next_steps: {
        type: 'array',
        items: { type: 'string' }
      }
    },
    required: ['crawl_scope', 'data_quality_thresholds', 'processing_strategy', 'next_steps']
  }
})

log('Workflow complete - ready for implementation review and execution')

return {
  discovery,
  architecture: architectureResults.filter(Boolean),
  implementation: implementationResults.filter(Boolean),
  ingest_orchestrator: ingestOrchestrator,
  execution_plan: executionPlan,
  summary: {
    total_semesters: discovery.total_semesters,
    estimated_resources: discovery.estimated_total_resources,
    estimated_crawl_duration: executionPlan.crawl_scope.estimated_duration_minutes,
    semesters_to_crawl: executionPlan.crawl_scope.semesters_to_crawl,
    components_implemented: implementationResults.filter(Boolean).length,
    ready_for_execution: true
  }
}
