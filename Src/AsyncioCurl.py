import asyncio
import aiohttp
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Base import sign
from config import config

sem = asyncio.Semaphore(3)

class AsyncioCurl:

    def __init__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=4))

    async def __get_json_body(self, rsp):
        json_body = await rsp.json(content_type=None)
        # 之后考虑加入expected_code、循环code、登录code来约束这个判定
        code = json_body['code']
        if code == 1024:
            Log.error('b站炸了，暂停所有请求1.5s后重试，请耐心等待')
            await asyncio.sleep(1.5)
            return None
        elif code == 3 or code == -401 or code == 1003 or code == -101 or code == 401:
            Log.error('api提示没有登录')
            Log.error(json_body)
            return json_body
        
        return json_body

# method 类似于aiohttp里面的对应method，目前只支持GET、POST
    async def request_json(self,
                           method,
                           url,
                           headers=None,
                           data=None,
                           params=None,
                           is_none_allowed=False):
        async with sem:
            i = 0
            while True:
                i += 1
                if i >= 10:
                    Log.warning(url)
                try:
                    async with self.session.request(method, url, headers=headers, data=data, params=params) as rsp:
                        if rsp.status == 200:
                            json_body = await self.__get_json_body(
                                rsp)
                            if json_body is not None or is_none_allowed:
                                await self.session.close()
                                return json_body
                        elif rsp.status == 403:
                            Log.warning("%s 403频繁,休眠240s"%url)
                            await asyncio.sleep(240)
                        elif rsp.status == 404:
                            return None
                except:
                    continue