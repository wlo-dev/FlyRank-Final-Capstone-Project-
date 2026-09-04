from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="FlyRank Image Relevance Engine")

app.include_router(router)