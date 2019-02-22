import re
import asyncio
import Statistics
from Log import Log
from Live import Live
from AsyncioCurl import AsyncioCurl
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
                data = await self.req_check(real_roomid)
                if data["data"]:
                    break
                await asyncio.sleep(1)
            else:
                Log.warning("%s 没有guard或guard已领取")

    @staticmethod
    async def join(self,real_roomid,raffle_id):
        await Live.is_normal_room(real_roomid)
        data = await self.req_join(real_roomid,raffle_id)
        Log.info("参与了房间 %s 的大航海抽奖")
        if not data["code"]:
            for award in data["data"]["award_list"]:
                result = re.search("(^获得|^)(.*)<%(\+|X)(\d*)%>", award['name'])
                Statistics.add2results(result.group(2),result.group(4))
            Log.critical("房间 %s 大航海抽奖结果: %s")
            Statistics.add2joined_raffles("大航海(合计)")
        else:
            Log.info(data)