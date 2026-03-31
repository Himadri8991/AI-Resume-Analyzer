from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def get_similarity_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_similarity(resume_text, job_text, job_emb=None):
    """
    If job_emb is provided, it skips re-encoding the job description 
    (useful for batch processing 1000s of resumes).
    """
    model = get_similarity_model()
    
    resume_emb = model.encode([resume_text])
    
    if job_emb is None:
        job_emb = model.encode([job_text])
        
    score = cosine_similarity(resume_emb, job_emb)
    return float(score[0][0]), job_emb