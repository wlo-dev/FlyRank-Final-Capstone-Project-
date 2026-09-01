from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.image import Image
from app.services.vision_pipeline import generate_embeddings


def find_best_matches(db: Session, blog_text: str, top_k: int = 3):
    query_embedding = generate_embedding(blog_text)
    
    
    result = db.execute(
        
    )
