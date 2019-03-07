# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了硬币换银瓜子功能

import time
import json
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Base import std235959
from Curl import Curl
from config import config

class Coin2Silver():
    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["COIN2SILVER"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        self.exchange(config["Coin2Silver"]["COIN"])

        self.lock = std235959() + 600
    
    def exchange(self,num):
        payload = {
            "num":num,
            "csrf_token":config["Token"]["CSRF"]
        }

        data = Curl().nspost("https://api.live.bilibili.com/pay/v1/Exchange/coin2silver",payload)
        data = json.loads(data)
        if data["code"] != 0:
            Log.warning(data["message"])

        Log.info(data["message"]+", %s 枚硬币兑换了 %s 个银瓜子"%(num,data["data"]["silver"]))