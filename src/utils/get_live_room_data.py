import requests

from config import SEND_CODE

# 初始化全局变量：从服务端获取
def init_live_room_data():
    # 定义要发送的数据
    params = {
        "mobile": "18701938401",
        "checkCode": "123456"
    }
    try:
        response = requests.post(SEND_CODE, data=params)
        response.raise_for_status()
        # 解析JSON响应
        data = response.json()
        print(data)
        return data

    except Exception as e:
        print("登陆失败")
