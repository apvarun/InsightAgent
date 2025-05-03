from fastapi import FastAPI

from .routers import insight

app = FastAPI(dependencies=[])


app.include_router(insight.router)


@app.get("/health")
async def root():
    return {"status": "ok"}
