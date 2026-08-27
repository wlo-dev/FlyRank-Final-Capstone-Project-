from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.image import Image


class ImageRepository:
    def __init__(self, db: Session) :
        self.db = db
        
    def create(self,filename: str, filepath: str) -> Image:
        image = Image(filename=filename, filepath=filepath)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
    
    def get_by_id(self, image_id: int) -> Image | None:
        return self.db.get(Image, image_id)
    
    def get_all(self) -> list[Image]:
        return list(self.db.execute(select(Image)).scalar().all())