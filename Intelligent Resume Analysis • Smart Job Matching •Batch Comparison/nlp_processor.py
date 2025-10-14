import spacy
from skills_database import SKILLS_DB, EDUCATION_DB, EXPERIENCE_KEYWORDS
import re

nlp = spacy.load("en_core_web_sm")

class ResumeProcessor:
    def __init__(self):
        self.skills_db = SKILLS_DB
        self.education_db = EDUCATION_DB
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = {}
        
        for category, skills in self.skills_db.items():
            found_skills[category] = []
            for skill in skills:
                # Case-insensitive search with word boundaries
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills[category].append(skill)
        
        return found_skills
    
    def extract_education(self, text):
        """Extract education information"""
        doc = nlp(text)
        education = []
        
        # Look for education keywords using spaCy
        for token in doc:
            if token.text.lower() in [e.lower() for e in self.education_db]:
                # Get context around the token
                start = max(0, token.i - 5)
                end = min(len(doc), token.i + 10)
                education.append(doc[start:end].text)
        
        return list(set(education))  # Remove duplicates
    
    def extract_email(self, text):
        """Extract email addresses from resume"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))  # Remove duplicates
    
    def extract_phone(self, text):
        """Extract phone numbers from resume"""
        # Patterns for different phone formats
        phone_patterns = [
            r'\+?1?\s*\(?([0-9]{3})\)?[\s.-]?([0-9]{3})[\s.-]?([0-9]{4})',  # US format
            r'\+234\s?([0-9]{10})',  # Nigeria +234
            r'0\d{10}',  # Nigeria format 0XXXXXXXXXX
            r'\+?[\d\s\-\(\)]{10,15}'  # General international format
        ]
        
        phones = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phones.extend(matches)
        
        # Filter out numbers that are too short or obviously not phones
        cleaned_phones = []
        for phone in phones:
            if isinstance(phone, tuple):
                phone = ''.join(str(p) for p in phone if p)
            phone_str = str(phone)
            # Keep only if it has at least 10 digits
            digits_only = re.sub(r'\D', '', phone_str)
            if len(digits_only) >= 10:
                cleaned_phones.append(phone_str)
        
        return list(set(cleaned_phones))  # Remove duplicates
    
    def extract_dates(self, text):
        """Extract valid dates/periods from resume"""
        doc = nlp(text)
        dates = []
        
        # Look for DATE entities from spaCy
        for ent in doc.ents:
            if ent.label_ == "DATE":
                # Filter out random numbers that spaCy might have flagged
                date_text = ent.text.strip()
                # Check if it looks like a real date (contains month names or year patterns)
                if any(month in date_text.lower() for month in 
                       ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']) \
                   or re.search(r'\b(20|19)\d{2}\b', date_text) \
                   or re.search(r'\b(present|current|ongoing)\b', date_text, re.IGNORECASE):
                    dates.append(date_text)
        
        # Also look for common date patterns
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b',  # Jan 2024
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b',  # 01/01/2024
            r'\b(20|19)\d{2}[-–]\s*(present|current|ongoing)\b',  # 2024-Present
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))  # Remove duplicates
    
    def extract_experience(self, text):
        """Extract work experience highlights"""
        doc = nlp(text)
        experiences = []
        
        for sent in doc.sents:
            sent_lower = sent.text.lower()
            # Check if sentence contains experience keywords
            if any(keyword in sent_lower for keyword in EXPERIENCE_KEYWORDS):
                # Filter out very short sentences
                if len(sent.text.split()) > 5:
                    experiences.append(sent.text.strip())
        
        return experiences[:10]  # Return top 10 experiences
    
    def extract_entities(self, text):
        """Extract named entities (organizations only, not dates)"""
        doc = nlp(text)
        entities = {
            "ORG": [],
            "PERSON": []
        }
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                if ent.text not in entities[ent.label_]:
                    entities[ent.label_].append(ent.text)
            elif ent.label_ == "PERSON":
                if ent.text not in entities[ent.label_]:
                    entities[ent.label_].append(ent.text)
        
        return entities
    
    def process_resume(self, text):
        """Complete resume processing pipeline"""
        return {
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "entities": self.extract_entities(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "dates": self.extract_dates(text)
        }