from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.config import config
from app.config.logger import setup_logging
from app.io.web.routers import furniture_segmentation_router
from app.furniture_segmentation_service_container import initialize_furniture_segmentation_service

setup_logging()

app = FastAPI(
    title=config.app.PROJECT_NAME,
    version=config.app.VERSION,
    docs_url=config.app.DOCS_URL,
    openapi_url=config.app.OPENAPI_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix='')


@api_router.get("/healthz")
async def healthcheck() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@api_router.on_event("startup")
async def startup():
    await initialize_furniture_segmentation_service()
    global service_is_ready
    service_is_ready = True


api_router.include_router(furniture_segmentation_router)
app.include_router(api_router)
