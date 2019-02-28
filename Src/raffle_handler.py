import asyncio

class RaffleHandler:
    instance = None
    
    # 单例模式
    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(RaffleHandler, cls).__new__(cls, *args, **kw)
            cls.instance.queue = asyncio.Queue()
            cls.instance.list_raffle_id = []
        return cls.instance

    async def run(self):
        while True:
            raffle0 = await self.queue.get()
            await asyncio.sleep(2)
            list_raffle = [self.queue.get_nowait() for i in range(self.queue.qsize())]
            list_raffle.append(raffle0)
            list_raffle = list(set(list_raffle))

            tasklist = []
            for i in list_raffle:
                i = list(i)
                i[0] = list(i[0])
                for j in range(len(i[0])):
                    if isinstance(i[0][j],tuple):
                        i[0][j] = await i[0][j][1](*(i[0][j][0]))
                
                task = asyncio.ensure_future(i[1](*i[0]))
                tasklist.append(task)
    
    @staticmethod
    def push2queue(value,func):
        RaffleHandler.instance.queue.put_nowait((value,func))
