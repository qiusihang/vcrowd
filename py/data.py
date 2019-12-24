import random

class DataUnit:

    def __init__(self, uid, data_row):
        self.uid = uid
        self.data_row = data_row
        self.judgements = []
        self.properties = {}

    def assign_property(self, name, value):
        self.properties[name] = value

    def add_judgement(self, worker, task, data_unit):
        self.judgements.append(Judgement(worker, task, data_unit))


class Judgement:

    def __init__(self, worker, task, data_unit):
        self.worker = worker
        self.task = task
        self.data_unit = data_unit
        self.properties = {}

    def assign_property(self, name, value):
        self.properties[name] = value


class Data:

    def __init__(self):
        self.data_units = []
        self.count = 0
        self.price = 0.1
        self.n_judgements = 3 # configurable

    def add_data(self, data_row):
        self.count += 1
        self.data_units.append( DataUnit(self.count, data_row) )

    def random_selection(self, n):
        l = len(self.data_units)
        d = []
        for i in range(l):
            r = random.randint(0,l-1)
            d.append(self.data_units[r])
        return d
