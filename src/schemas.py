# src/schemas.py

from pydantic import BaseModel, Field
from enum import Enum

class VerdictEnum(str, Enum):
    GOOD = "good"
    OK = "ok"
    BAD = "bad"

class SingleCriterionEvaluation(BaseModel):
    """Schema for evaluating a single criterion."""
    # Enforcing explanation before verdict as requested in the assignment
    explanation: str = Field(
        description="Detailed reasoning for the verdict based on the rubric. Must be generated before the verdict."
    )
    verdict: VerdictEnum = Field(
        description="The final verdict for this criterion: 'good', 'ok', or 'bad'."
    )

class AllCriteriaEvaluation(BaseModel):
    """Schema for evaluating all criteria in a single API call (Task 6.2)."""
    fluency: SingleCriterionEvaluation
    grammar: SingleCriterionEvaluation
    tone: SingleCriterionEvaluation
    length: SingleCriterionEvaluation
    grounding: SingleCriterionEvaluation