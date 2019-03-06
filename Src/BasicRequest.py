# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 直接把所有请求写在一个文件里了

import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from config import config
from Base import get_default,msign
from AsyncioCurl import AsyncioCurl

class BasicRequest:

# 小电视,DokiDoki,摩天大楼之类的请求
    @staticmethod
    async def tv_req_check(real_roomid):
        url = "https://api.live.bilibili.com/gift/v3/smalltv/check?roomid=%s"%real_roomid
        response = await AsyncioCurl().request_json("GET",url)
        return response
    
    @staticmethod
    async def tv_req_join(real_roomid,TV_raffleid):
        url = "https://api.live.bilibili.com/gift/v3/smalltv/join"
        payload = {
            "roomid": real_roomid,
            "raffleId": TV_raffleid,
            "type": "Gift",
            "csrf_token": ""
        }

        response = await AsyncioCurl().request_json("POST",url,data=payload,headers=config["pcheaders"])
        return response
    
    @staticmethod
    async def tv_req_notice(TV_roomid, TV_raffleid):
        url = "https://api.live.bilibili.com/gift/v3/smalltv/notice?type=small_tv&raffleId=%s"%TV_raffleid
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response
    
# 大航海请求
    @staticmethod
    async def guard_req_check(real_roomid):
        url = "https://api.live.bilibili.com/lottery/v1/Lottery/check_guard?roomid=%s"%real_roomid
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response

    @staticmethod
    async def guard_req_join(real_roomid,raffle_id):
        url = "https://api.live.bilibili.com/lottery/v2/Lottery/join"
        payload = {
            "roomid": real_roomid,
            "id": raffle_id,
            "type": "guard",
            "csrf_token": config["Token"]["CSRF"]
        }
        response = await AsyncioCurl().request_json("POST",url,data=payload,headers=config["pcheaders"])
        return response

# 节奏风暴请求
    @staticmethod
    async def storm_req_check(room_id):
        url = "https://api.live.bilibili.com/lottery/v1/Storm/check?roomid=%s"%room_id
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response
    
    @staticmethod
    async def storm_req_join(raffle_id):
        default = get_default()
        temp_params = "access_key=%s&actionKey=%s&appKey=%s&build=%s&device=%s&id=%s&mobi_app=%s&platform=%s&ts=%s"%(default["access_key"],default["actionKey"],default["appkey"],default["build"],default["device"],raffle_id,default["mobi_app"],default["platform"],int(time.time()))
        sign = msign(temp_params)
        url = "https://api.live.bilibili.com/lottery/v1/Storm/join?%s&sign=%s"%(temp_params,sign)
        response = await AsyncioCurl().request_json("POST",url,headers=config["pcheaders"])
        return response

# Live.py 请求
    @staticmethod
    async def init_room(roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id=%s"%roomid
        response = await AsyncioCurl().request_json("GET",url)
        return response

    @staticmethod
    async def get_room_info(roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s"%roomid
        response = await AsyncioCurl().request_json("GET",url)
        return response

    @staticmethod
    async def get_room_by_area(areaid):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=%s&cate_id=0&area_id=0&sort_type=online&page=1&page_size=15"%areaid
        response = await AsyncioCurl().request_json("GET",url)
        return response

    @staticmethod
    async def req_fetch_user_info():
        url = "https://api.live.bilibili.com/i/api/liveinfo"
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response
    
    @staticmethod
    async def req_fetch_bag_list():
        url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response

    @staticmethod
    async def req_fetch_medal():
        url = "https://api.live.bilibili.com/i/api/medal?page=1&pageSize=50"
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response

    @staticmethod
    async def req_check_taskinfo():
        url = "https://api.live.bilibili.com/i/api/taskInfo"
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response

    @staticmethod
    async def req_send_danmu(msg,roomId):
        url = "https://api.live.bilibili.com/msg/send"
        data = {
            "color": "16777215",
            "fontsize": "25",
            "mode": "1",
            "msg": msg,
            "rnd": "0",
            "roomid": int(roomId),
            "csrf_token": config["Token"]["CSRF"],
            "csrf": config["Token"]["CSRF"]
        }
        response = await AsyncioCurl().request_json("POST",url,data=data,headers=config["pcheaders"])
        return response
    
    @staticmethod
    async def req_send_gift(giftid,giftnum,bagid,ruid,biz_id):
        url = "https://api.live.bilibili.com/gift/v2/live/bag_send"
        data = {
            "uid": config["Token"]["UID"],
            "gift_id": giftid,
            "ruid": ruid,
            "gift_num": giftnum,
            "bag_id": bagid,
            "platform": "pc",
            "biz_code": "live",
            "biz_id": biz_id,
            "rnd": int(time.time()),
            "storm_beat_id": "0",
            "metadata": "",
            "price": "0",
            "csrf_token": config["Token"]["CSRF"]
        }
        response = await AsyncioCurl().request_json("POST",url,data=data,headers=config["pcheaders"])
        return response

    @staticmethod
    async def req_fetch_liveuser_info(real_roomid):
        url = "https://api.live.bilibili.com/live_user/v1/UserInfo/get_anchor_in_room?roomid=%s"%real_roomid
        response = await AsyncioCurl().request_json("GET",url)
        return response

    @staticmethod
    async def req_fetch_fan(real_roomid,uid):
        url = "https://api.live.bilibili.com/rankdb/v1/RoomRank/webMedalRank?roomid=%s&ruid=%s"%(real_roomid,uid)
        response = await AsyncioCurl().request_json("GET",url)
        return response

    @staticmethod
    async def req_fetch_capsule_info():
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/get_detail"
        response = await AsyncioCurl().request_json("GET",url,headers=config["pcheaders"])
        return response

    @staticmethod
    async def req_open_capsule(count):
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/capsule/open_capsule"
        data = {
            "type":"normal",
            "count":count,
            "csrf_token":config["Token"]["CSRF"],
            "csrf":config["Token"]["CSRF"]
        }
        response = await AsyncioCurl().request_json("POST",url,data=data,headers=config["pcheaders"])
        return response