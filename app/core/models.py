from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# --- Portfolio Models ---

class PersonalInfo(BaseModel):
    name: str
    title: str
    email: str
    location: str
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class Project(BaseModel):
    id: str
    name: str
    role: str
    description: str
    technologies: List[str] = []
    business_impact: Optional[str] = None

class SkillCategory(BaseModel):
    category: str
    items: List[str]

class ProfessionalConditions(BaseModel):
    availability: Dict[str, Any]
    work_permit: Dict[str, Any]
    salary_expectations: Dict[str, Any]
    motivation_for_change: Optional[str] = None

class Portfolio(BaseModel):
    personal_info: PersonalInfo
    professional_summary: Dict[str, Any]
    projects: Dict[str, Project]
    skills: List[SkillCategory]
    professional_conditions: ProfessionalConditions
    class Config:
        extra = "ignore" 

# --- Application Models ---

class JobOffer(BaseModel):
    raw_text: str = ""
    url: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    is_remote: bool = False
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "EUR"
    visa_sponsorship: Optional[bool] = None
    
class HardFilterStatus(BaseModel):
    remote_pass: bool = True
    visa_pass: bool = True
    salary_pass: bool = True

class AnalysisResult(BaseModel):
    match_score: int = 0
    verdict: str = "PENDING" # STRONGLY_APPLY, APPLY, CONSIDER, IGNORE
    reasoning_summary: Optional[str] = None
    pros: List[str] = []
    cons: List[str] = []
    hard_filter_check: Optional[HardFilterStatus] = None
