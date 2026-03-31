import json
from rapidfuzz import fuzz, process

def load_skills():
    try:
        with open('data/skills_taxonomy.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return list(data.keys())
    except FileNotFoundError:
        return [
            "Python", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "Docker", "Kubernetes",
            "SQL", "React", "Node.js", "AWS", "Google Cloud",
            "Communication", "Leadership", "Problem Solving"
        ]

skills_list = load_skills()

def extract_skills(text):
    text = text.lower()
    found_skills = set()
    
    # Fast exact matching
    for skill in skills_list:
        if skill.lower() in text:
            found_skills.add(skill)
            
    # Optional fuzzy matching for near-misses
    # We tokenize text roughly to find matches
    words = set(text.split())
    for skill in skills_list:
        if skill not in found_skills:
            # Check against words/phrases for high match probability
            if len(skill.split()) == 1:
                # single word skill fuzzy
                for word in words:
                    if len(word) > 4 and fuzz.ratio(skill.lower(), word) > 85:
                        found_skills.add(skill)
                        break
                        
    return list(found_skills)