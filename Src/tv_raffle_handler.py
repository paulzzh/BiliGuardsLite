import json
import Statistics
from Log import Log
from Live import Live
from AsyncioCurl import AsyncioCurl

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
    async def check(self,real_roomid):
        if not await Live.is_normal_room(real_roomid):
            return
        data = await self.req_check(real_roomid)
        checklen = data["data"]["list"]
        next_step_settings = []
        for j in checklen:
            raffle_id = j['raffleId']
            raffle_type = j['type']
            max_wait = j['time'] - 15

            if not Statistics.is_raffleid_duplicate(raffle_id):
                Log.info("本次获取到的抽奖id为: %s"%raffle_id)
                next_step_setting = (1, (0, max_wait), -2, real_roomid, raffle_id, raffle_type)
                next_step_settings.append(next_step_setting)
                Statistics.add2raffle_ids(raffle_id)

        return next_step_settings

    @staticmethod
    async def join(self,real_roomid,raffleid,raffle_type):
        await Live.enter_room(real_roomid)
        data2 = await self.req_join(real_roomid,raffleid)
        Log.info("参与了房间 %s 的小电视抽奖"%(real_roomid))
        Log.info("小电视抽奖状态: %s")

        code = data2["code"]
        if not code:
            return (2, (170, 190), raffleid, real_roomid),
        elif code == -500:
            Log.error("-500繁忙,稍后重试")
        elif code == 400:
            Log.error("当前账号正在小黑屋中")
        else:
            return

    @staticmethod
    async def notice(self,raffleid,real_roomid):
        data = await self.req_notice(real_roomid,raffleid)
        if not data["code"]:
            if data["data"]["gift_id"] == "-1":
                return
            elif data["data"]["gift_id"] != "-1":
                data = data["data"]
                Log.critical("房间 %s 小电视抽奖结果: %s X %s"%(real_roomid,data["gift_name"],data["gift_num"]))
                Statistics.add2results(data["gift_name"],data["gift_num"])