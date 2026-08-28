from pathlib import Path

import ollama

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.image_repository import ImageRepository


def get_image_files() -> list[Path]:
    corpus_dir = Path(settings.image_corpus_dir)
    return list(corpus_dir.glob("*.jpg"))


def generate_caption(image_path: Path) -> str:
    response = ollama.chat(
        model=settings.ollama_vision_model,
        messages=[
            {
                "role": "user",
                "content": "Describe this image in one concise sentence.",
                "images": [str(image_path)],
            }
        ],
    )
    return response["message"]["content"].strip()


def generate_embedding(text: str) -> list[float]: ## this functions purpose is built for  embedding models/ just converts  text to numbers.
    response = ollama.embed(
        model=settings.ollama_embed_model,
        input=text,
    )
    return response["embeddings"][0]