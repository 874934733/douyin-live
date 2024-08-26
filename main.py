import logging
from concurrent.futures import ThreadPoolExecutor
from distutils.command.config import config

from fastapi import FastAPI
import uvicorn

from src.dy_live import parseLiveRoomUrl, close_websocket
from src.live_rank import stop_interval_rank
from src.utils.common import RoomIdRequest

# 创建FastAPI应用实例
app = FastAPI()

# 日志配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG)

executor = ThreadPoolExecutor()  # 创建线程池


@app.post("/start_wss_server")
async def receive_code(room_request: RoomIdRequest):
    room_id = room_request.room_id
    logging.info(f"Received code: " + room_id)
    config.LIVE_ROOM_URL = f"https://live.douyin.com/{room_id}"
    logging.info(config.LIVE_ROOM_URL)
    live_status = await parseLiveRoomUrl(config.LIVE_ROOM_URL, room_id)
    if live_status is not None:
        return live_status.dict()
    else:
        return None


@app.post("/stop_wss_server")
async def stop_wss_server(room_request: RoomIdRequest):
    room_id = room_request.room_id
    logging.info(f"Received code: " + room_id)
    await close_websocket(room_id)
    await stop_interval_rank()
    return {"message": "直播已结束"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8110)
