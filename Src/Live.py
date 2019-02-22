import json
import random
import controller
from BasicRequest import BasicRequest
from Log import Log
from config import config
from AsyncioCurl import AsyncioCurl

class Live:

    @staticmethod
    async def enter_room(room_id):
        if not room_id:
            return
        data = {
            "room_id":room_id,
            "csrf_token": config["Token"]["CSRF"]
        }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = await AsyncioCurl().nspost(url,data)
        return response

    async def is_normal_room(roomid):
        if not roomid:
            return True
        data = await BasicRequest.init_room(roomid)
        if not data["code"]:
            data = data["code"]
            param1 = data["is_hidden"]
            param2 = data["is_locked"]
            param3 = data["encrypted"]
            # 如果三个中有一个是True
            if any((param1,param2,param3)):
                Log.warning("抽奖脚本检测到房间 %s 为异常房间"%roomid)
                return False
            # 否则
            else:
                Log.info("抽奖脚本检测到房间 %s 为正常房间"%roomid)
                return True

    @staticmethod
    async def get_room_by_area(area_id,room_id=None):
        
        if room_id is not None and room_id:
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
    
        if area_id == 1:
            room_id = 23058
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
            
        while True:
            print("test")
            data = await BasicRequest.get_room_by_area(area_id)
            print("hi coel!")
            data = data["data"]
            room_id = random.choice(data)["roomid"]
            print("ttst")
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
    
    @staticmethod
    async def is_ok_as_monitor(room_id,area_id):
        Log.debug("EXEC: is_ok_as_monitor")
        data = await BasicRequest.init_room(room_id)
        data = data["data"]
        is_hidden = data["is_hidden"]
        is_locked = data["is_locked"]
        is_encryped = data["encrypted"]
        is_normal = not any((is_hidden,is_locked,is_encryped))

        data = await BasicRequest.get_room_info(room_id)
        data = data["data"]
        is_open = True if data["live_status"] == 1 else False
        current_area_id = data["parent_area_id"]

        is_ok = (area_id == current_area_id) and is_normal and is_open
        return is_ok