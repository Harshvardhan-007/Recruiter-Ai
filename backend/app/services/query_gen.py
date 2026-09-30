from app.models import JobSchema
from typing import Dict

def build_boolean_queries(job: JobSchema) -> Dict[str, str]:
    """
    Generates targeted Boolean search queries for multiple platforms.
    """
    title_term = f'"{job.title}"'
    
    # Take top required skills (quote skills with spaces)
    formatted_skills = [f'"{s}"' if " " in s else s for s in job.required_skills[:4]]
    skills_and = " AND ".join(formatted_skills)
    
    location_term = f'"{job.location}"' if job.location else ""
    
    # 1. Google Dork for LinkedIn Profiles
    linkedin_query = f'site:linkedin.com/in/ {title_term}'
    if skills_and:
        linkedin_query += f' AND ({skills_and})'
    if location_term and not job.is_remote:
        linkedin_query += f' AND {location_term}'
        
    # 2. GitHub Candidate Search Query
    github_skills = " ".join([f'topic:{s.lower().replace(" ", "-")}' for s in job.required_skills[:3]])
    github_query = f'type:user {job.title} {github_skills}'
    if location_term and not job.is_remote:
        github_query += f' location:{job.location}'

    # 3. Generic Web/Resume Query
    resume_query = f'(intitle:resume OR inurl:resume) {title_term}'
    if skills_and:
        resume_query += f' AND ({skills_and})'
    if location_term:
        resume_query += f' AND {location_term}'

    return {
        "linkedin_dork": linkedin_query,
        "github_search": github_query,
        "generic_resume_search": resume_query
    }