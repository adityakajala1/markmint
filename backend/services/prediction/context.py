from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class HistoricalContext:
    course_id: int
    cutoff_year: int
    
class PredictionTarget:
    TOPIC = "topic"
    UNIT = "unit"
    FAMILY = "family"
    CONCEPT = "concept"
