from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.image import Image
from app.services.vision_pipeline import generate_embedding


def find_best_matches(db: Session, blog_text: str, top_k: int = 3):
    query_embedding = generate_embedding(blog_text)
    
    
    results = db.execute(
        select(
            Image,
            Image.embedding.cosine_distance(query_embedding).label("distance"),
        )
        .order_by("distance")
        .limit(top_k)

    ).all()
    
    return results
