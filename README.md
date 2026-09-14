# FlyRank Image Relevance Engine

An AI-powered backend service that semantically matches blog post content to the most relevant image in a corpus, using local vision and embedding models. Built as a FlyRank Backend AI Engineering capstone project.

## Demo

**Video walkthrough:**

[https://raw.githubusercontent.com/wlo-dev/FlyRank-Final-Capstone-Project-/main/docs/demo/flyrank-demo.mp4]

**Screenshots:**

| Input | Matched Results |
|-------|------------------|
| ![Input screenshot](docs/screenshots/input%20screenshot.png) | ![Results screenshot](docs/screenshots/output%20screenshot.png) |

## What it does

Given a piece of blog text, the system:
1. Generates a caption for every image in the corpus using a local vision model (moondream)
2. Converts each caption into a semantic embedding using a local embedding model (all-minilm)
3. Embeds the incoming blog text the same way
4. Searches for the closest matching image(s) using cosine similarity via pgvector
5. Applies a mismatch guard that rejects matches below a confidence threshold, rather than forcing a poor pairing

## Tech stack

- **Python 3.14**
- **FastAPI** — REST API layer
- **PostgreSQL 16 + pgvector** — vector similarity search, running in Docker
- **SQLAlchemy 2.0** — ORM and database access
- **Ollama** — local model runtime, running `moondream` (vision) and `all-minilm` (embeddings)
- **Pydantic / pydantic-settings** — data validation and configuration management
- **Docker Compose** — Postgres containerization

## Architecture

```
app/
├── main.py                    # FastAPI app entrypoint, CORS, static file serving
├── core/
│   └── config.py               # Typed, validated settings loaded from .env
├── db/
│   └── session.py               # SQLAlchemy engine and session management
├── models/
│   └── image.py                 # Image table definition (filename, caption, embedding, etc.)
├── repositories/
│   └── image_repository.py      # Database access layer for images
├── services/
│   ├── vision_pipeline.py       # Captioning + embedding generation via Ollama
│   └── matching_service.py      # Cosine similarity search + mismatch guard
└── api/
    ├── schemas.py                # Request/response data shapes
    └── routes.py                 # /health, /images, /match endpoints

frontend/
└── index.html                  # Simple demo UI for presentation purposes
```

## Setup

### Prerequisites
- Python 3.11+
- Docker Desktop
- [Ollama](https://ollama.com) installed locally, with the following models pulled:
  ```
  ollama pull moondream
  ollama pull all-minilm
  ```

### 1. Clone and install dependencies
```bash
git clone https://github.com/wlo-dev/FlyRank-Final-Capstone-Project-.git
cd FlyRank-Final-Capstone-Project-
pip install -r requirements.txt
```

### 2. Configure environment
Copy `.env.example` to `.env` and fill in a real Postgres password:
```bash
cp .env.example .env
```

### 3. Start Postgres
```bash
docker compose up -d
```

### 4. Create the database table
```bash
python -c "from app.models.image import Base; from app.db.session import engine; Base.metadata.create_all(engine)"
```

### 5. Run the vision pipeline
Processes every image in `data/images/`, generating captions and embeddings:
```bash
python -c "from app.services.vision_pipeline import run_pipeline; run_pipeline()"
```

### 6. Start the API
```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 7. (Optional) Try the demo frontend
Open `frontend/index.html` directly in a browser while the API is running.

## API Endpoints

| Method | Endpoint   | Description                                |
|--------|------------|---------------------------------------------|
| GET    | `/health`  | Health check                                |
| GET    | `/images`  | List all images in the corpus               |
| POST   | `/match`   | Match blog text to the closest image(s)     |

### Example request
```json
POST /match
{
  "blog_text": "An article about wolves hunting in a snowy forest.",
  "top_k": 3
}
```

### Example response
```json
{
  "matches": [
    { "filename": "wolf_02.jpg", "caption": "...", "distance": 0.4513 }
  ],
  "matched": true
}
```

If no image is a confident enough match, `matches` will be empty and `matched` will be `false`.

## Design notes and known limitations

- **Mismatch guard threshold** is currently set to a cosine distance of `0.55`. This was tuned empirically: values above this consistently corresponded to genuinely unrelated content, while lower values captured legitimate matches.
- **Match quality depends on descriptive query text.** The embedding model used (`all-minilm`) is small and optimized for speed and local/offline use rather than maximum semantic accuracy. Clear, descriptive blog text (similar in style to the image captions) produces the most reliable matches. Very short, indirect, or ambiguous phrasing can occasionally produce a less confident or incorrect match.
- **The corpus is currently 50 images** across five animal categories (bear, deer, dog, fox, wolf), generated for development and testing purposes.

## Possible future improvements

- Add a pgvector index (e.g. IVFFlat or HNSW) for faster search at larger corpus sizes
- Expand the image corpus and diversify categories
- Add authentication for production use
- Swap in a larger embedding model for improved semantic accuracy, if latency allows

## Author

Willouby — Final-year BSc IT (Software Engineering) student, Eduvos Cape Town
Built during a Backend AI Engineering internship at FlyRank AI# FlyRank Image Relevance Engine

