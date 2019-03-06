class Statistics:
    instance = None

    def __new__(cls, area_num=0):
        if not cls.instance:
            cls.instance = super(Statistics, cls).__new__(cls)
            cls.instance.area_num = area_num

            cls.instance.pushed_raffles = {}
            cls.instance.joined_raffles = {}
            cls.instance.raffle_results = {}

            cls.list_raffle_id = []
        return cls.instance

    @staticmethod
    def print_statistics():
        inst = Statistics.instance
        print("本次推送抽奖统计:")
        for k,v in inst.pushed_raffles.items():
            print(f'{v:^5.2f} X {k}')

        print()
        print('本次参与抽奖统计：')
        for k, v in inst.joined_raffles.items():
            print(f'{v:^5} X {k}')

        print()
        print('本次抽奖结果统计：')
        for k, v in inst.raffle_results.items():
            print(f'{v:^5} X {k}')
    
    @staticmethod
    def add2pushed_raffles(raffle_name,broadcast_type=0,num=1):
        inst = Statistics.instance
        # broadcast_type 广播类型 0 全区广播 1 分区广播 2 本房间
        if broadcast_type == 0:
            inst.pushed_raffles[raffle_name] = inst.pushed_raffles.get(raffle_name, 0) + int(num) / inst.area_num
        else:
            inst.pushed_raffles[raffle_name] = inst.pushed_raffles.get(raffle_name, 0) + int(num)

    @staticmethod
    def add2joined_raffles(raffle_name,num=1):
        inst = Statistics.instance
        inst.joined_raffles[raffle_name] = inst.joined_raffles.get(raffle_name, 0) + int(num)

    @staticmethod
    def add2results(result,num=1):
        inst = Statistics.instance
        inst.raffle_results[result] = inst.raffle_results.get(result, 0) + int(num)

    @staticmethod
    def add2raffle_ids(raffle_id):
        inst = Statistics.instance
        inst.list_raffle_id.append(raffle_id)

        if len(inst.list_raffle_id) > 150:
            del inst.list_raffle_id[:75]

    @staticmethod
    def is_raffleid_duplicate(raffle_id):
        inst = Statistics.instance
        return (raffle_id in inst.list_raffle_id)