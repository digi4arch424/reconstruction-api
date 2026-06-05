from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config   import settings
from database import engine
from routers  import sessions, reconstructions


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Spatial Recon API",
    version="0.1.0",
    description="Walking skeleton API — browser capture → reconstruction pipeline",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", tags=["system"])
async def health():
    return {
        "status":      "ok",
        "version":     "0.1.0",
        "environment": settings.environment
    }


app.include_router(sessions.router,        prefix="/sessions",        tags=["sessions"])
app.include_router(reconstructions.router, prefix="/reconstructions", tags=["reconstructions"])
