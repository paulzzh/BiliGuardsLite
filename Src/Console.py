import sys
from Statistics import Statistics
from Live import Live
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
import asyncio
from cmd import Cmd
from config import config

def fetch_real_roomid(roomid):
    if roomid:
        real_roomid = [[roomid], Live.check_room]
    else:
        real_roomid = config["Live"]["ROOM_ID"]
    return real_roomid
  
              
class Console(Cmd):
    prompt = ''

    def __init__(self, loop):
        self.loop = loop
        Cmd.__init__(self)
        
    def guide_of_console(self):
        print('___________________________')
        print('| 欢迎使用本控制台           |')
        print('|1 输出本次抽奖统计          |')
        print('|2 查看目前拥有礼物的统计     |')
        print('|3 查看持有勋章状态          |')
        print('|4 获取直播个人的基本信息     |')
        print('|5 检查今日任务的完成情况     |')
        print('|6 模拟电脑网页端发送弹幕     |')
        print('|7 直播间的长短号码的转化     |')
        print('|8 手动送礼物到指定直播间     |')
        print('|9 房间号码查看主播         |')
        print('|10 当前拥有的扭蛋币         |')
        print('|11 开扭蛋币(只能1，10，100) |')
        print('￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣')
        
    def default(self, line):
        self.guide_of_console()
        
    def emptyline(self):
        self.guide_of_console()
        
    def do_1(self, line):
        Statistics.print_statistics()
        
    def do_2(self, line):
        self.append2list_console(Live.fetch_bag_list)
        
    def do_3(self, line):
        self.append2list_console(Live.fetch_medal)
        
    def do_4(self, line):
        self.append2list_console(Live.fetch_user_info)
        
    def do_5(self, line):
        self.append2list_console(Live.check_taskinfo)
        
    def do_6(self, line):
        msg = input('请输入要发送的信息:')
        roomid = input('请输入要发送的房间号:')
        real_roomid = fetch_real_roomid(roomid)
        self.append2list_console([[msg, real_roomid], Live.send_danmu])
        
    def do_7(self, line):
        roomid = input('请输入要转化的房间号:')
        if not roomid:
            roomid = config["Live"]["ROOM_ID"]
        self.append2list_console([[roomid], Live.check_room])
    
    def do_8(self, line):
        self.append2list_console([[True], Live.fetch_bag_list])
        bagid = input('请输入要发送的礼物编号:')
        giftnum = int(input('请输入要发送的礼物数目:'))
        roomid = input('请输入要发送的房间号:')
        real_roomid = fetch_real_roomid(roomid)
        self.append2list_console([[real_roomid, giftnum, bagid], Live.send_gift])
            
    def do_9(self, line):
        roomid = input('请输入roomid')
        real_roomid = fetch_real_roomid(roomid)
        self.append2list_console([[real_roomid], Live.fetch_liveuser_info])
    
    def do_10(self, line):
        self.append2list_console(Live.fetch_capsule_info)
        
    def do_11(self, line):
        count = input('请输入要开的扭蛋数目(1或10或100)')
        self.append2list_console([[count], Live.open_capsule])
        
    def append2list_console(self, request):
        asyncio.run_coroutine_threadsafe(self.excute_async(request), self.loop)
        # inst.loop.call_soon_threadsafe(inst.queue_console.put_nowait, request)
        
    async def excute_async(self, i):
        if isinstance(i, list):
            for j in range(len(i[0])):
                if isinstance(i[0][j], list):
                    i[0][j] = await i[0][j][1](*(i[0][j][0]))
            if i[1] == 'normal':
                i[2](*i[0])
            else:
                await i[1](*i[0])
        else:
            await i()
    
    
    
