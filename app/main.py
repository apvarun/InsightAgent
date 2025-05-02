from fastapi import FastAPI

from .routers import items

app = FastAPI(dependencies=[])


app.include_router(items.router)


@app.get("/health")
async def root():
    return {"status": "ok"}
