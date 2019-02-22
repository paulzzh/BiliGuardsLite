import asyncio
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest

task = [
    BasicRequest.req_get_room_by_area(1)
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))