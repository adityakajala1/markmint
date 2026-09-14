# ExamScope Known Limitations

ExamScope is currently in Beta. The following architectural, data, and analytical limitations are known and active:

## 1. The "OR" Marks Inflation
The PDF extraction layer does not yet construct mutually exclusive choice blocks (`Q1(a) OR Q1(b)`). It parses both options as mandatory, which artificially inflates the total marks of an exam and slightly skews `marks_importance` scoring.

## 2. Global Question Families
Question families are calculated continuously. When backtesting a historical year (e.g., 2022), the recurrence tag (`family.repetition_type`) might be influenced by 2024 data. This is a mild temporal leak in the family tagging layer, though raw frequencies remain isolated.

## 3. The Year 0 Collapse
Exams missing chronological metadata (`year=None`) default to `0` during sorting. This severely corrupts the median time-split used by the Exam Evolution engine for detecting trends.

## 4. Dense Embedding Collisions
Short theoretical questions ("What is a Stack?", "What is a Graph?") may exhibit >95% cosine similarity if relying purely on embeddings, leading to false family grouping. 

## 5. API Search Performance
The current `/search` endpoint uses fallback `.ilike("%term%")` string matching on `Text` columns. Without a Postgres `tsvector`/GIN index, this requires a full table scan and will degrade API latency as the dataset scales.
