import uvicorn
from app.database import init_models
from app.routers import statistics
from fastapi import FastAPI

app = FastAPI()
app.include_router(statistics.router)


@app.on_event("startup")
async def init_db() -> None:
    await init_models()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
