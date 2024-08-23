import json
import logging
import threading
import time

import requests

from config import DONATION_UUID, LIVE_WEB_SEND_URL, LIVE_HTTP_SEND, LIVE_SEND_INTERVAL
from src.utils.common import GlobalVal
from src.utils.logger import logger

def sender(room_id):
    total_info = f"点赞：{GlobalVal.like_num}, 评论: {GlobalVal.commit_num}, 礼物价值: {GlobalVal.gift_value}"
    logging.info(f"获取到的直播数据是:{total_info}")
    payload = json.dumps({
        "taskuuid": "updatedonation",
        "uuid": DONATION_UUID,
        "applypoint": GlobalVal.like_num,
        "popmsg": GlobalVal.commit_num,
        "giftlist": GlobalVal.gift_value,
        "fannamereadylist": "|".join(GlobalVal.gift_list),
        "donationdetail": json.dumps(GlobalVal.rank_user),
        "room_id": room_id
    })
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        'Content-Type': 'application/json'
    }
    # print(f"推送的直播数据是:{payload}")
    response = requests.request("POST", LIVE_WEB_SEND_URL, headers=headers, data=payload)
    logging.info(f"HTTP推送消息结果: {response.json()}")


def http_send(room_id):
    print("http sender")
    while True:
        time.sleep(LIVE_SEND_INTERVAL)
        # 防止中间重启推送0数据
        try:
            sender(room_id)
        except Exception as e:
            # stopWSServer()
            logging.info(f"推送直播数据出错：如果你不用将直播数据推送到你们的服务器上，可以忽略此提示")


async def send_start(room_id):
    if LIVE_HTTP_SEND:
        # 启动WebSocket客户端
        logger.info(f"开启线程持续发送数据")
        # 阻塞，所以使用线程启动
        t = threading.Thread(target=http_send(room_id))
        t.start()
    else:
        print(f"unopened http senders")
        total_info = f"点赞：{GlobalVal.like_num}, 评论: {GlobalVal.commit_num}, 礼物价值: {GlobalVal.gift_value}"
        print({GlobalVal.rank_user})
        logging.info(f"获取到的直播数据是:{total_info}")
