from pydantic import BaseModel
class MatchRequest(BaseModel):
    blog_text: str
    top_k: int = 3
    
    class MatchResult(BaseModel):
        filename: str
        caption: str
        distance: float
        
        
    class MatchResponse(BaseModel):
        matches: list[MatchResult]
        matched: bool
        
    class ImageSummary(BaseModel):
        id: int
        filename: str
        caption: str| None
    