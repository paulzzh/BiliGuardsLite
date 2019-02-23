import asyncio
from user import User
from random import uniform

class Controller:
    def set_values(self,loop):
        self.loop = loop
    
    async def notify_all(self,func,*args):
        result = await User.accept(func,*args)
        return result

    def __set_delay(self, delay_range):
        if delay_range is None:
            delay_range = 0, 0

        return (uniform(*delay_range))

    # 接受id >=0
    async def __exec_one_step(self, id, task, step, *args):
        # print('当前请求', task, id, step, args)
        func = task.target(step)
        assert func is not None
        results = await self.notify_all(func, *args)
        # results为()或None,就terminate,不管是否到头，这里的设计是user的拒绝执行的功能
        # 返回必须是tuple/list！
        # print('结果返回', results)
        if results is None:
            return
        for new_step, *result in results:
            # user的延迟执行功能实现
            if new_step == -1:
                new_step = step
            # print(f'本step结果:{result} 下一步:{new_step}')
            delay, new_uid, *args = result
            self.call_after(delay, new_uid, task, new_step, *args)
    
    # 接受uid -2/-1/>=0
    def call_after(self, delay_range, *args):
        for new_id, delay in self.__set_delay(delay_range):
            # print(f'休息{delay}s   {new_id}执行:{args}')
            # 这里用callafter api把notify送到queue里面立刻退出,所以不会爆
            self.loop.call_later(delay, self.__exec_bg, new_id, *args)
        
    def __exec_bg(self, *args):
        asyncio.ensure_future(self.__exec_one_step(*args))

var = Controller()

def set_values(loop):
    var.set_values(loop)

def exec_task(task,step,*args,delay_range=None):
    var.call_after(delay_range,task,step,*args)

async def exec_func(func,*args):
    result = await var.notify_all(func,*args)
    return result