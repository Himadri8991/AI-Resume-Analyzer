from resume_parser import extract_text
from utils.text_cleaner import clean_text
from skill_extractor import extract_skills
from similarity_engine import get_similarity
from experience_extractor import extract_experience
from suggestions import generate_suggestions
from job_matcher import match_resume_to_jobs
from nlp_engine import extract_entities

def calculate_ats_score(similarity, skills_matched, total_skills, experience):
    # Core ATS equation (Similarity 50%, Skills 30%, Experience factor 20%)
    skill_ratio = min(len(skills_matched) / max(total_skills, 1), 1.0)
    exp_ratio = min(experience / 5.0, 1.0) # Base 5 years scale

    score = (similarity * 0.5) + (skill_ratio * 0.3) + (exp_ratio * 0.2)
    return round(score * 100, 2)

def skill_gap(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))

def analyze_resume(file_obj, filename, job_description="", job_emb=None):
    try:
        # 1. Parsing
        raw_text = extract_text(file_obj, filename)
        clean_resume = clean_text(raw_text)

        # 2. NLP Entity Extraction
        entities = extract_entities(raw_text)
        
        # 3. Skills & Experience
        resume_skills = extract_skills(clean_resume)
        experience = extract_experience(raw_text)
        
        # 4. SBERT Job Matching (Infer the job role directly from the resume)
        matched_jobs = match_resume_to_jobs(clean_resume, top_k=5)
        top_match = matched_jobs[0] if matched_jobs else None

        # 5. JD Comparison & Scoring (If User Provided JD)
        similarity_score = 0
        missing = []
        ats = 0
        new_job_emb = job_emb
        jd_skills = []
        
        if job_description:
            clean_job = clean_text(job_description)
            jd_skills = extract_skills(clean_job)
            
            similarity_score, new_job_emb = get_similarity(clean_resume, clean_job, job_emb)
            missing = skill_gap(resume_skills, jd_skills)
            ats = calculate_ats_score(similarity_score, set(jd_skills).intersection(set(resume_skills)), len(jd_skills), experience)
        elif top_match:
            # If no manual JD, grade against the best auto-matched O*NET role
            similarity_score = top_match["match_score"] / 100.0
            missing = skill_gap(resume_skills, [s.lower() for s in top_match["skills_needed"]])
            ats = calculate_ats_score(similarity_score, set([s.lower() for s in top_match["skills_needed"]]).intersection(set(resume_skills)), len(top_match["skills_needed"]), experience)
            
        # 6. Suggestions
        suggestions = generate_suggestions(missing, experience, job_match=top_match)

        # 7. Name Formatting Fallback
        final_name = entities["name"]
        if not final_name:
            import os, re
            base = os.path.splitext(filename)[0]
            base = base.replace('_', ' ').replace('-', ' ')
            base = re.sub(r'\(\d+\)', '', base) # Remove (1)
            base = re.sub(r'\d+', '', base) # Remove digits
            base = re.sub(r'(?i)\b(resume|cv|profile|final|updated|draft|candidate)\b', '', base)
            base = base.strip()
            final_name = base.title() if len(base) > 0 else "Unknown Candidate"

        return {
            "name": final_name,
            "email": entities["email"],
            "phone": entities["phone"],
            "education": entities["education"],
            "skills": resume_skills,
            "experience": experience,
            "missing_skills": missing,
            "similarity_score": round(similarity_score * 100, 2),
            "ats_score": ats,
            "matched_roles": matched_jobs,
            "suggestions": suggestions,
            "job_emb_cache": new_job_emb,
            "raw_text_snippet": raw_text[:300]
        }

    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}