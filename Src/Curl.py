import requests
from Log import Log
from Base import sign
from config import config

class Curl(object):
    # 自定义get方法,自带sign签名   
    def get(self,url,param):
        Log.debug("GET: "+url)
        payload = {
            "cookie":config["Token"]["COOKIE"]
            }
        payload = dict(param,**payload)
        payload = sign(payload)
        r = requests.get(url,payload)
        return r.text
    
    # 自定义post方法,自带sign签名
    def post(self,url,param):
        Log.debug("POST: "+url)
        payload = {
            "cookie":config["Token"]["COOKIE"]
        }
        payload = dict(param,**payload)
        payload = sign(payload)
        r = requests.post(url,payload)
        return r.text
    
    # 自定义不带sign签名的post方法,取名为nspost(no sign post)
    def nspost(self,url,param):
        Log.debug("POST: "+url)
        headers = {
            "Accept":"application/json, text/plain, */*",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "accept-encoding":"gzip, deflate",
            "cookie":config["Token"]["COOKIE"]
        }
        r = requests.post(url,param,headers=headers)
        return r.text