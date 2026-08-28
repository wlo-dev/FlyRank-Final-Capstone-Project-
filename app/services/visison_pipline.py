from pathlib import Path

import ollama


from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.image_repository import ImageRepository

def get_image_files() -> list[Path]:
    corpus_dir = Path(settings.image_corpus-dir)
    return list(corpus_dir.glob("*.jpg"))