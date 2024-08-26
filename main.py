import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from distutils.command.config import config

from fastapi import FastAPI
import uvicorn

from src.dy_live import parseLiveRoomUrl
from src.live_rank import stop_interval_rank
from src.utils.common import RoomIdRequest
from src.utils.http_send import send_start

# 创建FastAPI应用实例
app = FastAPI()

# 日志配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG)

executor = ThreadPoolExecutor()  # 创建线程池


@app.post("/receive_code")
async def receive_code(room_request: RoomIdRequest):
    room_id = room_request.room_id
    logging.info(f"Received code: " + room_id)
    config.LIVE_ROOM_URL = f"https://live.douyin.com/{room_id}"
    logging.info(config.LIVE_ROOM_URL)
    # 使用线程池执行同步的 init_global 函数
    # await asyncio.get_running_loop().run_in_executor(executor, init_global(room_id))
    # 使用线程池执行同步的 send_start 函数
    # await asyncio.get_running_loop().run_in_executor(executor, send_start(room_id))
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    live_status = await parseLiveRoomUrl(config.LIVE_ROOM_URL, room_id)
    if live_status is not None:
        return live_status.dict()
    else:
        return None


@app.post("/stop_wss_server")
async def stop_wss_server():
    # await stopWSServer()
    await stop_interval_rank()
    return {"message": "直播已结束"}


if __name__ == '__main__':
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    # dy_live.parseLiveRoomUrl(LIVE_ROOM_URL)
    # 运行Flask应用
    uvicorn.run(app, host="192.168.0.109", port=8001)
