from sqlalchemy import create_engine # function that actually establishes SQLAlchemy's connection machinery to your Postgres database
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)