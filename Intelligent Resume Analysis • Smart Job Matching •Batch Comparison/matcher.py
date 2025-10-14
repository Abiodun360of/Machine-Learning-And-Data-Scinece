from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class JobMatcher:
    def __init__(self, resume_skills, job_description):
        self.resume_skills = resume_skills
        self.job_description = job_description
    
    def flatten_skills(self, skills_dict):
        """Convert skill dict to flat list"""
        return [skill for category in skills_dict.values() for skill in category]
    
    def calculate_skill_match(self):
        """Calculate matching skills percentage"""
        resume_skills_flat = self.flatten_skills(self.resume_skills)
        job_skills = self.extract_job_skills(self.job_description)
        
        # FIX: Always return a dictionary, not an integer
        if not job_skills:
            return {
                "match_percentage": 0,
                "matched_skills": [],
                "missing_skills": []
            }
        
        matches = len(set(resume_skills_flat) & set(job_skills))
        match_percentage = (matches / len(job_skills)) * 100
        
        return {
            "match_percentage": round(match_percentage, 2),
            "matched_skills": list(set(resume_skills_flat) & set(job_skills)),
            "missing_skills": list(set(job_skills) - set(resume_skills_flat))
        }
    
    def extract_job_skills(self, job_description):
        """Extract skills mentioned in job description"""
        job_skills = []
        job_text_lower = job_description.lower()
        
        # Get all skills from the database
        from skills_database import SKILLS_DB
        
        for category, skills in SKILLS_DB.items():
            for skill in skills:
                if skill.lower() in job_text_lower:
                    job_skills.append(skill)
        
        return job_skills
    
    def semantic_similarity(self):
        """Calculate semantic similarity using TF-IDF"""
        vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            vectors = vectorizer.fit_transform([
                " ".join(self.flatten_skills(self.resume_skills)),
                self.job_description
            ])
            similarity = cosine_similarity(vectors)[0][1]
            return round(similarity * 100, 2)
        except:
            return 0
    
    def get_match_report(self):
        """Generate complete match report"""
        skill_match = self.calculate_skill_match()
        semantic_score = self.semantic_similarity()
        
        return {
            "skill_match": skill_match,
            "semantic_similarity": semantic_score,
            "overall_score": round((skill_match["match_percentage"] + semantic_score) / 2, 2)
        }