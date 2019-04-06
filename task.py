import random
import functions

class Task:

    def __init__(self, tid, data_units):
        self.tid = tid
        self.data_units = data_units
        self.properties = {} # configurable

    def assign_property(self, name, value):
        self.properties[name] = value


class TaskManager:

    def __init__(self, data):
        self.data = data
        self.n_data_rows = 3 # configurable
        self.data_selection = "default" # configurable
        self.assign = "default" # configurable
        self.count = 0
        self.tasks = []
        self.waiting_queue = []

    def assign_property(self, name, value):
        self.properties[name] = value

    def remove_task(self, task):
        try:
            self.waiting_queue.remove(task)
        except ValueError:
            "Do nothing"

    def add_task(self):
        self.count += 1
        # try custom selection fucntion
        if self.data_selection == "customized":
            return functions.data_selection(self.data)
        # if custom execution fucntion doesn't exist, use default random function
        data_units = self.data.random_selection(self.n_data_rows)
        task = Task(self.count, data_units)
        if len(task.data_units > 0): # the task is not empty
            self.tasks.append(task)
            self.waiting_queue.append(task)

    def return_upcoming_task(self):
        if len(self.waiting_queue) <= 0:
            self.add_task()
        if len(self.waiting_queue) > 0:
            return self.waiting_queue[0]
        return None

    def assign_task(self, wm):
        # try custom assign fucntion
        if self.assign == "customized":
            return functions.assign(wm, self, self.data)
        # if custom assign fucntion doesn't exist, use default random function
        worker = wm.return_upcoming_worker()
        task = self.return_upcoming_task()
        return (worker, task)
