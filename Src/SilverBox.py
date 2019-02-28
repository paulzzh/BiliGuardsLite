# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了自动领取银瓜子宝箱的功能

import json
import time
import random
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Curl import Curl
from config import config
from Base import std235959

class SilverBox():
    
    def __init__(self):
        self.lock = int(time.time())
        self.task = 0

    def work(self):
        if config["Function"]["SILVERBOX"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        if self.task == 0:
            self.getTask()
        else:
            self.openTask()
        
    def openTask(self):
        payload = {}
        data = Curl().get("https://api.live.bilibili.com/mobile/freeSilverAward",payload)
        data = json.loads(data)
    
        if data["code"] != 0:
            Log.warning("开启宝箱失败")
            self.lock = int(time.time()) + random.randint(60,120)
            return
    
        Log.info("开始宝箱成功,获得 %s 个银瓜子,当前有 %s 个银瓜子"%(data["data"]["awardSilver"],int(data["data"]["silver"])))
        self.task = 0
        self.lock = int(time.time()) + random.randint(5,20)
    
    
    def getTask(self):
        payload = {}
        data = Curl().get("https://api.live.bilibili.com/lottery/v1/SilverBox/getCurrentTask",payload)
        data = json.loads(data)
        
        if data["code"] == -10017:
            Log.info(data["message"])
            self.lock = std235959()
            return
    
        if data["code"] != 0:
            Log.error("领取宝箱任务失败")
            return

        Log.info("领取宝箱成功,内含 %s 个瓜子"%data["data"]["silver"])
        Log.info("等待 %s 分钟后打开宝箱"%data["data"]["minute"])

        self.task = data["data"]["time_start"]
        self.lock = int(time.time()) + data["data"]["minute"] * 60 + random.randint(5,30)