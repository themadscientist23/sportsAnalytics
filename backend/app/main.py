from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.teams import router as teams_router

app = FastAPI(title="Sports Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Sports Analytics API is running."}


app.include_router(teams_router)
