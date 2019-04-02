import util
from enum import Enum
import random
from util import PriorityQueue
from collections import deque

mean_service_time = 0.8
mean_interarrvial_time = 1.0
MAX_CUSTOMERS_TO_SERVICE = 30000


class EventType(Enum):
    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"


sim_time = 0.0
event_list = PriorityQueue()


class Request:
    def __init__(self, creation_time):
        self.creation_time = creation_time

    def __repr__(self):
        return str("(Request creation time = " + str(round(self.creation_time, 6)) + ")")


class Server:
    def __init__(self, mean_service_time):
        print("Server: Created ", mean_service_time)
        self.mean_service_time = mean_service_time
        self.queue = deque([])
        self.is_busy = False
        self.customers_serviced = 0

    def handleDeparture(self, request):
        print(str(sim_time) + "   \t: ", request, "   \tDeparted ")
        self.customers_serviced += 1
        if len(self.queue) == 0:
            # No requests present in queue
            self.is_busy = False
        else:
            self.is_busy = True
            request = self.queue.popleft()
            # Returns an exponential random variable with mean equal to mean_service_time
            service_time = random.expovariate(1.0/mean_service_time)
            # Add a departure event to the event_list
            event_list.push(sim_time + service_time,
                            EventType.DEPARTURE, request)

    def handleArrival(self, request):
        print(str(sim_time) + "   \t: ", request, "   \tArrived ")
        if not self.is_busy:
            self.is_busy = True
            # Returns an exponential random variable with mean equal to mean_service_time
            service_time = random.expovariate(1.0/mean_service_time)
            # Add a departure event to the event_list
            event_list.push(sim_time + service_time,
                            EventType.DEPARTURE, request)
        else:
            # Add the request to the queue
            self.queue.append(request)

    def getNumberOfCustomersServiced(self):
        return self.customers_serviced


server = Server(mean_service_time)
event_list.push(sim_time, EventType.ARRIVAL, Request(sim_time))

# Main loop to process events until it is empty or number of customers handled execeeds given limit
while not (event_list.isEmpty() or server.getNumberOfCustomersServiced() == MAX_CUSTOMERS_TO_SERVICE):
    event_start_time, event_type, request = event_list.pop()
    sim_time = event_start_time
    if event_type == EventType.DEPARTURE:
        # print("departure")
        server.handleDeparture(request)
    elif event_type == EventType.ARRIVAL:
        # print("arrival")
        server.handleArrival(request)
        # Returns an exponential random variable with mean equal to mean_service_time
        interarrvial_time = random.expovariate(1.0/mean_interarrvial_time)
        event_list.push(sim_time + interarrvial_time, EventType.ARRIVAL,
                        Request(sim_time + interarrvial_time))