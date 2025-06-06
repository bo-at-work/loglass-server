from fastapi import FastAPI

from app.routers import chromsizes, tilesets

app = FastAPI(
    title="Loglass FastAPI Clone",
    description="A FastAPI clone of HiGlass server tileset API functionality (MVP).",
    version="0.1.0",
)

app.include_router(tilesets.router)
app.include_router(chromsizes.router)


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the Loglass FastAPI Clone. See /docs for API documentation."}
