import heapq

class Event:

    def __init__(self, type, time, agent = None):
        self.type = type
        self.time = time
        self.agent = agent

class EventHeap:

    def __init__(self, key=lambda x:x):
        self.key = key
        self._data = []
        self.count = 0

    def push(self, item):
        self.count += 1
        heapq.heappush(self._data, [self.key(item), self.count, item])

    def pop(self):
        return heapq.heappop(self._data)[2]

    def heapify(self):
        heapq.heapify(self._data)
