from pydantic import BaseModel

class RewriteRequest(BaseModel):
    text: str
    tone: str

class RewriteResponse(BaseModel):
    task_id: str

class RewriteResult(BaseModel):
    result: str
