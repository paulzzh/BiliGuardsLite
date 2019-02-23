import asyncio
from AsyncioCurl import AsyncioCurl
from Live import Live


task = [
    Live.get_room_by_area(1),
    Live.get_room_by_area(2),
    Live.get_room_by_area(3),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(task))