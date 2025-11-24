from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import memos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI backend!"}

app.include_router(memos.router, prefix="/api", tags=["memos"])