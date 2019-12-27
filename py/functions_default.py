#workermodel
class Worker:

    def __init__(self, wid, classification, properties):
    # do not change input parameters - it is used for initialize a worker
        self.wid = wid
        self.classification = classification
        self.properties = properties
        self.task = None # it will be assigned by task assignment strategy

    def execute(self, worker_manager, task_manager, data):
    # must have this function
    # this function returns the actual execution time
        return self.properties["execution_time"]

    def submit(self):
    # must have this function
        if self.task is None:
            return
        for du in self.task.data_units:
            j = Judgement(self, self.task, du)
            du.judgements.append(j)

#taskmodel
class Task:

    def __init__(self, tid, data_units):
    # do not change input parameters - it is used for initialize a task
        self.tid = tid
        self.data_units = data_units
        self.properties = {} # configurable

#workerslt
def worker_seletion(worker):
# do not change input parameters - it returns if a worker is qualified (true)
    return True

#taskgen
def task_generation(data, n_data_rows):
# do not change input parameters - it returns data_units for creating a new task
    data_units = data.random_selection(n_data_rows)
    return data_units

#taskassign
def assign(worker_manager, task_manager, data):
    worker = wm.return_upcoming_worker()
    task = tm.return_upcoming_task()
    return (worker, task)

#others

def init(instance, worker_manager, task_manager, data):
    "Do something"

def output(instance, worker_manager, task_manager, data):
    dict = {}
    dict["num_of_workers"] = len(worker_manager.workers)
    return dict

def final(instance, worker_manager, task_manager, data):
    "Do something"
