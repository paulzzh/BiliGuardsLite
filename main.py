import sys
sys.path.append("Src")
import time
from Log import Log
from Auth import Auth
from Capsule import Capsule
from GiftSend import GiftSend
from Group import Group
from Heart import Heart
from SilverBox import SilverBox
from Task import Task
from Sentence import Sentence
from config import config

# 初始化所有class
Auth = Auth()
Capsule = Capsule()
GiftSend = GiftSend()
Group = Group()
Heart = Heart()
SilverBox = SilverBox()
Task = Task()

if config["Other"]["INFO_MESSAGE"] != "False":
    Log.info("BiliBiliHelper Python Version Beta 0.0.1")
if config["Other"]["SENTENCE"] != "False":
    Log.info(Sentence().get_sentence())

while (1):
    Auth.work()
    Capsule.work()
    GiftSend.work()
    Group.work()
    Heart.work()
    SilverBox.work()
    Task.work()
    # 休息0.5s,减少CPU占用
    time.sleep(0.5)