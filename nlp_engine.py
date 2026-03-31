import spacy
import re

# Load the English NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: spaCy model 'en_core_web_sm' not found. Will be limited to Regex.")
    nlp = None

def extract_entities(text):
    """Extract Named Entities using spaCy + Regex fallbacks"""
    entities = {
        "name": None,
        "email": None,
        "phone": None,
        "education": [],
        "organizations": []
    }

    # Regex for Email and Phone
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    
    email_match = re.search(email_pattern, text)
    if email_match:
        entities["email"] = email_match.group()
        
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        entities["phone"] = phone_match.group()

    if nlp:
        doc = nlp(text)
        
        invalid_keywords = {'backend', 'frontend', 'engineer', 'developer', 'c++', 'java', 'regression', 'association', 'resume', 'pdf', 'machine', 'learning', 'technology', 'software', 'bachelors', 'masters', 'phd', 'college', 'university', 'table', 'tennis', 'tennisassociation', 'cv', 'curriculum', 'vitae'}
        
        # Name Extraction (heuristic: first PERSON entity)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not entities["name"]:
                clean_name = ent.text.strip()
                name_words = clean_name.split()
                name_lower = clean_name.lower()
                
                # Verify it's genuinely a person name and not a title/org
                if 1 <= len(name_words) <= 4 and not any(kw in name_lower for kw in invalid_keywords) and not any(c.isdigit() for c in clean_name):
                    # Also check it doesn't have weird characters
                    if re.match(r'^[A-Za-z\s\-\'\,]+$', clean_name):
                        entities["name"] = clean_name.title()
            elif ent.label_ == "ORG" and ent.text not in entities["organizations"]:
                entities["organizations"].append(ent.text)

    # Robust Fallback: Names are almost always in the first 3 lines of a resume
    if not entities["name"]:
        lines = [line.strip() for line in text.replace('\r', '\n').split('\n') if line.strip()]
        for line in lines[:5]:
            words = line.split()
            # A name is usually 2-4 words, alphabet only
            if 1 <= len(words) <= 4:
                line_lower = line.lower()
                invalid_fallbacks = ['resume', 'cv', 'email', 'phone', 'address', 'curriculum', 'vitae', 'page', 'c++', 'java', 'python', 'developer', 'engineer']
                if not any(kw in line_lower for kw in invalid_fallbacks):
                    if re.match(r'^[A-Za-z\s\-\']+$', line):
                        entities["name"] = line.title()
                        break

    # Education Heuristic Regex
    education_levels = ["Bachelor", "B.S.", "B.A.", "Master", "M.S.", "M.A.", "PhD", "MBA", "B.Tech", "M.Tech"]
    for level in education_levels:
        if re.search(r'\b' + re.escape(level) + r'\b', text, re.IGNORECASE):
            entities["education"].append(level)

    return entities
