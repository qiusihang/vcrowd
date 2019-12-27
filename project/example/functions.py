#workermodel
import random

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
        for du in self.task.data_units:
            for i in range(len(du.data_row) - 1):
                n1 = du.data_row[i]
                n2 = du.data_row[i+1]
                steps = int(n1.get_distance(n2) / 5)
                for j in range(steps):
                    lat = n1.lat + (n2.lat-n1.lat)/steps*j
                    lng = n1.lng + (n2.lng-n1.lng)/steps*j
                    trees = data.tf.find_trees(lat, lng)
                    for tree in trees:
                        if random.random() < self.properties["accuracy"]: # it can be set by worker properties on web
                            data.res.append(tree)
        return self.properties["execution_time"]

    def submit(self):
    # must have this function
        if self.task is None:
            return
        for du in self.task.data_units:
            du.add_judgement(self, self.task, du)

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

import xml.dom.minidom
import matplotlib.pyplot as plt
import math

class Tree:
    def __init__(self, id, category, lat, lng):
        self.category = category
        self.lat = lat
        self.lng = lng
        self.id = id

class TreeFinder:

    def __init__(self, filename, initial_trees = [], grid_size = 5):
        self.tree_finder = []
        self.trees = initial_trees
        self.count = 0
        self.max_lat = -1e99
        self.min_lat = 1e99
        self.max_lng = -1e99
        self.min_lng = 1e99
        self.grid_size = grid_size
        tid = len(self.trees)
        if filename is not None and filename != "":
            for line in open(filename,'r'):
                temp = line.split(';')
                tree = Tree(tid, temp[0],float(temp[1]),float(temp[2]))
                tid += 1
                self.trees.append(tree)
        for tree in self.trees:
            self.max_lat = max(self.max_lat, tree.lat)
            self.min_lat = min(self.min_lat, tree.lat)
            self.max_lng = max(self.max_lng, tree.lng)
            self.min_lng = min(self.min_lng, tree.lng)
        w = LatLng(self.min_lat, self.min_lng).get_xy(LatLng(self.min_lat, self.max_lng)).x
        h = LatLng(self.min_lat, self.min_lng).get_xy(LatLng(self.max_lat, self.min_lng)).y
        self.n_lat = int(h / grid_size) + 1
        self.n_lng = int(w / grid_size) + 1
        self.k_lat = int((self.n_lat-1)/(self.max_lat-self.min_lat))
        self.k_lng = int((self.n_lng-1)/(self.max_lng-self.min_lng))
        for i in range(self.n_lat):
            self.tree_finder.append([])
            for j in range(self.n_lng):
                self.tree_finder[i].append([])
        self.tree_vis = [False for tree in self.trees]
        for tree in self.trees:
            self.add_tree(tree)

    def add_tree(self, tree):
        i = int((tree.lat - self.min_lat) * self.k_lat)
        j = int((tree.lng - self.min_lng) * self.k_lng)
        self.tree_finder[i][j].append(tree)
        self.count += 1

    def find_trees(self, lat, lng, radius = 5):
        trees = []
        grid_range = int((radius-0.1)/self.grid_size) + 1
        i = int((lat - self.min_lat) * self.k_lat)
        j = int((lng - self.min_lng) * self.k_lng)
        for p in range(i-grid_range,i+grid_range+1):
            for q in range(j-grid_range,j+grid_range+1):
                if 0 <= p and p < self.n_lat and 0<=q and q < self.n_lng:
                    for tree in self.tree_finder[p][q]:
                        if LatLng(lat,lng).get_distance(LatLng(tree.lat,tree.lng)) < radius:
                            trees.append(tree)
        return trees


class Cartesian:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class LatLng:

    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def get_latlng(self, x, y):
        return LatLng(self.lat + y/111300.0, self.lng + x/111300.0/math.cos(self.lat/180.0*math.pi))

    def get_xy(self, latlng):
        return Cartesian((latlng.lng - self.lng) * 111300.0 * math.cos(self.lat/180.0*math.pi), (latlng.lat - self.lat) * 111300.0)

    def get_distance(self,latlng):
        p = self.get_xy(latlng)
        return math.sqrt(p.x*p.x + p.y*p.y)


class RoadNetwork:

    def __init__(self, xml_filename):
        DOMTree = xml.dom.minidom.parse(xml_filename)
        self.roads = []
        root = DOMTree.documentElement
        xml_roads = root.getElementsByTagName("road")
        i = 0
        for xml_road in xml_roads:
            coords = []
            nodes = xml_road.getElementsByTagName("node")
            for node in nodes:
                coords.append(LatLng(float(node.getAttribute('lat')),float(node.getAttribute('lng'))) )
            self.roads.append(coords)
            i += 1

    def plot_map(self):
        plt.switch_backend('Agg')   # run matplotlib at the backend
        for road in self.roads:
            ndx = []
            ndy = []
            for node in road:
                ndy.append(node.lat)
                ndx.append(node.lng)
            plt.plot(ndx, ndy, lw = 0.5, c = [0.3,0.3,0.3])


def init(instance, worker_manager, task_manager, data):
    rn = RoadNetwork("project/example/road_network.xml")
    tf = TreeFinder("project/example/trees.csv")
    for r in rn.roads:
        data.add_data(r)
    data.rn = rn
    data.tf = tf
    data.res = []

def output(instance, worker_manager, task_manager, data):
    dict = {}
    n = 0
    for du in data.data_units:
        n += len(du.judgements)
    dict["cost"] = n * data.price
    dict["num_of_workers"] = len(worker_manager.workers)
    return dict

def final(instance, worker_manager, task_manager, data):
    plt.figure()
    data.rn.plot_map()
    px = []
    py = []
    for tree in data.res:
        px.append(tree.lng)
        py.append(tree.lat)
    plt.scatter(px,py,c=[0.3,0.8,0.3],marker='o',s=1)
    plt.savefig(instance.fig_location("tree_map"))
