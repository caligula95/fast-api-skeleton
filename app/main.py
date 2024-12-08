import time
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.config import config
from app.models.enums.tags import Tags
from app.routers import users
from app.helpers.openapi import open_api

DEFAULT_CLIENT = 'web'
DEFAULT_VERSION = '0'

scheduler = AsyncIOScheduler(timezone=timezone(offset=timedelta(hours=-7)))

def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config['ALLOWED_ORIGINS'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     scheduler.start()
#     yield
#     scheduler.shutdown()


app = FastAPI()
app.debug = config['DEBUG_OUTPUT']
app.title = open_api['app_title']
app.summary = open_api['app_summary']
app.description = open_api['app_description']
app.version = open_api['app_version']
app.openapi_tags = open_api['tags']

setup_middlewares(app)


def include_routers(app: FastAPI):
    app.include_router(users.router)


include_routers(app)


@app.middleware("http")
async def add_process_time_header(
        request: Request,
        call_next,
):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def get_client_headers(
        request: Request,
        call_next,
):
    client = request.headers.get("X-Client-Type", DEFAULT_CLIENT)
    version = request.headers.get("X-Client-Version", DEFAULT_VERSION)
    token = request.headers.get("Authorization", '')
    background_tasks = BackgroundTasks()
    # background_tasks.add_task(store_headers, token=token, client=client, version=version)
    response = await call_next(request)
    response.background = background_tasks
    return response


@app.get("/ping", tags=[Tags.public])
async def ping():
    return {
        "time": datetime.now(),
        "time_utc": datetime.now(timezone.utc),
        "time_pacific": datetime.now(timezone(offset=timedelta(hours=-7)))
    }