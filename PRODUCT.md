# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Engineering students at SRMIST. They need to calculate their GPAs across 54+ branches and analyze historical exam patterns to optimize their study time for Cycle Tests and End Semesters.

## Product Purpose
MarkMint is a deterministic exam analytics and forecasting engine. It calculates exact GPAs based on live curriculum data and uses MintAI to predict upcoming exam topics based on historical question families, section weightages, and volatility. Success means students trust the tool's accuracy over generic AI outputs and use it to efficiently pass their exams.

## Positioning
MarkMint relies strictly on deterministic historical extraction. It does not hallucinate probabilities and does not act as a conversational chatbot. It is a utility engine.

## Capabilities and Constraints
- Pulls live 2021 curriculum data for 54+ branches.
- Predicts exam topics using real evidence (confidence scores, rank, history counts, evidence details).
- Connects to a FastAPI backend.
- Strictly handles specific assessment types: CT1, CT2, CT3, ENDSEM.
- Explicitly unresolved predictions are allowed and intentional when data quality is low; no fake data is generated.

## Brand Commitments
- Name: MarkMint (formerly examscope).
- Voice: Calm, Analytical, Premium, Trustworthy, Minimal.
- Constraints: Strict Anti-Vibe-Coding Rules. No purple gradients, no pill-shaped buttons (`rounded-full`), no fake reviews/metrics, no emoji icons, no em dashes, no over-the-top scroll animations, no AI slop photos/copy, no cursor animations.
- Icons must be lucide-react or SVG.
- Light mode must adapt elegantly and not rely on hardcoded dark cards.

## Evidence on Hand
- Live curriculum data for 54+ branches, 8 semesters.
- Existing developer profiles (Aditya: Frontend Engineer, Naman: Backend Engineer).
