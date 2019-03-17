# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了自动扭蛋功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/Capsule.php

import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Curl import Curl
from config import config

class Capsule():

    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["CAPSULE"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        count = self.info()
        while (count > 0):
            count -= self.open(1)
        
        self.lock = int(time.time()) + 86400
    
    def info(self):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/get_detail"
        payload = {}
        data = Curl().request_json("GET",url,headers=config["pcheaders"],params=payload)

        if data["code"] != 0:
            Log.warning("扭蛋币余额查询异常")
            return 0

        Log.info("当前还有 %s 枚扭蛋币"%data["data"]["normal"]["coin"])
        
        return data["data"]["normal"]["coin"]

    def open(self,num):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/open_capsule"
        csrf = config["Token"]["CSRF"]

        payload = {
            "type":"normal",
            "count":num,
            "csrf_token":csrf,
            "csrf":csrf
        }
        data = Curl().request_json("POST",url,headers=config["pcheaders"],data=payload,sign=False)

        if data["code"] != 0:
            Log.warning("扭蛋失败,请稍后重试")
            return 0

        awards=data["data"]["awards"][0]
        if len(awards) != 0:
            Log.info("扭蛋成功,获得 %s 个 %s"%(awards["num"],awards["name"]))

        return True