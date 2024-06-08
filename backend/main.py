import time
import uvicorn
import configparser
import logging
import logging.config
from math import ceil
from app.api.api_v1.api import api
from app.core.settings import settings
from app.core.db_init import redis_connection
from fastapi import FastAPI, Request, Response, HTTPException
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter

config = configparser.ConfigParser()
config.read(settings.LOGGING_INI)
config["handler_fileHandler"][
    "args"
] = f"('{settings.LOG_FILE_NAME}', {settings.LOG_FILE_SIZE}, {settings.LOG_FILE_BACKUP})"
config.set("handler_LogtailHandler", "args", f"('{settings.LOGGING_PLATFORM_TOKEN}',)")
with open(settings.LOGGING_INI, "w") as configfile:
    config.write(configfile)
logging.config.fileConfig(fname=settings.LOGGING_INI)
logger = logging.getLogger(__name__)


async def custom_callback(request: Request, response: Response, pexpire: int):
    expire = ceil(pexpire / 1000)
    raise HTTPException(
        status_code=492, detail=f"Too Many Requests. Retry after {expire} seconds."
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    await FastAPILimiter.init(redis=redis_connection, http_callback=custom_callback)
    logger.info("<<<Staring API server...>>>")
    yield
    logger.info("<<<Shuting down API server...>>>")
    await FastAPILimiter.close()


app = FastAPI(
    title="Fickel",
    description="This platform is used to connect people with problemstatment and the developers who have capablity to work on those problemstatments. ",
    version="1.0.0",
    contact={
        "name": "Amirdhesh S",
        "url": "https://amirdhesh.onrender.com/",
        "email": "amirdhesh2003@gmail.com",
    },
    lifespan=lifespan,
)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    try:
        start_time: time = time.time()
        response = await call_next(request)
        process_time: time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        log_dict = {
            "URL": request.url.path,
            "Method": request.method,
            "Process_time": process_time,
        }
        logger.info(log_dict)
        return response
    except Exception as e:
        logger.error(str(e))


app.include_router(api)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
