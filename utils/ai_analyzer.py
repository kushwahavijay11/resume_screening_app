import os
import json
import openai
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIAnalyzer:
    """Analyze resume using OpenAI API"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def analyze_resume(self, resume_text: str) -> Dict:
        """Extract skills, experience, and education from resume"""
        try:
            prompt = f"""
            Analyze the following resume and extract structured information.
            
            Resume:
            {resume_text[:4000]}  # Limit to avoid token limits
            
            Return a JSON object with the following structure:
            {{
                "skills": {{
                    "technical": ["skill1", "skill2", ...],
                    "soft": ["skill1", "skill2", ...]
                }},
                "experience": "summary of experience including years",
                "education": "summary of education",
                "profile_summary": "brief summary of candidate's profile"
            }}
            
            Only return the JSON object, no additional text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional resume analyzer. Extract structured information from resumes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            return result
            
        except json.JSONDecodeError:
            # Fallback: extract using simple heuristics
            return self._fallback_analysis(resume_text)
        except Exception as e:
            # Fallback to simple extraction
            return self._fallback_analysis(resume_text)
    
    def _fallback_analysis(self, resume_text: str) -> Dict:
        """Fallback analysis using basic text extraction"""
        # Convert to lowercase for easier matching
        text_lower = resume_text.lower()
        
        # Common tech skills
        tech_skills = ["python", "javascript", "java", "c++", "react", "node.js", "sql", "mongodb", 
                       "docker", "kubernetes", "aws", "machine learning", "data analysis", "tensorflow",
                       "pytorch", "html", "css", "typescript", "redux", "spring boot", "django",
                       "jenkins", "terraform", "linux", "git", "agile", "scrum"]
        
        # Soft skills
        soft_skills = ["communication", "leadership", "teamwork", "problem solving", "critical thinking",
                      "adaptability", "creativity", "time management", "interpersonal skills", 
                      "project management", "organization", "attention to detail"]
        
        found_tech = [skill for skill in tech_skills if skill in text_lower]
        found_soft = [skill for skill in soft_skills if skill in text_lower]
        
        # Extract experience (simple heuristic)
        experience = "Not specified"
        if "year" in text_lower:
            import re
            years = re.findall(r'(\d+)\s*year', text_lower)
            if years:
                experience = f"{years[0]} years"
        
        return {
            "skills": {
                "technical": found_tech,
                "soft": found_soft
            },
            "experience": experience,
            "education": "Not specified",
            "profile_summary": "Resume analysis completed using fallback method."
        }
    
    def recommend_job_role(self, skills: Dict, experience: str, education: str, job_roles: List[Dict]) -> Dict:
        """Recommend job role based on skills and experience"""
        try:
            # Flatten skills
            all_skills = skills.get("technical", []) + skills.get("soft", [])
            skills_text = ", ".join(all_skills)
            
            prompt = f"""
            Based on the following candidate profile, recommend the most suitable job role.
            
            Skills: {skills_text}
            Experience: {experience}
            Education: {education}
            
            Available Job Roles:
            {json.dumps(job_roles, indent=2)}
            
            Return a JSON object with:
            {{
                "recommended_role": "job title",
                "match_score": 85,
                "missing_skills": ["skill1", "skill2"],
                "reasoning": "brief explanation"
            }}
            
            Only return the JSON object.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a career advisor. Recommend job roles based on candidate profiles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            # Fallback recommendation
            return self._fallback_recommendation(skills, job_roles)
    
    def _fallback_recommendation(self, skills: Dict, job_roles: List[Dict]) -> Dict:
        """Fallback recommendation based on skill matching"""
        all_skills = set(skills.get("technical", []) + skills.get("soft", []))
        
        best_match = None
        best_score = 0
        best_missing = []
        
        for role in job_roles:
            required = set(role["required_skills"])
            matched = len(all_skills.intersection(required))
            total = len(required)
            
            if total > 0:
                score = (matched / total) * 100
                if score > best_score:
                    best_score = score
                    best_match = role
                    best_missing = list(required - all_skills.intersection(required))
        
        if best_match:
            return {
                "recommended_role": best_match["title"],
                "match_score": round(best_score, 1),
                "missing_skills": best_missing[:5],  # Top 5 missing skills
                "reasoning": f"Candidate's skills match {round(best_score, 1)}% of the requirements for {best_match['title']}."
            }
        else:
            return {
                "recommended_role": "General Software Developer",
                "match_score": 50,
                "missing_skills": ["Python", "JavaScript", "SQL"],
                "reasoning": "No strong match found. Consider expanding your skills."
            }