import json
import random
import asyncio
import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Live import Live
from Timer import Timer
from Statistics import Statistics
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest

class TvRaffleHandler:

    @staticmethod
    async def check(real_roomid):
        if not await Live.is_normal_room(real_roomid):
            return
        data = await BasicRequest.tv_req_check(real_roomid)
        checklen = data["data"]["list"]
        list_available_raffleid = []
        for j in checklen:
            raffle_id = j['raffleId']
            raffle_type = j['type']
            time_wanted = j["time_wait"] + int(time.time())

            if not Statistics.is_raffleid_duplicate(raffle_id):
                Log.info("本次获取到的抽奖id为: %s"%raffle_id)
                list_available_raffleid.append((raffle_id,raffle_type,time_wanted))
                Statistics.add2raffle_ids(raffle_id)
        # 暂时没啥用    
        #num_aviable = len(list_available_raffleid)
        for raffle_id,raffle_type,time_wanted in list_available_raffleid:
            Timer.add2list_jobs(TvRaffleHandler.join,time_wanted,(real_roomid,raffle_id,raffle_type))

    @staticmethod
    async def join(real_roomid,raffle_id,raffle_type):
        await Live.enter_room(real_roomid)
        data2 = await BasicRequest.tv_req_join(real_roomid,raffle_id)
        Log.info("参与了房间 %s 的小电视抽奖"%(real_roomid))
        Log.info("小电视抽奖状态: %s"%data2["msg"])
        Statistics.add2joined_raffles("小电视类(合计)")

        code = data2["code"]
        tasklist = []
        if not code:
            await asyncio.sleep(random.randint(170,190))
            task = asyncio.ensure_future(TvRaffleHandler.notice(raffle_id,real_roomid))
            tasklist.append(task)
            await asyncio.wait(tasklist, return_when=asyncio.FIRST_COMPLETED)
        elif code == -500:
            Log.error("-500繁忙,稍后重试")
            return False
        elif code == 400:
            Log.error("当前账号正在小黑屋中")
            return False

    @staticmethod
    async def notice(raffleid,real_roomid):
        data = await BasicRequest.tv_req_notice(real_roomid,raffleid)
        if not data["code"]:
            if data["data"]["gift_id"] == "-1":
                return
            elif data["data"]["gift_id"] != "-1":
                data = data["data"]
                Log.critical("房间 %s 小电视抽奖结果: %s X %s"%(real_roomid,data["gift_name"],data["gift_num"]))
                Statistics.add2results(data["gift_name"],int(data["gift_num"]))