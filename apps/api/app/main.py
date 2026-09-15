from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.api.routers import (
    auth,
    business_goals,
    health,
    projects,
    requirements,
    stakeholders,
    use_cases,
    user_stories,
)
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(stakeholders.router, prefix="/api")
app.include_router(business_goals.router, prefix="/api")
app.include_router(requirements.router, prefix="/api")
app.include_router(use_cases.router, prefix="/api")
app.include_router(user_stories.router, prefix="/api")
