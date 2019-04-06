from worker import *
from task import *
from data import *
from event import *
from settingparser import *
import random
import datetime
import os
import shutil
import numpy as np

class Instance:

    def __init__(self, filename = "simulation.setting"):
        # self.agents = []
        self.data = Data()
        self.wm = WorkerManager()
        self.tm = TaskManager(self.data)
        self.simulation_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.setting  = SettingParser(filename, self.wm, self.tm, self.data) # read simulation settings
        self.time = 0 # set simulation clock
        self.event_heap = EventHeap(key=lambda x:x.time)

        if not os.path.exists("output"):
            os.makedirs("output")
        if not os.path.exists("output/"+self.simulation_id):
            os.makedirs("output/"+self.simulation_id)
        shutil.copyfile(filename,"output/"+self.simulation_id+"/"+filename)


    def run(self, end_time = 3600):
         # add first event create_agent
        self.event_heap.push(Event("create_agent",np.random.poisson(self.wm.worker_arrival_interval,1)[0]))

        # add events output
        k = 1
        while True:
            t = k * self.setting.time_stamp
            if t >= end_time: break
            self.event_heap.push(Event("output",t))
            k += 1

        # add event finish
        self.event_heap.push(Event("finish", end_time))

        while True:
            # get first event from heap
            event = self.event_heap.pop()
            self.time = event.time # update simulation clock

            if event.type == "create_agent":
                # push new worker to waiting queue
                self.wm.add_worker()
                # arrange the arrival of the next worker
                self.event_heap.push(Event("create_agent",self.time + np.random.poisson(self.wm.worker_arrival_interval,1)[0]))
                if len(self.tm.tasks) > 0: # still has task to do
                    (worker, task) = self.tm.assign_task(self.wm)
                    if worker is not None and task is not None:
                        worker.task = task
                        wm.remove_worker(worker)
                        self.remove_task(task)
                        execution_time = worker.execute()
                        if execution_time < self.wm.dropout_time:
                            self.event_heap.push(Event("agent_finish_task",self.time + execution_time, worker))

            if event.type == "agent_finish_task":
                event.agent.submit()

            if event.type == "output":
                self.output()

            if event.type == "finish":
                self.output()
                return


    def output(self):
        print(len(self.wm.workers))
    #     for property in self.setting.output_properties:
    #         foldername = "output/"+self.simulation_id+"/"+property
