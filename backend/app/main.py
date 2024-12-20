from contextlib import asynccontextmanager

from app.models.db.database import init_db
from app.routers import refresh
from app.routers import summary_route
from fastapi import FastAPI

app = FastAPI(title="My API Project")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    await init_db()
    yield
    # Shutdown code
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(summary_route.router)
app.include_router(refresh.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to My API!"}
