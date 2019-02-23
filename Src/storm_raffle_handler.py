import time
import Statistics
from Log import Log
from Base import msign,get_default
from Live import Live
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest

class StormRaffleHandler:
    @staticmethod
    def target(step):
        if step == 0:
            return StormRaffleHandler.check
        if step == 1:
            return StormRaffleHandler.join

    @staticmethod
    async def check(self,room_id,raffle_id=None):
        if not await Live.is_normal_room(room_id):
            return
        if raffle_id is not None:
            data = {data: {"id": raffle_id}}
        else:
            data = await BasicRequest.storm_req_check(room_id)
        next_step_settings = []
        data = data["data"]
        if data:
            raffle_id = data["id"]
            if not Statistics.is_raffleid_duplicate(raffle_id):
                Log.info("本次获取到的抽奖id为 %s")
                next_step_setting = (1,(1,3),-2,room_id,raffle_id)
                next_step_settings.append(next_step_setting)

                next_step_setting = (1, (2, 4), -2, room_id, raffle_id)
                next_step_settings.append(next_step_setting)

                Statistics.add2raffle_ids(raffle_id)
        return next_step_settings
    
    @staticmethod
    async def join(self,room_id,raffle_id):
        await Live.enter_room(room_id)
        data = await BasicRequest.storm_req_join(raffle_id)
        Statistics.add2joined_raffles("节奏风暴(合计)")
        if not data["code"]:
            data = data["data"]
            gift_name = data["gift_name"]
            gift_num = data["gift_num"]
            Log.critical("房间 %s 节奏风暴抽奖结果: %s X %s")
            Statistics.add2results(gift_name,gift_num)
            return