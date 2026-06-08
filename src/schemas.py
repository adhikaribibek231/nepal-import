from typing import Literal

from pydantic import BaseModel, Field

ConflictStatus = Literal[
    "consistent",
    "conflict",
    "partial_match",
    "missing_in_one_source",
    "needs_confirmation",
]
RequirementStatus = Literal[
    "evidence_found", "partial", "missing", "needs_confirmation", "not_assessed"
]


class Evidence(BaseModel):
    source_file: str
    page: str
    quote_or_summary: str
    confidence: Literal["low", "medium", "high"] = "medium"


class ProductFact(BaseModel):
    field_name: str
    raw_value: str
    normalized_value: str | None = None
    evidence: Evidence


class RequirementMapping(BaseModel):
    requirement: str
    status: RequirementStatus
    evidence: list[Evidence] = Field(default_factory=list)
    notes: str | None = None


class Conflict(BaseModel):
    field_name: str
    source_a: str
    source_b: str
    status: ConflictStatus
    issue: str
    decision: str | None = None


class ExtractedFacts(BaseModel):
    facts: list[ProductFact] = Field(default_factory=list)


class ReviewMapping(BaseModel):
    mappings: list[RequirementMapping] = Field(default_factory=list)


class ConflictMatrix(BaseModel):
    conflicts: list[Conflict] = Field(default_factory=list)
