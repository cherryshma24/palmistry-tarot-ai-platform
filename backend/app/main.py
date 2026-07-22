from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.database.connection import engine
from app.database.base import Base
from app.models.user import User
from app.auth.register import router as register_router  # <-- Add this
from app.auth.login import router as login_router
from app.auth.profile import router as profile_router
from app.palm.router import router as palm_router
from app.tarot.router import router as tarot_router
from app.report.router import router as report_router
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Palmistry & Tarot Intelligence Platform",
    description="AI-powered platform for Palmistry and Tarot Reading",
    version="1.0.0"
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Register API
app.include_router(register_router) 
app.include_router(login_router)
app.include_router(api_router)
app.include_router(profile_router)
app.include_router(palm_router)  
app.include_router(tarot_router)
app.include_router(report_router)# <-- Add this

@app.get("/")
def home():
    return {
        "message": "Welcome to Palmistry & Tarot Intelligence Platform"
    }