from worker import *
from task import *
from data import *
from event import *
from settingparser import *
import random
import datetime
import os
import shutil
import importlib
import numpy as np
import matplotlib.pyplot as plt

class Instance:

    def __init__(self, filename):
        # self.agents = []
        self.data = Data()
        self.wm = WorkerManager()
        self.tm = TaskManager(self.data)
        self.setting  = SettingParser(filename, self.wm, self.tm, self.data) # read simulation settings
        # self.simulation_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.simulation_id = self.setting.pid
        self.time = 0 # set simulation clock
        self.event_heap = EventHeap(key=lambda x:x.time)
        self.output_data = []
        self.range = []

        if not os.path.exists("output"):
            os.makedirs("output")
        if not os.path.exists("output/"+self.simulation_id):
            os.makedirs("output/"+self.simulation_id)
        shutil.copyfile(filename,"output/"+self.simulation_id+"/settings.json")

        self.functions =  __import__("functions")
        importlib.reload(self.functions)
        self.functions.init(self, self.wm, self.tm, self.data)


    def run(self):
        # generate task
        for i in range(len(self.data.data_units)):
            self.tm.add_task()

        # add first event create_agent
        self.event_heap.push(Event("create_agent",np.random.poisson(self.wm.worker_arrival_interval,1)[0]))

        # add events output
        k = 1
        while True:
            t = k * self.setting.time_stamp
            if t >= self.setting.runtime: break
            self.event_heap.push(Event("output",t))
            k += 1

        # add event finish
        self.event_heap.push(Event("finish", self.setting.runtime))

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
                        self.wm.remove_worker(worker)
                        self.tm.remove_task(task)
                        execution_time = worker.execute(self.wm, self.tm, self.data)
                        if execution_time < self.wm.dropout_time:
                            self.event_heap.push(Event("agent_finish_task",self.time + execution_time, worker))

            if event.type == "agent_finish_task":
                event.agent.submit()

            if event.type == "output":
                self.output()

            if event.type == "finish":
                self.finish()
                return

    def output(self):
        self.range.append(self.time)
        self.output_data.append(self.functions.output(self, self.wm, self.tm, self.data))

    def fig_location(self, prop):
        return "output/"+str(self.simulation_id)+"/fig/"+prop+".png"

    def plot(self,range):
        plt.switch_backend('Agg')   # run matplotlib at the backend
        for prop in self.output_data[0].keys():
            d = []
            l = 0
            for i,t in enumerate(self.range):
                if prop in self.output_data[i]:
                    l = self.output_data[i][prop]
                d.append(l)
            plt.figure()
            plt.plot(range,d)
            plt.xlabel("time (s)")
            plt.ylabel(prop)
            plt.savefig(self.fig_location(prop))

    def finish(self):
        self.output()
        foldername = "output/"+str(self.simulation_id)
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        if os.path.exists(foldername+"/fig"):
            shutil.rmtree(foldername+"/fig")
        os.makedirs(foldername+"/fig")
        f = open(foldername+"/data.txt","w")
        f.write(json.dumps(self.output_data))
        f.close()
        f = open(foldername+"/range.txt","w")
        f.write(json.dumps(self.range))
        f.close()
        self.plot(self.range)
        self.functions.final(self, self.wm, self.tm, self.data)
