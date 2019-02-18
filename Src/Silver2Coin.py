# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了银瓜子对换硬币的功能

import time
import json
from Log import Log
from Curl import Curl
from Base import std235959
from config import config

class Silver2Coin():
    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["SILVER2COIN"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        self.exchange()

        self.lock = std235959() + 600
    
    def exchange(self):
        payload = {}
        data = Curl().get("https://api.live.bilibili.com/pay/v1/Exchange/silver2coin",payload)
        data = json.loads(data)
        
        if data["code"] == 403:
            Log.warning(data["message"]+"硬币")
            return
        
        Log.info(data["message"]+",兑换了一枚硬币")