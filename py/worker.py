import random
from data import *

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
        self.worker_property_names = [] # configurable
        self.worker_properties = [] # configurable
        self.functions =  __import__("functions")

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
                properties = {}
                for j in range(len(self.worker_property_names)):
                    name = self.worker_property_names[j]
                    properties[name] = self.worker_properties[j][i]
                worker = self.functions.Worker(self.count, i, properties)
                worker.executefunc = self.execute
                self.workers.append(worker)
                self.waiting_queue.append(worker)

    def return_upcoming_worker(self):
        if len(self.waiting_queue) > 0:
            return self.waiting_queue[0]
        return None
