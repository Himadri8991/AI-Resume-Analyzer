from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import io
import time
from analyzer import analyze_resume

app = FastAPI(title="PI Enterprise Resume Engine")

# Allow the frontend to call this API without CORS blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_batch(
    files: List[UploadFile] = File(...),
    job_description: Optional[str] = Form("")
):
    try:
        results = []
        cached_job_emb = None
        start_time = time.time()
        
        for i, file in enumerate(files):
            # Read file bytes securely in-memory
            contents = await file.read()
            file_obj = io.BytesIO(contents)
            
            # Analyze using our enterprise engine
            result = analyze_resume(
                file_obj=file_obj,
                filename=file.filename,
                job_description=job_description,
                job_emb=cached_job_emb
            )
            
            if "error" in result:
                results.append({"error": result["error"], "name": file.filename})
                continue
                
            # Cache JD embedding from the first run to accelerate bulk parsing (1,000 resumes!)
            if i == 0 and "job_emb_cache" in result:
                cached_job_emb = result["job_emb_cache"]
                
            # Strip cache array out for JSON serialization
            if "job_emb_cache" in result:
                del result["job_emb_cache"]
                
            results.append(result)

        return {
            "status": "success",
            "time_taken": round(time.time() - start_time, 2),
            "candidates_processed": len(results),
            "results": sorted([r for r in results if not r.get("error")], key=lambda x: x["ats_score"], reverse=True),
            "errors": [r for r in results if r.get("error")]
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Local serving
    uvicorn.run(app, host="0.0.0.0", port=8000)
