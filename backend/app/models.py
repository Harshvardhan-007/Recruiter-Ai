from pydantic import BaseModel, Field
from typing import List, Optional

class JobSchema(BaseModel):
    title: str = Field(..., description="The primary job title")
    required_skills: List[str] = Field(..., description="Top 5 technical skills")
    min_years_experience: int
    location: str
    is_remote: bool
    target_companies: Optional[List[str]] = Field(None, description="Companies the recruiter likes")

class CandidateProfile(BaseModel):
    full_name: str
    current_role: str
    years_of_experience: int
    location: str
    skills: List[str]
    profile_url: str
    relevance_explanation: str # Why the AI thinks they fit