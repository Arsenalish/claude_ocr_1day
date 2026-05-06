import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import upload, expenses, summary

load_dotenv()

app = FastAPI(title="Receipt Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(summary.router, prefix="/api")

# uploads 디렉토리 보장
Path("uploads").mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Receipt Expense Tracker API", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
