from sqlalchemy import create_engine # function that actually establishes SQLAlchemy's connection machinery to your Postgres database
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Provides one database session per request, then guarantees it's
    closed afterward - even if the request fails partway through.

    This is a generator function (note `yield`, not `return`). FastAPI
    will call this, run everything up to `yield`, hand the session to
    an endpoint via `Depends(get_db)`, let the endpoint do its work,
    then come back and run `db.close()` in the `finally` block.

    Using it in an endpoint looks like:
        def some_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()