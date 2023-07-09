import dotenv
from fastapi import FastAPI
from loguru import logger
import sys
import uvicorn
from MQ import Queue

logger.remove()
logger.add("MQSrv.log", colorize=True, format="{time} {level}:{level.icon} {message}",
           rotation="00:00", retention="3 days", level="DEBUG", enqueue=True)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{level}:{level.icon} {message}</level>")
srv = FastAPI()
env = dotenv.dotenv_values("./MQSrv.env")
Key = {"MST": env.get("MST"), "OMR": env.get("OMR"), "MathAI": env.get("MathAI"), "KorAI": env.get("KorAI")}
ReverseKey = {v: k for k, v in Key.items()}
logger.debug("Using Authantication Key: {}", str(Key))
queue = Queue()
logger.debug("Successfully initialized queue")


@srv.get("/")
async def root():
    return {"ServerState": "OK"}


@srv.get("/queue")
async def get_queue():
    return {"Data": queue.get_all()}


@srv.get("/dequeue/{to}")
async def get_queue(to: str, key: str):
    if key not in Key.values():
        logger.warning("Invalid key value: {}", key)
        return {"Error": "Invalid key value"}
    if to not in ["MST", "OMR", "MathAI", "KorAI"]:
        logger.warning("Invalid to value: {}", to)
        return {"Error": "Invalid to value"}
    logger.debug("Getting queue data for {} from {}", to, ReverseKey[key])
    return {"Data": queue.dequeue(to)}


@srv.post("/enqueue/{to}")
async def post_queue(to: str, item: str, key: str):
    if key not in Key.values():
        logger.warning("Invalid key value: {}", key)
        return {"Error": "Invalid key value"}
    if to not in ["MST", "OMR", "MathAI", "KorAI"]:
        logger.warning("Invalid to value: {}", to)
        return {"Error": "Invalid to value"}
    queue.enqueue(item, to)
    logger.debug("Enqueued {} to {} from {}", item, to, ReverseKey[key])
    return {"Queue": {"to": to, "item": item, "key": key, "from": ReverseKey[key], "status": "OK"}}


uvicorn.run(srv, host="0.0.0.0", port=8009)
logger.debug("Server started")
