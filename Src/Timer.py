import asyncio
import time

class Timer:
    __slots__ = ("loop",)
    instance = None

    def __new__(cls,loop=None):
        if not cls.instance:
            cls.instance = super(Timer,cls).__new__(cls)
            cls.instance.loop = loop
        return cls.instance

    def excute_async(self,i):
        asyncio.ensure_future(i[0](*i[1]))

    @staticmethod
    def call_after(func,delay):
        inst = Timer.instance
        value = (func,())
        inst.loop.call_after(delay,inst.excute_async,value)
    
    @staticmethod
    def add2list_jobs(func,time_expected,tuple_values):
        inst = Timer.instance
        current_time = int(time.time())
        value = (func,tuple_values)
        inst.loop.call_later(time_expected-current_time,inst.excute_async,value)