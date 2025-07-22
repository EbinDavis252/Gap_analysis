# nlp_extractor.py

import spacy
import en_core_web_sm  # <-- KEY CHANGE: Import the model package directly
from spacy.matcher import Matcher

# Load the model from the imported package
nlp = en_core_web_sm.load() # <-- KEY CHANGE: Use the .load() method of the package

# --- The rest of your code remains the same ---
SKILL_LIST = [
    "python", "java", "c++", "sql", "nosql", "mongodb", "postgresql",
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "data analysis", "pandas", "numpy", "matplotlib", "seaborn",
    "streamlit", "flask", "django", "fastapi",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "git", "github", "agile", "scrum", "project management"
]

def extract_skills(text):
    matcher = Matcher(nlp.vocab)
    for skill in SKILL_LIST:
        pattern = [{"LOWER": s.lower()} for s in skill.split()]
        matcher.add(skill.upper(), [pattern])
    doc = nlp(text)
    matches = matcher(doc)
    found_skills = set()
    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        found_skills.add(skill_name.lower())
    return list(found_skills)

