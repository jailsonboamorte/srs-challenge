from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from startup import init_db
from mangum import Mangum
import uvicorn

from constants import ENV
from routers.v1 import producers_router, farms_router, crops_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield init_db()


api = FastAPI(lifespan=lifespan, root_path=f"/{ENV}")

api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# /V1
v1 = "/v1"
api.include_router(producers_router.router, prefix=v1)
api.include_router(farms_router.router, prefix=v1)
api.include_router(crops_router.router, prefix=v1)


@api.get("/")
async def health_check() -> dict:
    return {"Welcome to": "Serasa World"}


handler = Mangum(api)

if __name__ == "__main__":
    uvicorn.run(api, port=8000, reload=True)
