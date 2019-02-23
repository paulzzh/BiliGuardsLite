# BiliBiliHelper Python Version
# Copy right (c) 2019 TheWanderingCoel
# 不知道为什么,exec_fun总会报错
# 说什么 'controller' object has no attribute 'xxx'
# 干脆直接把所有请求写在一个文件里了

import time
from Log import Log
from config import config
from Base import get_default,msign
from AsyncioCurl import AsyncioCurl

class BasicRequest:

# 小电视,DokiDoki,摩天大楼之类的请求
    @staticmethod
    async def tv_req_check(real_roomid):
        payload = {}
        url = "https://api.live.bilibili.com/gift/v3/smalltv/check?roomid=%s"%real_roomid
        response = await AsyncioCurl().request_json
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

        response = await AsyncioCurl().nspost(url,payload)
        return response
    
    @staticmethod
    async def tv_req_notice(TV_roomid, TV_raffleid):
        url = "https://api.live.bilibili.com/gift/v3/smalltv/notice?type=small_tv&raffleId={%s}"%TV_raffleid
        response = await AsyncioCurl().request_json("GET",url)
        return response
    
# 大航海请求
    @staticmethod
    async def guard_req_check(real_roomid):
        payload = {}
        url = "https://api.live.bilibili.com/lottery/v1/Lottery/check_guard?roomid=%s"%real_roomid
        response = await AsyncioCurl().get(url,payload)
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
        response = await AsyncioCurl().nspost(url,payload)
        return response

# 节奏风暴请求
    @staticmethod
    async def storm_req_check(room_id):
        payload = {}
        url = "https://api.live.bilibili.com/lottery/v1/Storm/check?roomid=%s"%room_id
        response = await AsyncioCurl().get(url,payload)
        return response
    
    @staticmethod
    async def storm_req_join(raffle_id):
        default = get_default()
        temp_params = "access_key=%s&actionKey=%s&appKey=%s&build=%s&device=%s&id=%s&mobi_app=%s&platform=%s&ts=%s"%(default["access_key"],default["actionKey"],default["appkey"],default["build"],default["device"],raffle_id,default["mobi_app"],default["platform"],int(time.time()))
        sign = msign(temp_params)
        url = "https://api.live.bilibili.com/lottery/v1/Storm/join?%s&sign=%s"%(temp_params,sign)
        response = await AsyncioCurl().nsdpost(url)
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