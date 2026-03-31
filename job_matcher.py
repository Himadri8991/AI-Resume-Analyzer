import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load jobs
try:
    with open('data/job_categories.json', 'r', encoding='utf-8') as f:
        JOB_DATASET = json.load(f)
except Exception as e:
    JOB_DATASET = []
    print(f"Error loading Job Dataset: {e}")

_model = None

def get_model():
    global _model
    if _model is None:
        # MiniLM is perfect for fast local inference and good accuracy
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

# Pre-compute job embeddings for fast matching
_job_embeddings = None
_job_list = []

def init_job_embeddings():
    global _job_embeddings, _job_list
    if _job_embeddings is None and JOB_DATASET:
        model = get_model()
        texts = []
        for job in JOB_DATASET:
            # Create a rich text representation of the job
            text = f"{job['job_title']} {job['category']} {' '.join(job['skills'])} {' '.join(job.get('keywords', []))}"
            texts.append(text)
            _job_list.append(job)
        
        if texts:
            _job_embeddings = model.encode(texts)

def match_resume_to_jobs(resume_text, top_k=5):
    """
    Takes parsed resume text, encodes it, and compares against 
    pre-computed job category embeddings to find the best domain/role fits.
    """
    init_job_embeddings()
    if _job_embeddings is None or len(_job_list) == 0:
        return []

    model = get_model()
    resume_emb = model.encode([resume_text])
    
    similarities = cosine_similarity(resume_emb, _job_embeddings)[0]
    
    # Get top K indices
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    matches = []
    for idx in top_indices:
        job = _job_list[idx]
        matches.append({
            "job_title": job["job_title"],
            "category": job["category"],
            "sub_category": job["sub_category"],
            "skills_needed": job["skills"],
            "match_score": round(float(similarities[idx]) * 100, 2)
        })
        
    return matches
