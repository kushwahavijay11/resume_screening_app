import json
from typing import List, Dict

class JobMatcher:
    """Match candidate profile with job roles"""
    
    def __init__(self, job_roles_file: str = "data/job_roles.json"):
        with open(job_roles_file, 'r') as f:
            self.job_roles = json.load(f)["job_roles"]
    
    def calculate_match_score(self, candidate_skills: List[str], job_required_skills: List[str]) -> int:
        """Calculate match percentage between candidate skills and job requirements"""
        if not job_required_skills:
            return 0
        
        candidate_skills_set = set([s.lower() for s in candidate_skills])
        required_skills_set = set([s.lower() for s in job_required_skills])
        
        matched = len(candidate_skills_set.intersection(required_skills_set))
        total = len(required_skills_set)
        
        return int((matched / total) * 100) if total > 0 else 0
    
    def find_best_matches(self, candidate_skills: List[str], top_n: int = 3) -> List[Dict]:
        """Find top N matching job roles"""
        results = []
        
        for role in self.job_roles:
            score = self.calculate_match_score(candidate_skills, role["required_skills"])
            missing = [skill for skill in role["required_skills"] 
                      if skill.lower() not in [s.lower() for s in candidate_skills]]
            
            results.append({
                "title": role["title"],
                "match_score": score,
                "required_skills": role["required_skills"],
                "missing_skills": missing[:5],  # Top 5 missing skills
                "experience": role.get("experience", "Not specified"),
                "education": role.get("education", "Not specified")
            })
        
        # Sort by match score (descending)
        results.sort(key=lambda x: x["match_score"], reverse=True)
        
        return results[:top_n]