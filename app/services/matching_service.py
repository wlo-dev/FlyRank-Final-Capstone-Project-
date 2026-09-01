from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.image import Image
from app.services.vision_pipeline import generate_embedding

# Cosine distance threshold: matches with a distance ABOVE this value
# are considered too dissimilar to be a good match, and get rejected
# by the mismatch guard instead of being returned as a false match.
MISMATCH_THRESHOLD = 0.6


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


def find_match_with_guard(db: Session, blog_text: str, top_k: int = 3):
    """
    Same as find_best_matches, but applies the mismatch guard: if even
    the closest match is too dissimilar (distance above the threshold),
    this returns no matches at all rather than forcing a bad pairing.
    """
    results = find_best_matches(db, blog_text, top_k)

    if not results:
        return []

    best_distance = results[0][1]
    if best_distance > MISMATCH_THRESHOLD:
        return []

    return results
