import time
import json
import struct # struct模块来解决str和其他二进制数据类型的转换
import asyncio
import aiohttp
import Statistics
import raffle_handler
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Live import Live
from Tv_Raffle_Handler import TvRaffleHandler
from Guard_Raffle_Handler import GuardRaffleHandler
from Storm_Raffle_Handler import StormRaffleHandler

class BaseDanmu():
    structer = struct.Struct("!I2H2I")

    def __init__(self,room_id,area_id,client_session=None):
        if client_session is None:
            self.client = aiohttp.ClientSession()
        else:
            self.client = client_session
        self.ws = None
        self._area_id = area_id
        self.room_id = room_id
        # 建立连接过程中难以处理重设置房间问题
        self.lock_for_reseting_roomid_manually = asyncio.Lock()
        self.task_main = None
        self.bytes_heartbeat = self.wrap_str(opt=2,body="")
    
    # 装饰器
    @property
    def room_id(self):
        return self._room_id
    
    @room_id.setter
    def room_id(self,room_id):
        self._room_id = room_id
        str_conn_room = f'{{"uid":0,"roomid":{room_id},"protover":1,"platform":"web","clientver":"1.3.3"}}'
        self.bytes_conn_room = self.wrap_str(opt=7, body=str_conn_room)
    
    def wrap_str(self,opt,body,len_header=16,ver=1,seq=1):
        remain_data = body.encode("utf-8")
        len_data = len(remain_data) + len_header
        header = self.structer.pack(len_data,len_header,ver,opt,seq)
        data = header + remain_data
        return data

    async def send_bytes(self,bytes_data):
        # 尝试发送bytes
        try:
            await self.ws.send_bytes(bytes_data)
        # 如果取消
        except asyncio.CancelledError:
            return False
        # 如果发送失败
        except:
            Log.error("发送bytes失败")
            return False
        return True
    
    async def read_bytes(self):
        bytes_data = None
        # 尝试接受bytes
        try:
            msg = await asyncio.wait_for(self.ws.receive(),timeout=35.0)
            bytes_data = msg.data
        # 如果超时
        except asyncio.TimeoutError:
            Log.error("35秒没有收到心跳包,与服务器的连接已断开")
            return None
        # 如果接受错误
        except:
            Log.error("未知错误")
            return None

        return bytes_data
        
    async def open(self):
        try:
            url = "wss://broadcastlv.chat.bilibili.com:443/sub"
            self.ws = await asyncio.wait_for(self.client.ws_connect(url),timeout=3)
        except:
            Log.error("无法连接到B站弹幕姬服务器,请检查您的网络连接")
            return False
        Log.info("%s 号弹幕监控已连接到B站弹幕姬服务器"%self._area_id)
        return (await self.send_bytes(self.bytes_conn_room))
    
    async def heart_beat(self):
        try:
            while True:
                if not (await self.send_bytes(self.bytes_heartbeat)):
                    return
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass
    
    async def read_datas(self):
        while True:
            datas = await self.read_bytes()
			# 本函数对bytes进行相关操作，不特别声明，均为bytes
            if datas is None:
                return
            data_l = 0
            len_datas = len(datas)
            while data_l != len_datas:
                # 每片data都分为header和body，data和data可能粘连
                # data_l == header_l && next_data_l = next_header_l
                # ||header_l...header_r|body_l...body_r||next_data_l...
                tuple_header = self.structer.unpack_from(datas[data_l:])
                len_data,len_header,ver,opt,seq = tuple_header
                body_l = data_l + len_header
                next_data_l = data_l + len_data
                body = datas[body_l:next_data_l]
                # 人气值之类的,在这里不使用
                if opt == 3:
                    # 满屏都是这个破玩意,注释掉了
                    # Log.info("弹幕心跳检测 %s"%self._area_id)
                    pass
                # cmd
                elif opt == 5:
                    if not self.handle_danmu(body):
                        return
                # 握手确认
                elif opt == 8:
                    Log.info("%s 号弹幕监控进入房间 %s"%(self._area_id,self._room_id))
                else:
                    Log.warning(datas[data_l:next_data_l])

                data_l = next_data_l

    async def close(self):
        # 尝试关闭连接
        try:
            await self.ws.close()
        # 如果关闭失败
        except:
            Log.error("关闭与B站弹幕姬服务器时出现错误")
        if not self.ws.closed:
            Log.error("%s 号弹幕收尾模块状态 %s"%(self._area_id,self.ws.closed))

    def handle_danmu(self,body):
        return True

    async def run_forever(self):
        time_now = 0
        while True:
            if int(time.time()) -time_now <= 3:
                Log.warning("网络波动,%s 号弹幕姬延迟3s后重启"%self._area_id)
                await asyncio.sleep(3)
            Log.info("正在启动 %s 号弹幕姬"%self._area_id)
            time_now = int(time.time())
            async with self.lock_for_reseting_roomid_manually:
                is_open = await self.open()
            if not is_open:
                continue
            self.task_main = asyncio.ensure_future(self.read_datas())
            task_heartbeat = asyncio.ensure_future(self.heart_beat())
            tasks = [self.task_main, task_heartbeat]
            _,pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            Log.warning("%s 号弹幕姬异常或主动断开，正在处理剩余信息"%self._area_id)
            if not task_heartbeat.done():
                task_heartbeat.cancel()
            await self.close()
            await asyncio.wait(pending)
            Log.info("%s 号弹幕姬退出，剩余任务处理完毕"%self._area_id)

    async def reconnect(self,room_id):
        async with self.lock_for_reseting_roomid_manually:
            if self.ws is not None:
                await self.close()
            if self.task_main is not None:
                await self.task_main
            # 由于锁的存在，绝对不可能到达下一个的自动重连状态，这里是保证正确显示当前监控房间号
            self.room_id = room_id
            Log.info("%s 号弹幕姬已经切换房间 %s"%(self._area_id,room_id))

