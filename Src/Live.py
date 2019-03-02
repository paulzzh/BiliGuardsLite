import json
import random
from Base import adjust_for_chinese
from BasicRequest import BasicRequest
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from config import config
from AsyncioCurl import AsyncioCurl

class Live:

    @staticmethod
    async def enter_room(room_id):
        if not room_id:
            return
        data = {
            "room_id":room_id,
            "csrf_token": config["Token"]["CSRF"]
        }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = await AsyncioCurl().request_json("POST",url,data=data,headers=config["pcheaders"])
        return response

    async def is_normal_room(roomid):
        if not roomid:
            return True
        data = await BasicRequest.init_room(roomid)
        if not data["code"]:
            data = data["data"]
            param1 = data["is_hidden"]
            param2 = data["is_locked"]
            param3 = data["encrypted"]
            # 如果三个中有一个是True
            if any((param1,param2,param3)):
                Log.warning("抽奖脚本检测到房间 %s 为异常房间"%roomid)
                return False
            # 否则
            else:
                Log.info("抽奖脚本检测到房间 %s 为正常房间"%roomid)
                return True

    @staticmethod
    async def get_room_by_area(area_id,room_id=None):

        if room_id is not None and room_id:
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
    
        if area_id == 1:
            room_id = 23058
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
            
        while True:
            data = await BasicRequest.get_room_by_area(area_id)
            data = data["data"]
            room_id = random.choice(data)["roomid"]
            if await Live.is_ok_as_monitor(room_id,area_id):
                Log.info("%s 号弹幕监控选择房间 %s"%(area_id,room_id))
                return room_id
    
    @staticmethod
    async def is_ok_as_monitor(room_id,area_id):
        data = await BasicRequest.init_room(room_id)
        data = data["data"]
        is_hidden = data["is_hidden"]
        is_locked = data["is_locked"]
        is_encryped = data["encrypted"]
        is_normal = not any((is_hidden,is_locked,is_encryped))

        data = await BasicRequest.get_room_info(room_id)
        data = data["data"]
        is_open = True if data["live_status"] == 1 else False
        current_area_id = data["parent_area_id"]

        is_ok = (area_id == current_area_id) and is_normal and is_open
        return is_ok

    @staticmethod
    async def fetch_user_info():
        data = await BasicRequest.req_fetch_user_info()
        Log.info("查询用户信息...")
        if not data["code"]:
            data = data["data"]
            userInfo = data["userInfo"]
            userCoinInfo = data["userCoinInfo"]
            uname = userInfo["uname"]
            achieve = data["achieves"]
            user_level = userCoinInfo["user_level"]
            silver = userCoinInfo["silver"]
            gold = userCoinInfo["gold"]
            identification = bool(userInfo["identification"])
            mobile_verify = bool(userInfo["mobile_verify"])
            user_next_level = userCoinInfo["user_next_level"]
            user_intimacy = userCoinInfo["user_intimacy"]
            user_next_intimacy = userCoinInfo["user_next_intimacy"]
            user_level_rank = userCoinInfo["user_level_rank"]
            billCoin = userCoinInfo["coins"]
            bili_coins = userCoinInfo["bili_coins"]
            Log.info("用户名:"+uname)
            Log.info(f"手机认证状态 {mobile_verify} | 实名认证状态 {identification}")
            Log.info("银瓜子:"+silver)
            Log.info("金瓜子:"+gold)
            Log.info("硬币数:"+billCoin)
            Log.info("B币数:"+bili_coins)
            Log.info("成就值:"+achieve)
            Log.info("等级值:"+user_level+"———>"+user_next_level)
            Log.info("经验值:"+user_intimacy)
            Log.info("剩余值:"+user_next_intimacy-user_next_intimacy)
            arrow = int(user_intimacy * 30 / user_next_intimacy)
            line = 30 - arrow
            percent = user_intimacy / user_next_intimacy * 100.0
            process_bar = "# [" + ">" * arrow + "-" * line + "]" + "%.2f" % percent + "%"
            Log.info(process_bar)
            Log.info("等级榜:"+user_level_rank)

    @staticmethod
    async def fetch_bag_list(verbose=False,bagid=None,show=True):
        data = await BasicRequest.req_fetch_bag_list()
        gift_list = []
        if show:
            Log.info("查询可用礼物...")
        for i in data:
            bag_id = i["bag_id"]
            gift_id = i["gift_id"]
            gift_num = i["gift_num"]
            gift_name = i["gift_name"]
            expireat  = i["expire_at"]
            left_time = (expireat - data["data"]["time"])
            if not expireat:
                left_days = "+∞".center(6)
                left_time = None
            else:
                left_days = round(left_time / 86400,1)
            if bagid is not None:
                if bag_id == int(bagid):
                    return gift_id,gift_num
            else:
                if verbose:
                    Log.info(f"编号为 {bag_id} 的 {gift_name:^3} X {gift_num:^4} (在 {left_days:^6} 天后过期)")
                elif show:
                    Log.info(f" {gift_name:^3} X {gift_num:^4} (在 {left_days:^6} 后过期")
                
            gift_list.append([gift_id,gift_num,bag_id,left_time])
            return gift_list
    
    @staticmethod
    async def check_taskinfo():
        data = await BasicRequest.req_check_taskinfo()
        if not data["code"]:
            data = data["data"]
            double_watch_info = data["double_watch_info"]
            sign_info = data["sign_info"]
        
        if double_watch_info["status"] == 1:
            Log.warning("双端观看直播已完成，但未领取奖励")
        elif double_watch_info["status"] == 2:
            Log.info("双端观看直播已完成，已经领取奖励")
        else:
            Log.warning("双端观看直播未完成")
            if double_watch_info["web_watch"] == 1:
                Log.info("网页端观看任务已完成")
            else:
                Log.warning("网页端观看任务未完成")

            if double_watch_info["mobile_watch"] == 1:
                Log.info("移动端观看任务已完成")
            else:
                Log.warning("移动端观看任务未完成")
        
        if sign_info["status"] == 1:
            Log.info("每日签到已完成")
        else:
            Log.warning("每日签到未完成")
        
    @staticmethod
    async def fetch_medal(show=True,list_wanted_mendal=None):
        printlist = []
        list_medal = []
        if show:
            printlist.append("查询勋章信息")
            printlist.append("{} {} {:^12} {:^10} {} {:^6} {}".format(adjust_for_chinese("勋章"), adjust_for_chinese("主播昵称"), "亲密度", "今日的亲密度", adjust_for_chinese("排名"), "勋章状态", "房间号码"))
        dic_worn = {"1":"正在佩戴","0":"待机状态"}
        data = await BasicRequest.req_fetch_medal()
        if not data["code"]:
            for i in data["data"]["fansMedalList"]:
                if "roomid" in i:
                    list_medal.append((i["roomid"], int(i["dayLimit"]) - int(i["todayFeed"]), i["medal_name"], i["level"]))
                    if show:
                        printlist.append("{} {} {:^14} {:^14} {} {:^6} {:^9}".format(adjust_for_chinese(i["medal_name"] + "|" + str(i["level"])), adjust_for_chinese(i["anchorInfo"]["uname"]), str(i["intimacy"]) + "/" + str(i["next_intimacy"]), str(i["todayFeed"]) + "/" + str(i["dayLimit"]), adjust_for_chinese(str(i["rank"])), dic_worn[str(i["status"])], i["roomid"]))
        if show:
            Log.info(printlist)
        if list_wanted_mendal is not None:
            list_return_medal = []
            for roomid in list_wanted_mendal:
                for i in list_medal:
                    if i[0] == roomid:
                        list_return_medal.append(i[:3])
                        break
        else:
            list_return_medal = [i[:3] for i in sorted(list_medal,key=itemgetter(3),reverse=True)]
        return list_return_medal

    @staticmethod
    async def send_danmu(msg,roomId):
        data = await BasicRequest.req_send_danmu(msg,roomId)
        Log.info(data)

    @staticmethod
    async def check_room(roomid):
        data = await BasicRequest.init_room(roomid)
        if not data["code"]:
            data = data["data"]

            if not data["short_id"]:
                Log.warning