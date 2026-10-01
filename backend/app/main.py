from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.teams import router as teams_router
from app.core.config import CORS_ORIGINS

app = FastAPI(title="Sports Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Sports Analytics API is running."}


app.include_router(teams_router)