class DanmuRaffleHandler(BaseDanmu):
    async def check_area(self):
        try:
            while True:
                await asyncio.sleep(300)
                is_ok = await asyncio.shield(Live.is_ok_as_monitor(self._room_id,self._area_id))
                if not is_ok:
                    Log.warning("%s 不再适合作为监控房间，即将切换")
                    return
        except asyncio.CancelledError:
            pass
        

    def handle_danmu(self, body):
        data = json.loads(body.decode("utf-8"))
        cmd = data["cmd"]

        if cmd == "PREPARING":
            Log.info("%s 号弹幕监控下播 %s"%(self._area_id,self._room_id))
            return False
        
        elif cmd == "NOTICE_MSG":
			# 1 《第五人格》哔哩哔哩直播预选赛六强诞生！
            # 2 全区广播：<%user_name%>送给<%user_name%>1个嗨翻全城，快来抽奖吧
            # 3 <%user_name%> 在 <%user_name%> 的房间开通了总督并触发了抽奖，点击前往TA的房间去抽奖吧
            # 4 欢迎 <%总督 user_name%> 登船
            # 5 恭喜 <%user_name%> 获得大奖 <%23333x银瓜子%>, 感谢 <%user_name%> 的赠送
            # 6 <%user_name%> 在直播间 <%529%> 使用了 <%20%> 倍节奏风暴，大家快去跟风领取奖励吧！(只报20的)
            msg_type = data["msg_type"]
            msg_common = data["msg_common"]
            real_roomid = data["real_roomid"]
            msg_common = data["msg_common"].replace(" ","")
            msg_common = msg_common.replace("“","")
            msg_common = msg_common.replace("”","")
            # 小电视,DokiDoki,摩天大楼之类的抽奖活动
            if msg_type == 2 or msg_type == 8:
                str_gift = msg_common.split('%>')[-1].split('，')[0]
                if "个" in str_gift:
                    raffle_num,raffle_name = str_gift.split("个")
                elif "了" in str_gift:
                    raffle_num = 1
                    raffle_name = str_gift.split("了")[-1]
                else:
                    raffle_num = 1
                    raffle_name = str_gift
                broadcast = msg_common.split("广播")[0]
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self._area_id,real_roomid,raffle_name))
                raffle_handler.RaffleHandler.push2queue((real_roomid,),TvRaffleHandler.check)
                # 如果不是全区就设置为1(分区)
                broadcast_type = 0 if broadcast == '全区' else 1
                #Statistics.add2pushed_raffles(raffle_name,broadcast_type,raffle_num)
            # 大航海
            elif msg_type == 3:
                raffle_name = msg_common.split("开通了")[-1][:2]
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self._area_id,real_roomid,raffle_name))
                raffle_handler.RaffleHandler.push2queue((real_roomid,),GuardRaffleHandler.check)
                # 如果不是总督就设置为2(本房间)
                broadcast_type = 0 if raffle_name == "总督" else 2
                #Statistics.add2pushed_raffles(raffle_name,broadcast_type)
            # 节奏风暴
            elif msg_type == 6:
                raffle_name = "二十倍节奏风暴"
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self._area_id,real_roomid,raffle_name))
                raffle_handler.RaffleHandler.push2queue(StormRaffleHandler.check, real_roomid)
                #Statistics.add2pushed_raffles((real_roomid,),StormRaffleHandler.check)
        
        # 论缩进的重要性,缩进太多永远都是: 
        # 网络波动, X 号弹幕姬延迟3s后重启
        # X 号弹幕姬异常或主动断开，正在处理剩余信息
        # X 号弹幕姬退出，剩余任务处理完毕
        # Debug 这个问题Debug了两天
        return True

    async def run_forever(self):
        time_now = 0
        while True:
            if int(time.time()) - time_now <= 3:
                Log.warning("网络波动, %s 号弹幕姬延迟3s后重启"%self._area_id)
                await asyncio.sleep(3)
            Log.info("正在启动 %s 号弹幕姬"%self._area_id)
            time_now = int(time.time())
            async with self.lock_for_reseting_roomid_manually:
                self.room_id = await Live.get_room_by_area(self._area_id,self._room_id)
                is_open = await self.open()
            if not is_open:
                continue
            self.task_main = asyncio.ensure_future(self.read_datas())
            task_heartbeat = asyncio.ensure_future(self.heart_beat())
            task_checkarea = asyncio.ensure_future(self.check_area())
            tasks = [self.task_main,task_heartbeat,task_checkarea]
            _, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            Log.warning("%s 号弹幕姬异常或主动断开，正在处理剩余信息"%self._area_id)
            if not task_heartbeat.done():
                task_heartbeat.cancel()
            if not task_checkarea.done():
                task_checkarea.cancel()
            await self.close()
            await asyncio.wait(pending)
            Log.info("%s 号弹幕姬退出，剩余任务处理完毕"%self._area_id)
