import json
from Log import Log
from AsyncioCurl import AsycnioCurl

class Live:
    
    @staticmethod
    async def is_normal_room(self,roomid):
        if not roomid:
            return True
        data = await self.init_room(roomid)
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
    async def is_ok_as_monitor(self,room_id,area_id):
        data = await self.init_room(room_id)
        data = data["data"]
        is_hidden = data["is_hidden"]
        is_locked = data["is_locked"]
        is_encryped = data["encrypted"]
        is_normal = not any((is_hidden,is_locked,is_encryped))

        data = await self.get_room_info(room_id)
        data = data["data"]
        is_open = True if data["live_status"] == 1 else False
        current_area_id = data["parent_area_id"]

        is_ok = (area_id == current_area_id) and is_normal and is_open
        return is_ok


    @staticmethod
    async def init_room(self,roomid):
        payload = {}
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id={%s}"%roomid
        r = await AsycnioCurl().get(url,payload)
        return json.loads(r)

    @staticmethod
    async def get_room_info(self,roomid):
        payload = {}
        url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id={%s}"%roomid
        r = await AsycnioCurl().get(url,payload)
        return json.loads(r)
