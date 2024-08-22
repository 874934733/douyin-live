import logging
import threading
import time
from config import LIVE_RANK_INTERVAL, LIVE_RANK_LIST
from src.utils.common import GlobalVal
import requests

# 用于控制循环请求的标志
should_stop = False

def get_rank(room_id):
    url = f"https://live.douyin.com/webcast/ranklist/audience/?aid=6383&app_name=douyin_web&live_id=1&device_platform=web&language=zh-CN&cookie_enabled=true&screen_width=2560&screen_height=1440&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=117.0.0.0&webcast_sdk_version=2450&room_id={room_id}&rank_type=30"
    payload = {}
    headers = {
        'authority': 'live.douyin.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie': 'msToken=SIGjc0nNMCGoBKHwLG2P62wNZehUUEEl1C7DDnOMwjjXUKgF_rFDBLBSqRe6YOnxl3c-tDmAlF7-W3pbYJ8mTxZYfYrLZyK9Q7znbNcuWbfzPBBVNdhEQoOlrakh'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    rank_list = response.json()
    # logger.info(f"[liveRankList] 直播间在线观众排名: {rank_list}")
    # 获取前三名然后只要昵称数据和排名
    ranks_list = rank_list.get("data").get("ranks")[:4]
    ranks_three = []
    for rank in ranks_list:
        ranks_three.append({
            "nickname": rank.get("user").get("nickname"),
            "rank": rank.get("rank")
        })
    # 判断是否存在排名，不存在就是空
    GlobalVal.rank_user = ranks_three
    logging.info(f"更新打赏排行: {ranks_three}")
    print(f"更新打赏排行: {ranks_three}")


def handle_rank(room_id, interval):
    global should_stop
    while not should_stop:
        logging.info(f"处理直播礼物排名，房间ID: {room_id}")
        # 执行处理直播礼物排名的逻辑
        do_rank_logic(room_id)
        time.sleep(interval)

def do_rank_logic(room_id):
    # 实际处理直播礼物排名的逻辑
    pass


def interval_rank(roo_id):
    global should_stop
    logging.info("---------------------------------------->")
    logging.info(f"直播间ID: {roo_id}")
    logging.info(f"间隔 {LIVE_RANK_INTERVAL} 秒更新一次排行")

    if LIVE_RANK_LIST:
        logging.info("开启直播礼物排名")
        rank_t = threading.Thread(target=handle_rank, args=(roo_id, LIVE_RANK_INTERVAL))
        rank_t.start()
    else:
        logging.info("未开启直播礼物排名")

# 停止循环请求
async def stop_interval_rank():
    global should_stop
    should_stop = True
    logging.info("停止直播礼物排名循环请求")


if __name__ == '__main__':
    room_id = "7282911872611830584"
    interval_rank(room_id)
