# ExamScope Prediction Methodology

## Core Philosophy
ExamScope does not predict the future using AI "vibes" or LLM hallucinations. All predictions and backtests are strictly deterministic, mathematically modeled, and chronologically isolated.

## The Temporal Leakage Barrier
To prove predictive value, the `BacktestEngine` uses a **Sliding Window Iterator**.
- When evaluating the predictive accuracy for the target year $Y$, the engine executes a strict SQL filter: `WHERE year < Y`.
- This guarantees that no questions, trends, or marks from year $Y$ (or later) influence the generation of the Exam DNA.

## Baselines
ExamScope predictions are measured against two naive baselines:
1. **Historical Baseline**: Predicting that the upcoming exam will exactly mirror the average of all past exams.
2. **Recent Baseline**: Predicting that the upcoming exam will exactly mirror the most recent exam.

The Engine's precision and recall (Marks@5, Precision@5) must consistently beat these baselines to be considered statistically valid.

## Data Sufficiency & Confidence
The engine refuses to output a confident prediction if the dataset is too small. 
- **INSUFFICIENT**: < 2 papers or < 10 questions.
- **LIMITED**: < 4 papers or < 30 questions.
- **MODERATE**: < 7 papers or < 100 questions.
- **STRONG**: 7+ papers.

If a dataset is INSUFFICIENT, the engine overrides the confidence score and the API outputs an explicit warning state to the frontend.
