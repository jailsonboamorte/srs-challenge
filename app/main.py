from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from constants import ENV
from routers.v1 import producers_router, farms_router

api = FastAPI(root_path=f"/{ENV}")

api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# /V1
v1 = "/v1"
api.include_router(producers_router.router, prefix=v1)
api.include_router(farms_router.router, prefix=v1)


@api.get("/")
async def health_check() -> dict:
    return {"Welcome to": "Serasa World"}
