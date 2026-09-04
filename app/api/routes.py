from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.models.image import Image
from app.repositories.image_repository import ImageRepository
from app.services.matching_service import find_match_with_guard
from app.api.schemas import MatchRequest, MatchResponse, MatchResult, ImageSummary

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/images", response_model=list[ImageSummary])
def list_images(db: Session = Depends(get_db)):
    repo = ImageRepository(db)
    images = repo.get_all()
    return images