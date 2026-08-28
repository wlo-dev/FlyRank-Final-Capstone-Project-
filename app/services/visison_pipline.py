from pathlib import Path

import ollama


from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.image_repository import ImageRepository