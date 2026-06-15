from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.scheduler import scheduler, ingest_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(ingest_job, "interval", hours=6, id="ingest_costs")
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="AWS Cost Guardian",
    version="0.1.0",
    description="Monitor de costos AWS amb alertes i notificacions.",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "AWS Cost Guardian està actiu"}
