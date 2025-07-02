from fastapi import FastAPI
from .core.config import settings
from .routers import emails, calendar, auth

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(emails.router, prefix="/emails", tags=["emails"])
app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Taskly API"} 