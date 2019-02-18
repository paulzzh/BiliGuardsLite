# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了自动扭蛋功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/Capsule.php

import time
import json
from Log import Log
from Curl import Curl
from config import config

class Capsule():

    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["CAPUSLE"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        count = self.info()
        while (count > 0):
            count -= self.open(1)
        
        self.lock = int(time.time()) + 86400
    
    def info(self):
        payload = {}
        data = Curl().get("https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/get_detail",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("扭蛋币余额查询异常")
            return 0

        Log.info("当前还有 %s 枚扭蛋币"%data["data"]["normal"]["coin"])
        
        return data["data"]["normal"]["coin"]

    def open(self,num):
        csrf = config["Token"]["CSRF"]

        payload = {
            "type":"normal",
            "count":num,
            "csrf_token":csrf,
            "csrf":csrf
        }
        data = Curl().nspost("https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/open_capsule",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("扭蛋失败,请稍后重试")
            return 0

        awards=data["data"]["awards"][0]
        if len(awards) != 0:
            Log.info("扭蛋成功,获得 %s 个 %s"%(awards["num"],awards["name"]))

        return True