import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from distutils.command.config import config
from logging import Logger

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from config import LIVE_ROOM_URL
from src import dy_live
from src.dy_live import parseLiveRoomInfo, stopWSServer
from src.live_rank import stop_interval_rank
from src.utils.common import init_global
from src.utils.http_send import send_start

# 创建FastAPI应用实例
app = FastAPI()

# 日志配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG)


class CodeRequest(BaseModel):
    code: str


executor = ThreadPoolExecutor()  # 创建线程池

@app.post("/receive_code")
async def receive_code(code_request: CodeRequest):
    code = code_request.code
    logging.info(f"Received code: "+code)
    # 使用线程池执行同步的 init_global 函数
    # await asyncio.get_running_loop().run_in_executor(executor, init_global)
    # 使用线程池执行同步的 send_start 函数
    # await asyncio.get_running_loop().run_in_executor(executor, send_start)
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    config.LIVE_ROOM_URL = f"https://live.douyin.com/{code}"
    logging.info(config.LIVE_ROOM_URL)
    live_status = await parseLiveRoomInfo(config.LIVE_ROOM_URL)
    logging.info(live_status)
    # if live_status.get("status") == "4":
        # 如果直播已结束，返回特定的消息
        # return {"message": "直播已结束"}

    return live_status


@app.post("/stop_wss_server")
async def stop_wss_server():
    await stopWSServer()
    await stop_interval_rank()
    return {"message": "直播已结束"}

if __name__ == '__main__':
    # 在config.py配置中修改直播地址: LIVE_ROOM_URL
    # dy_live.parseLiveRoomUrl(LIVE_ROOM_URL)
    # 运行Flask应用
    uvicorn.run(app, host="192.168.0.109", port=8001)
