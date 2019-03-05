import sys
sys.path.append("Src")
import time
import asyncio
import Console
import threading
import Danmu_Monitor
from raffle_handler import RaffleHandler
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Auth import Auth
from Capsule import Capsule
from GiftSend import GiftSend
from Group import Group
from Heart import Heart
from SilverBox import SilverBox
from Statistics import Statistics
from Task import Task
from Sentence import Sentence
from Timer import Timer
from config import config

# 初始化所有class
Auth = Auth()
Capsule = Capsule()
GiftSend = GiftSend()
Group = Group()
Heart = Heart()
SilverBox = SilverBox()
Task = Task()
rafflehandler = RaffleHandler()

if config["Other"]["INFO_MESSAGE"] != "False":
    Log.info("BiliBiliHelper Python Version Beta 0.0.1")
if config["Other"]["SENTENCE"] != "False":
    Log.info(Sentence().get_sentence())

loop = asyncio.get_event_loop()

timer = Timer(loop)
console = Console.Console(loop)

area_ids = [1,2,3,4,5,6,]
Statistics(len(area_ids))
danmu_tasks = [Danmu_Monitor.run_Danmu_Raffle_Handler(i) for i in area_ids]
other_tasks = [
    rafflehandler.run()
]

console_thread = threading.Thread(target=console.cmdloop)
console_thread.start()

# 先登陆一次,防止速度太快导致抽奖模块出错
Auth.work()

def daily_job():
    while (1):
        Auth.work()
        Capsule.work()
        #GiftSend.work()
        Group.work()
        Heart.work()
        SilverBox.work()
        Task.work()
        # 休息0.5s,减少CPU占用
        time.sleep(0.5)

daily_job_thread = threading.Thread(target=daily_job)
daily_job_thread.start()

loop.run_until_complete(asyncio.wait(danmu_tasks+other_tasks))

console_thread.join()
daily_job_thread.join()

loop.close()