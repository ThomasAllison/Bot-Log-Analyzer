import operator


class BotCounter:
    bots = {}

    def add(self, useragent):
        if self.bots.get(useragent):
            self.bots[useragent] += 1
        else:
            self.bots[useragent] = 1

    def get_bots(self):
        return self.bots

    def get_sorted_list_by_frequency(self):
        return list(reversed(sorted(self.bots.items(), key=operator.itemgetter(1))))
