import rsa
import time
import datetime
import hashlib
import urllib.parse
from config import config

def sign(payload):

    # ios 6680
    appkey = "27eb53fc9058f8c3"
    appsecret = "c2ed53a74eeefe3cf99fbd01d8c9c375"

    # Android
    # appkey = "1d8b6e7d45233436"
    # appsecret = "560c52ccd288fed045859ed18bffd973"

    # 云视听 TV
    # appkey = "4409e2ce8ffd12b8"
    # appsecret = "59b43e04ad6965f34319062b478f83dd"

    default = {
        "access_key":config["Token"]["ACCESS_TOKEN"],
        "actionKey":"appkey",
        "appkey":appkey,
        "build":"8290",
        "device":"phone",
        "mobi_app":"iphone",
        "platform":"ios",
        "ts":int(time.time()),
        "type":"json"
    }

    payload = dict(payload,**default)
    payload = ksort(payload)
    data = urllib.parse.urlencode(payload)
    md5 = hashlib.md5()
    md5.update(data.encode() + appsecret.encode())
    sign = {"sign":md5.hexdigest()}
    payload = dict(payload,**sign)
    return payload

def ksort(d):
     return [(k,d[k]) for k in sorted(d.keys())]

def openssl_public_encrypt(plaintext,key):
     key = rsa.PublicKey.load_pkcs1_openssl_pem(key)
     ciphertext = rsa.encrypt(plaintext.encode(),key)
     return ciphertext

def arrange_cookie(array):
     cookie_array = array["data"]["cookie_info"]["cookies"]
     cookie = ""
     for i in range(0, len(cookie_array)):
          cookie = cookie + cookie_array[i]["name"] + "=" + cookie_array[i]["value"] + ";"
     return cookie_array[0]["value"],cookie

def std235959():
     now = datetime.datetime.now()
     zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
     lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
     return int(time.mktime(lastToday.timetuple()))