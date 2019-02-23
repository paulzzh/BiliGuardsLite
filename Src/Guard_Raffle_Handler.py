import re
import asyncio
import Statistics
from Log import Log
from Live import Live
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest
from config import config

class GuardRaffleHandler:
    @staticmethod
    def target(step):
        if step == 0:
            GuardRaffleHandler.check
        if step == 1:
            GuardRaffleHandler.join
        return None
    
    @staticmethod
    async def check(self,real_roomid,raffle_id=None):
        if not await Live.is_normal_room(real_roomid):
            return
        if raffle_id is not None:
            data = {"data":[{"id":raffle_id,"time": 65}]}
        else:
            for i in range(10):
                data = await BasicRequest.guard_req_check(real_roomid)
                if data["data"]:
                    break
                await asyncio.sleep(1)
            else:
                Log.warning("%s 没有guard或guard已领取"%real_roomid)
                return
            next_step_settings = []
            for j in data["data"]:
                raffle_id = j["id"]
                max_wait = min(j["time"] -15,240)
                if not Statistics.is_raffleid_duplicate(raffle_id):
                    Log.info("本次获取到的抽奖id为 %s"%raffle_id)
                    next_step_setting = (1,(0,max_wait),-2,real_roomid,raffle_id)
                    next_step_settings.append(next_step_setting)
                    Statistics.add2raffle_ids(raffle_id)
            return next_step_settings

    @staticmethod
    async def join(self,real_roomid,raffle_id):
        await Live.is_normal_room(real_roomid)
        data = await BasicRequest.guard_req_join(real_roomid,raffle_id)
        Log.info("参与了房间 %s 的大航海抽奖"%(real_roomid))
        if not data["code"]:
            for award in data["data"]["award_list"]:
                result = re.search("(^获得|^)(.*)<%(\+|X)(\d*)%>", award['name'])
                Statistics.add2results(result.group(2),result.group(4))
            Log.critical("房间 %s 大航海抽奖结果: %s"%(real_roomid,data["data"]["message"]))
            Statistics.add2joined_raffles("大航海(合计)")
        else:
            Log.info(data)