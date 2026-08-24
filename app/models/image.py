# This file defines the SHAPE of an "image" record - like a blank form
# template, not an actual action being performed on any real image.
#
# It doesn't look at photos or talk to any AI model. It just tells
# Python and Postgres: "every image in this system will have these
# exact fields, with these exact types." That agreement is what lets
# the rest of the app safely create, save, and read image records.
#
# Some fields (filename, filepath) are known and filled in immediately
# when an image is first registered. Others (caption, embedding) start
# empty on purpose - they only get filled in later, once the vision
# and embedding pipeline actually processes the image.

from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Image(Base):
    
    __tablename__ = "images" # tells SQLAlchemy the actual table name to create in Postgres
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255),nullable=False)
    
    filepath: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )