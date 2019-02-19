import asyncio
import aiohttp
from Log import Log
from Base import sign
from config import config

class AsycnioCurl:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get(self,url,param):
        Log.debug("GET: "+url)
        payload = {
            "cookie":config["Token"]["COOKIE"]
        }
        payload = dict(param,**payload)
        payload = sign(payload)
        async with self.session.get(url,params=payload) as r:
            return await r.text()
    
    async def post(self,url,param):
        Log.debug("POST: "+url)
        payload = {
            "cookie":config["Token"]["COOKIE"]
        }
        payload = dict(param,**payload)
        payload = sign(payload)
        async with self.session.post(url,data=payload) as r:
            return await r.text()

    async def nspost(self,url,param):
        Log.debug("POST: "+url)
        headers = {
            "Accept":"application/json, text/plain, */*",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "accept-encoding":"gzip, deflate",
            "cookie":config["Token"]["COOKIE"]
        }
        async with self.session.post(url,data=param,headers=headers) as r:
            return await r.text()