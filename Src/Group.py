# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 该代码实现了应援团签到功能
# 代码根据metowolf大佬的PHP版本进行改写
# PHP代码地址:https://github.com/metowolf/BilibiliHelper/blob/0.9x/src/plugins/Group.php

import json
import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Curl import Curl
from Base import std235959
from config import config

class Group():

    def __init__(self):
        self.lock = int(time.time())

    def work(self):
        if config["Function"]["GROUP"] == "False":
            return
        if self.lock > int(time.time()):
            return
        
        groups = self.getList()
        count = len(groups)
        for each in groups:
            count -= self.signIn(each)

        if count == 0:
            self.lock = std235959()
        else:
            self.lock = int(time.time()) + 3600

    def getList(self):
        payload = {}
        data = Curl().get("https://api.vc.bilibili.com/link_group/v1/member/my_groups",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("查询应援团名单异常")
            return []
        
        if len(data["data"]["list"]) == 0:
            Log.info("没有需要签到的应援团")
            return []
        
        return data["data"]["list"]

    def signIn(self,value):
        payload = {
            "group_id":value["group_id"],
            "owner_id":value["owner_uid"]
        }
        data = Curl().post("https://api.vc.bilibili.com/link_setting/v1/link_setting/sign_in",payload)
        data = json.loads(data)

        if data["code"] != 0:
            Log.warning("应援团 %s 签到异常"%value["group_name"])
            return False

        if data["data"]["status"] != 0:
            Log.info("应援团 %s 已经签到过了"%value["group_name"])
        else:
            Log.info("应援团 %s 签到成功,增加 %s 点亲密度"%(value["group_name"],data["data"]["add_num"]))
        
        return True