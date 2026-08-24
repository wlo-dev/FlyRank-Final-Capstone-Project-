from sqlalchemy.orm import Session

from app.models.image import Image


class ImageRepository:
    def __init__(self, db: Session) :
        self.db = db