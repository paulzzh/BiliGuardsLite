class Statistics:
    instance = None

    def __new__(cls, area_num=0):
        if not cls.instance:
            cls.instance = super(Statistics, cls).__new__(cls)
            cls.instance.area_num = area_num
            cls.instance.activity_id_list = []
            # cls.instance.activity_time_list = []
            cls.instance.TV_id_list = []
            # cls.instance.TV_time_list = []
            cls.instance.pushed_raffle = {}
            
            cls.instance.joined_raffle = {}
            cls.instance.result = {}
            # cls.instance.TVsleeptime = 185
            # cls.instance.activitysleeptime = 125

            cls.list_raffle_id = []
        return cls.instance

    @staticmethod
    def print_statistics():
        inst = Statistics.instance
        print("本次推送抽奖统计")
        for k,v in inst.pushed_raffles.items():
            if isinstance(v,int):
                print(f'{v:^5} X {k}')
            else:
                print(f'{v:^5.2f} X {k}')

        print()
        print('本次参与抽奖统计：')
        joined_of_id = inst.joined_raffles.get()
        for k, v in joined_of_id.items():
            print(f'{v:^5} X {k}')

        print()
        print('本次抽奖结果统计：')
        results_of_id = inst.raffle_results.get()
        for k, v in results_of_id.items():
            print(f'{v:^5} X {k}')
    
    def add2pushed_raffles(self,raffle_name,broadcast_type,num):
        inst = Statistics.instance
        # broadcast_type 广播类型 0 全区广播 1 分区广播 2 本房间
        if broadcast_type == 0:
            inst.pushed_raffle[raffle_name] = inst.pushed_raffle.get(raffle_name, 0) + int(num) / inst.area_num
        else:
            inst.pushed_raffle[raffle_name] = inst.pushed_raffle.get(raffle_name, 0) + int(num)

    def add2joined_raffles(self,raffle_name,num):
        inst = Statistics.instance
        inst.joined_raffle[type] = inst.joined_raffle.get(type, 0) + int(num)

    def add2results(self,gift_name,num=1):
        results_of_id  = self.raffle_results[0]
        results_of_id[gift_name] = results_of_id.get(gift_name,0) + num

    def add2raffle_ids(self,raffle_id):
        inst = Statistics.instance
        inst.list_raffle_id.append(raffle_id)

        if len(inst.ist_raffle_id) > 150:
            del inst.list_raffle_id[:75]
        
    def is_raffleid_duplicate(self,raffle_id):
        inst = Statistics.instance
        return (raffle_id in inst.list_raffle_id)

var = Statistics()

def add2pushed_raffles(raffle_name,broadcast_type=0,num=1):
    var.add2pushed_raffles(raffle_name,broadcast_type,int(num))

def add2joined_raffles(raffle_name,num=1):
    var.add2joined_raffles(raffle_name,int(num))

def add2results(gift_name,num=1):
    var.add2results(gift_name,int(num))

def add2raffle_ids(raffle_id):
    var.add2raffle_ids(int(raffle_id))

def is_raffleid_duplicate(raffle_id):
    return var.is_raffleid_duplicate(int(raffle_id))