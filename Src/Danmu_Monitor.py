import aiohttp
from Danmu import DanmuRaffleHandler

class DanmuMonitor:
    def __init__(self):
        self._session = None
    
    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def run_Danmu_Raffle_Handler(self,area_id):
        # (房间号,分区号,session)
        await DanmuRaffleHandler(0,area_id,self.session).run_forever()

danmu_monitor = DanmuMonitor()

async def run_Danmu_Raffle_Handler(area_id):
    await danmu_monitor.run_Danmu_Raffle_Handler(area_id)