import random
import functions
from data import *

class Worker:

    def __init__(self, wid, classification):
        self.wid = wid
        self.classification = classification
        self.task = None
        self.properties = {} # configurable
        self.executefunc = "default"

    def assign_property(self, name, value):
        self.properties[name] = value

    def execute(self): # this function returns the actual execution time
        # try custom execution fucntion
        if self.executefunc == "customized":
            return functions.execute(self, self.task)
        # if custom execution fucntion doesn't exist, return default value
        return 300 # execution_time

    def submit(self):
        if self.task is None:
            return
        for du in self.task.data_units:
            j = Judgement(self, self.task, du)
            du.judgements.append(j)

class WorkerManager:

    def __init__(self):
        self.count = 0
        self.workers = []
        self.waiting_queue = []
        self.execute = "default"
        self.worker_arrival_interval = 38 # configurable
        self.worker_classification = 3 # configurable
        self.worker_classification_name = ["low", "medium", "high"] # configurable
        self.worker_distribution = [0.333, 0.333, 0.333] # configurable
        self.dropout_time = 1800 # configurable
        self.properties = {} # configurable

    def assign_property(self, name, value):
        self.properties[name] = value

    def remove_worker(self, worker):
        try:
            self.waiting_queue.remove(worker)
        except ValueError:
            "Do nothing"

    def add_worker(self):
        p = random.random()
        probability = 0
        for i in range(len(self.worker_distribution)):
            probability += self.worker_distribution[i]
            if i == len(self.worker_distribution) - 1:
                probability = 1
            if p <= probability:
                self.count += 1
                worker = Worker(self.count, i)
                worker.executefunc = self.execute
                self.workers.append(worker)
                self.waiting_queue.append(worker)

    def return_upcoming_worker(self):
        if len(self.waiting_queue) > 0:
            return self.waiting_queue[0]
        return None
