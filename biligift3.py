import urllib.request,urllib.parse,json,hashlib,time,platform,random
import sys
sys.path.append("Src")
from Auth import Auth
from config import config

from bs4 import BeautifulSoup
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log

#签到
def sign():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36','Cookie':cookie}
        url = 'http://api.live.bilibili.com/sign/doSign'
        request = urllib.request.Request(url=url, headers=headers, method='GET')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        Log.info(str(html))
    except:
        Log.info("签到网络失败")

#获取上船领奖id
def getcapid(roomid):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'}
        url = "https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/Check?roomid="+str(roomid)
        request = urllib.request.Request(url=url,headers=headers,method='GET')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        Log.info(str(html))
        obj=json.loads(html)
        return obj["data"]["guard"]
    except:
        return []

#检测钓鱼房间
def checkroom(id):
    try:
        url = 'http://api.live.bilibili.com/room/v1/Room/room_init?id=' + str(id)
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36','Accept-Encoding':''}
        request = urllib.request.Request(url=url, headers=headers, method='GET')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        obj=json.loads(html)['data']
        if not (obj['encrypted'] or obj['is_locked'] or obj['is_hidden']):
            return True
        else:
            Log.info("钓鱼房间 "+str(id)+" "+str(obj))
            return False
    except:
        return False

#伪造观看历史（已失效）
def post_watching_history(room_id):
    try:
        values = {"room_id":room_id,"csrf_token":csrf}
        data=urllib.parse.urlencode(values).encode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36','Cookie':cookie}
        url = "http://api.live.bilibili.com/room/v1/Room/room_entry_action"
        request = urllib.request.Request(url=url, data=data, headers=headers,method='POST')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        obj=json.loads(html)
        Log.info(str(obj))
    except:
        Log.info("历史记录失败 "+str(room_id))

#上船领奖
def get_gift_of_captain(room_id,capid):
    try:
        values = {"roomid":room_id,"id":capid,"type":"guard","csrf_token": csrf}
        data=urllib.parse.urlencode(values).encode('utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36','Cookie':cookie}
        #url = "http://api.live.bilibili.com/lottery/v2/lottery/join"
        url = "http://api.live.bilibili.com/xlive/lottery-interface/v3/guard/join"
        request = urllib.request.Request(url=url, data=data, headers=headers,method='POST')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        obj=json.loads(html)
        Log.info(str(obj))
        return obj
    except:
        Log.info("领取失败网络错误 "+str(room_id))
        return {"code":400}

#按类型获取上船房间 接口来自 https://live.bilibili.com/164725
def getvaluecaplist(level):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9; DUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36'}
        url = 'https://bilipage.expublicsite.com:23333/Guards/SimpleView'
        request = urllib.request.Request(url=url, headers=headers, method='GET')
        html = urllib.request.urlopen(request).read().decode('utf-8')
        Log.info(str(html))
        soup=BeautifulSoup(html).body
        tb=soup.find_all("table")
        
        vlist=[[],[],[]]
        
        for tbl in tb:
            which=2
            if "总督" in tbl.findPrevious().text:
                which=0
            if "提督" in tbl.findPrevious().text:
                which=1
            if "舰长" in tbl.findPrevious().text:
                which=2
            
            tlist=[]
            for a in tbl.find_all("a"):
                if a["href"][0]=="b":
                    tlist.append(int(a["href"][16:]))
            vlist[which]=tlist
        Log.info(str(vlist))
        
        alist=[]
        if level>=1:
            alist+=vlist[0]
        if level>=2:
            alist+=vlist[1]
        if level>=3:
            otall=len(vlist[0])+len(vlist[1])
            if len(vlist[2])>otall:
                alist+=vlist[2][:otall]
            else:
                alist+=vlist[2]
        
        #olist=getcaplist()
        nlist=[]
#        for cap in getcaplist():
#            if cap['OriginRoomId'] in alist:
#                nlist.append(cap)
        for rmid in alist:
            for gd in getcapid(rmid):
                nlist.append((rmid,gd["id"]))
        
        #Log.info(str(nlist))
        return nlist
    except Exception as e:
        print(e)

def worker(level):
    cpslist=getvaluecaplist(level)
    Log.info(str(cpslist))
    #打乱顺序
    random.shuffle(cpslist)
    for roomid,capid in cpslist:
#        roomid=cap['OriginRoomId']
#        capid=cap['GuardId']
        capdone2[str(capid)]=True
        if not capdone.get(str(capid),False):
            #capdone2[str(capid)]=True
            #检测钓鱼房间且capid不为0
            if checkroom(roomid) and capid:
                #伪造观看历史,现已失效
                #post_watching_history(roomid)
                #time.sleep(0.5+random.random())
                obj=get_gift_of_captain(roomid,capid)
                if obj['code']==0:
                    Log.info(str(roomid)+" 获取亲密度 "+str(obj['data']['award_text']))
                elif obj['code']==-403:
                    #发现被封禁立刻终止
                    Log.info("疑似被封禁"+str(obj))
                    break
                else:
                    Log.info("领取失败"+str(obj))
                #随机延迟5-10秒
                time.sleep(5+int(random.random()*10))

Log.info("\n======START======"+str(time.asctime())+"============\n")

a=Auth()
a.work()
csrf = config['Token']['CSRF']
Log.info(str(csrf))
cookie = config['Token']['COOKIE']
Log.info(str(cookie))

capdone = json.load(open("done.json"))
capdone2={}    

#capdone={}

nhour=time.localtime().tm_hour

nlevel=0

#每日签到
if nhour in [0]:
    sign()

#上午十点开始领取 总督提督
if nhour in [10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,4]:
    nlevel=2

#下午一点开始领取 总督提督舰长
if nhour in [13,14,18,19,20,21,22]:
    nlevel=3

time.sleep(10)

worker(nlevel)

Log.info(str(capdone))
with open("done.json","w") as f:
    f.write(json.dumps(capdone2))


Log.info("\n======FINISH======"+str(time.asctime())+"============\n")
