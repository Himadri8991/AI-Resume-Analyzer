import re

def extract_experience(text):
    text = text.lower()
    
    # Common regex patterns to detect "X years" or "X+ years"
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*yrs?\s*exp',
        r'experience[:\s]+(\d+)\+?\s*years?',
        r'(\d+)(?:\.\d+)?\+?\s*years?',
    ]
    
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                # Catch cases where match is a string with a dot
                val = float(match)
                if val < 40: # Unlikely to have 40+ years explicitly written like this, filter out noise
                    max_years = max(max_years, val)
            except ValueError:
                pass
                
    # Fallback to checking date spans (e.g., 2018 - 2023)
    # Simple heuristic to extract overall years
    years = [int(y) for y in re.findall(r'\b(19|20)\d{2}\b', text)]
    if len(years) >= 2:
        diff = max(years) - min(years)
        if diff < 40 and diff > max_years:
            max_years = float(diff)
            
    return round(max_years, 1)