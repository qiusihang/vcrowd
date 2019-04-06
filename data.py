
class DataUnit:

    def __init__(self, uid, data_row):
        self.uid = uid
        self.data_row = data_row
        self.judgements = []
        self.properties = {}

    def assign_property(self, name, value):
        self.properties[name] = value


class Judgement:

    def __init__(self, worker, task, data_unit):
        self.worker = worker
        self.task = task
        self.data_unit = data_unit
        self.properties = {} # configurable

    def assign_property(self, name, value):
        self.properties[name] = value


class Data:

    def __init__(self):
        self.data_units = []
        self.count = 0
        self.n_judgements = 3 # configurable

    def add_data(self, data_row):
        self.count += 1
        self.data_units.append( DataUnit(self.count, data_row) )

    def random_selection(self, n):
        l = []
        d = []
        for i in range(len(self.data_units)):
            du = self.data_units[i]
            if len(du.judgements) < du.n_judgements:
                l.append(i)
        for i in range(n):
            r = random.randint(0,len(l)-1)
            d.append(self.data_units[l.pop(r)])
        return d
