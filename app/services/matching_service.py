from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.image import Image
from app.services.vision_pipeline import generate_embeddings
