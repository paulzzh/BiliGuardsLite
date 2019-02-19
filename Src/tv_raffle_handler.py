import json
from Log import Log
from Live import Live
from AsyncioCurl import AsycnioCurl

class TvRaffleHandler:
    @staticmethod
    def target(step):
        # 第一步进行检查
        if step == 0:
            return TvRaffleHandler.check
        # 第二步进行加入
        if step == 1:
            return TvRaffleHandler.join
        # 第三步进行提醒
        if step == 2:
            return TvRaffleHandler.notice
        return None
    
    @staticmethod
    async def check(user,real_roomid):
        if not await Live.is_normal_room(real_roomid):
            return
        payload = {}
        url = "https://api.live.bilibili.com/gift/v3/smalltv/check?roomid={%s}"%real_roomid
        data = await AsycnioCurl().get(url,payload)
        data = json.loads(data)
        checklen = data["data"]["list"]
        next_step_settings = []
        for j in checklen:
            raffle_id = j['raffleId']
            raffle_type = j['type']
            max_wait = j['time'] - 15

        return next_step_settings

    @staticmethod
    async def join(self,real_roomid,raffleid,raffle_type):
        Log.info("参与了房间 %s 的小电视抽奖"%(real_roomid))
        Log.info("小电视抽奖状态: %s")

    @staticmethod
    async def notice(self,real_roomid):
        payload = {}
        url = "https://api.live.bilibili.com/gift/v3/smalltv/notice?type=small_tv&raffleId={%s}"%TV_raffleid
        data = await AsycnioCurl().get(url,payload)
        if not data["code"]:
            if data["data"]["gift_id"] == "-1":
                return
            elif data["data"]["gift_id"] != "-1":
                data = data["data"]
                Log.critical("房间 %s 小电视抽奖结果: %s X %s"%(real_roomid,data["gift_name"],data["gift_num"]))