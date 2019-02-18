from Log import Log
from Curl import Curl

class Live:

    async def is_normal_room(user,room_id):
        if not roomid:
            return True
        json_response = await 

    def init_room(user,roomid):
        payload = {}
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id="+"{%s}"%roomid
        response = Curl().get(url,payload)
        return response