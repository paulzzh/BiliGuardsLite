import time
import json
import struct # struct模块来解决str和其他二进制数据类型的转换
import asyncio
import aiohttp
from Log import Log
from Live import Live

class BaseDanmu():
    structer = struct.Struct("!I2H2I")

    def __init__(self,room_id,area_id,client_session=None):
        if client_session is None:
            self.client = aiohttp.ClientSession()
        else:
            self.client = client_session
        self.ws = None
        self.area_id = 0
        self.room_id = 0
        # 建立连接过程中难以处理重设置房间问题
        self.lock_for_reseting_roomid_manually = asyncio.Lock()
        self.task_main = None
        self.bytes_heartbeat = self.wrap_str(opt=2,body="")
    
    # 装饰器
    @property
    def room_id(self):
        return self.room_id
    
    @room_id.setter
    def room_id(self,room_id):
        self.room_id = room_id
    
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
    
    async def read_bytes(self):
        bytes_data = None
        # 尝试接受bytes
        try:
            msg = await asyncio.wait_for(self.ws.receive(),timeout=35)
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
            self.ws = await asyncio.wait_for(self.client.ws_connect(url),timeout=5)
        except:
            Log.error("无法连接到B站弹幕姬服务器,请检查您的网络连接")
            return False
        Log.info("%s 号弹幕监控已连接到B站弹幕姬服务器"%self.area_id)
    
    async def heart_beat(self):
        try:
            while True:
                if not await(self.send_bytes(self.bytes_heartbeat)):
                    return
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass
    
    async def read_datas(self):
        while True:
            datas = await self.read_bytes()
            if datas is None:
                return
            data_l = 0
            len_datas = len(datas)
            while data_l != len_datas:
                tuple_header = self.structer.unpack_from(datas[data_l:])
                len_data,len_header,ver,opt,seq = tuple_header
                body_l = data_l + len_data
                next_data_l = data_l + len_data
                body = datas[body_l:next_data_l]
                # 人气值之类的,在这里不使用
                if opt == 3:
                    pass
                # cmd
                elif opt == 5:
                    if not self.handle_danmu(body):
                        return
                # 握手确认
                elif opt == 8:
                    Log.info("%s 号弹幕监控进入房间 %s"%(self.area_id,self.room_id))
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
            Log.error("%s 号弹幕收尾模块状态 %s"%(self.area_id,self.ws.closed))

    def handle_danmu(self,body):
        return True

    async def runforever(self):
        time_now = 0
        while True:
            if int(time.time()) -time_now <= 3:
                Log.warning("网络波动,%s 号弹幕姬延迟3s后重启")
                await asyncio.sleep(3)
                Log.info("正在启动 %s 号弹幕姬")
                time_now = int(time.time())
                async with self.lock_for_reseting_roomid_manually:
                    is_open = await self.open()
                if not is_open:
                    continue
                self.task_main = asyncio.ensure_future(self.read_datas())
                task_heartbeat = asyncio.ensure_future(self.heart_beat())
                tasks = [self.task_main, task_heartbeat]
                _,pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                Log.warning("%s 号弹幕姬异常或主动断开，正在处理剩余信息")
                if not task_heartbeat.done():
                task_heartbeat.cancel()
                await self.close()
                await asyncio.wait(pending)
                Log.info("%s 号弹幕姬退出，剩余任务处理完毕")

    async def reconnect(self,room_id):
        async with self.lock_for_reseting_roomid_manually:
            if self.ws is not None:
                await self.close()

class DanmuRaffleHandler(BaseDanmu):
    async def check_area(self):
        try:
            while True:
                await asyncio.sleep(300)
                is_ok = await asyncio.shield(Live.is_ok_as_monitor(self.room_id,self.area_id))
                if not is_ok:
                    Log.warning("%s 不再适合作为监控房间，即将切换")
                    return
        except asyncio.CancelledError:
            pass
        

    def handle_danmu(self, body):
        data = json.loads(body.decode("utf-8"))
        cmd = data["cmd"]

        if cmd == "PREPARING":
            Log.info("%s 号弹幕监控下播 %s"%(self.area_id,self.room_id))
            return False
        
        if cmd == "NOTICE_MSG":
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
                    raffle_name = str_gift.split('了')[-1]
                else:
                    raffle_num = 1
                    raffle_name = str_gift
                broadcast = msg_common.split("广播")[0]
                raffle_handler
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self.area_id,self.room_id,raffle_name))
            # 大航海
            if msg_type == 3:
                # 开通的名称
                raffle_name = msg_common.split("开通了")[-1][:2]
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self.area_id,self.room_id,raffle_name))
            # 节奏风暴
            if msg_type == 6:
                raffle_name = "二十倍节奏风暴"
                Log.critical("%s 号弹幕监控检测到 %s 的 %s"%(self.area_id,self.room_id,raffle_name))
            return True

    async def run_forever(self):
        time_now = 0
        while True:
            if int(time.time()) - time_now <= 3:
                Log.warning("网络波动, %s号弹幕姬延迟3s后重启")
                await asyncio.sleep(3)
            Log.info("正在启动 %s 号弹幕姬")
            time_now = int(time.time())
            if not is_open:
                continue
            self.task_main = asyncio.ensure_future(self.read_datas())
            task_heartbeat = asyncio.ensure_future(self.heart_beat())
            task_checkarea = asyncio.ensure_future(self.check_area())
            Log.warning("%s 号弹幕姬异常或主动断开，正在处理剩余信息")
             if not task_heartbeat.done():
                task_heartbeat.cancel()
            if not task_checkarea.done():
                task_checkarea.cancel()
            await self.close()
            await asyncio.wait(pending)
            Log.into("%s 号弹幕姬退出，剩余任务处理完毕")
