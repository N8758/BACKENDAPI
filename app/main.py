from fastapi import FastAPI
from .schemas import RewriteRequest, RewriteResponse, RewriteResult
from .tasks import rewrite_task, celery_app
from .cache import get_cache

app = FastAPI(
    title="Tone Rewriter API",
    description="GenAI-powered API to rewrite text in different tones",
    version="1.0.0"
)

# ✅ Root route to avoid 404
@app.get("/")
def read_root():
    return {"message": "Welcome to the Tone Rewriter API 🚀"}

@app.post("/rewrite", response_model=RewriteResponse)
def submit_rewrite(request: RewriteRequest):
    cache_key = f"{request.text}_{request.tone}"
    cached = get_cache(cache_key)
    if cached:
        return RewriteResponse(task_id="cached:" + cache_key)

    task = rewrite_task.delay(request.text, request.tone)
    return RewriteResponse(task_id=task.id)

@app.get("/result/{task_id}", response_model=RewriteResult)
def get_result(task_id: str):
    if task_id.startswith("cached:"):
        cached = get_cache(task_id.replace("cached:", ""))
        return RewriteResult(result=cached or "No cached result")

    result = celery_app.AsyncResult(task_id)
    if result.ready():
        try:
            final_result = str(result.result)
            return RewriteResult(result=final_result)
        except Exception as e:
            return RewriteResult(result=f"Error: {str(e)}")
    return RewriteResult(result="Processing...")
