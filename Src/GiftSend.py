# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了自动送出即将过期礼物的功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/GiftSend.php

import json
import time
from Log import Log
from Curl import Curl
from config import config

class GiftSend():
    
    def __init__(self):
        self.lock = int(time.time())
        self.uid = 0
        self.ruid = 0
        self.roomid = 0

    def work(self):
        if config["Function"]["GIFTSEND"] == "False":
            return
        if self.lock > int(time.time()):
            return

        if self.ruid == 0:
            self.getRoomInfo()
        
        payload = {}
        data = Curl().get("https://api.live.bilibili.com/gift/v2/gift/bag_list",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("背包查看失败!"+data["message"])
        
        if len(data["data"]["list"]) != 0:
            for each in data["data"]["list"]:
                if each["expire_at"] >= data["data"]["time"] and each["expire_at"] <= data["data"]["time"] + 3600:
                    self.send(each)
                    time.sleep(3)
        
        self.lock = int(time.time()) + 600


    def getRoomInfo(self):
        Log.info("正在生成直播间信息...")

        payload = {}
        data = Curl().get("https://account.bilibili.com/api/myinfo/v2",payload)
        data = json.loads(data)

        if "code" in data and data["code"] != 0:
            Log.warning("获取账号信息失败!"+data["message"])
            Log.warning("清空礼物功能禁用!")
            self.lock = int(time.time()) + 100000000
            return
        
        self.uid = data["mid"]

        payload = {
            "id":config["Live"]["ROOM_ID"]
        }
        data = Curl().get("https://api.live.bilibili.com/room/v1/Room/get_info",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("获取主播房间号失败!"+data["message"])
            Log.warning("清空礼物功能禁用!")
            self.lock = int(time.time()) + 100000000
            return

        Log.info("直播间信息生成完毕!")

        self.ruid = data["data"]["uid"]
        self.roomid = data["data"]["room_id"]

    def send(self,value):
        payload = {
            "coin_type":"silver",
            "gift_id":value["gift_id"],
            "ruid":self.ruid,
            "uid":self.uid,
            "biz_id":self.roomid,
            "gift_num":value["gift_num"],
            "data_source_id":"",
            "data_behavior_id":"",
            "bag_id":value["bag_id"]
        }
        data = Curl().post("https://api.live.bilibili.com/gift/v2/live/bag_send",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("送礼失败!"+data["message"])
        else:
            Log.info("成功向 %s 投喂了 %s 个 %s"%(payload["biz_id"],value["gift_num"],value["gift_name"]))