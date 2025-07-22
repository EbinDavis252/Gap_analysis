# nlp_extractor.py

import spacy
from spacy.matcher import Matcher

# Load a pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Define a list of skills. This is crucial and should be as comprehensive as possible.
# You can expand this list significantly or load it from a CSV file.
SKILL_LIST = [
    "python", "java", "c++", "sql", "nosql", "mongodb", "postgresql",
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "data analysis", "pandas", "numpy", "matplotlib", "seaborn",
    "streamlit", "flask", "django", "fastapi",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "git", "github", "agile", "scrum", "project management"
]

def extract_skills(text):
    """Extracts skills from a job description using spaCy's Matcher."""
    matcher = Matcher(nlp.vocab)
    
    # Create patterns for the matcher
    for skill in SKILL_LIST:
        # The pattern looks for the exact skill text, case-insensitively
        pattern = [{"LOWER": s.lower()} for s in skill.split()]
        matcher.add(skill.upper(), [pattern])

    doc = nlp(text)
    matches = matcher(doc)
    
    found_skills = set()
    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        found_skills.add(skill_name.lower())
        
    return list(found_skills)

