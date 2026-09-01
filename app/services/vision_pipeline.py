from pathlib import Path

import ollama
from sqlalchemy import select

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.image_repository import ImageRepository
from app.models.image import Image


def get_image_files() -> list[Path]:
    corpus_dir = Path(settings.image_corpus_dir)
    return list(corpus_dir.glob("*.jpg"))


def generate_caption(image_path: Path) -> str:
    prompts = [
        "Describe this image in one concise sentence.",
        "Describe this image.",
    ]
    for prompt in prompts:
        response = ollama.chat(
            model=settings.ollama_vision_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [str(image_path)],
                }
            ],
        )
        caption = response["message"]["content"].strip()
        if caption:
            return caption
    raise ValueError(f"Moondream returned an empty caption for {image_path.name}")


def generate_embedding(text: str) -> list[float]:
    response = ollama.embed(
        model=settings.ollama_embed_model,
        input=text,
    )
    embeddings = response.get("embeddings", [])
    if not embeddings:
        raise ValueError(f"No embedding returned for text: {text[:50]!r}")
    return embeddings[0]


def run_pipeline():
    db = SessionLocal()
    repo = ImageRepository(db)

    already_done = {
        row.filename for row in db.execute(select(Image.filename)).all()
    }

    image_files = get_image_files()
    remaining = [f for f in image_files if f.name not in already_done]

    print(f"Found {len(image_files)} images total, {len(remaining)} remaining to process.")

    succeeded = 0
    failed = []

    for image_path in remaining:
        print(f"Processing {image_path.name}...")
        try:
            caption = generate_caption(image_path)
            embedding = generate_embedding(caption)

            image = repo.create(filename=image_path.name, filepath=str(image_path))
            image.caption = caption
            image.embedding = embedding
            db.commit()

            print(f"  Caption: {caption}")
            succeeded += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            db.rollback()
            failed.append(image_path.name)

    db.close()
    print(f"Pipeline complete. Succeeded: {succeeded}, Failed: {len(failed)}")
    if failed:
        print("Failed images:", failed)
