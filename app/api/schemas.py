from pydantic import BaseModel
class MatchRequest(BaseModel):
    user_id: int
    blog_text: str
    top_k: int = 3
    