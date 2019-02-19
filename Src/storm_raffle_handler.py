class StormRaffleHandler:
    @staticmethod
    def target(step):
        if step == 0:
            return StormRaffleHandler.check
        if step == 1:
            return StormRaffleHandler.join
