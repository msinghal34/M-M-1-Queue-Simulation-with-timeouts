import random
from enum import Enum
from collections import deque
from util import PriorityQueue


class EventType(Enum):
    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"


class Request:
    def __init__(self, creation_time):
        self.creation_time = creation_time

    def __repr__(self):
        return str("(Request creation time = " + str(round(self.creation_time, 6)) + ")")


class Server:
    def __init__(self, mean_service_time):
        self.mean_service_time = mean_service_time
        self.queue = deque([])
        self.is_busy = False
        self.customers_serviced = 0
        self.response_time_so_far = 0.0

    def handleDeparture(self, request, sim_time, event_list, verbose=True):
        if verbose:
            print(str(sim_time) + "   \t: ", request, "   \tDeparted ")

        # Updating metrics
        self.customers_serviced += 1
        self.response_time_so_far += (sim_time - request.creation_time)

        if len(self.queue) == 0:
            # No requests present in queue
            self.is_busy = False

        else:
            self.is_busy = True
            request = self.queue.popleft()

            # Returns an exponential random variable with mean equal to mean_service_time
            service_time = random.expovariate(1.0/self.mean_service_time)

            # Add a departure event to the event_list
            event_list.push(sim_time + service_time,
                            EventType.DEPARTURE, request)

    def handleArrival(self, request, sim_time, event_list, verbose=True):
        if verbose:
            print(str(sim_time) + "   \t: ", request, "   \tArrived ")

        if not self.is_busy:
            # If server is idle
            self.is_busy = True

            # Returns an exponential random variable with mean equal to mean_service_time
            service_time = random.expovariate(1.0/self.mean_service_time)

            # Add a departure event to the event_list
            event_list.push(sim_time + service_time,
                            EventType.DEPARTURE, request)
        else:
            # Add the request to the queue
            self.queue.append(request)

    def getNumberOfCustomersServiced(self):
        return self.customers_serviced

    def getStatus(self):
        return self.is_busy

    def getQueueLength(self):
        return len(self.queue)

    def getTotalResponseTime(self):
        return self.response_time_so_far


# Taking all needed user inputs
mean_service_time = float(
    input("Enter mean service time of server: "))
mean_interarrvial_time = float(
    input("Enter mean interarrival time of requests: "))
MAX_CUSTOMERS_TO_SERVICE = int(
    input("Enter maximum number of customers to service before stopping a run: "))
NUM_OF_RUNS = int(
    input("Enter number of runs: "))
verbose = bool(int(
    input("Type 1 for verbose and 0 for no verbose: ")))


def run(i, mean_service_time, mean_interarrvial_time, MAX_CUSTOMERS_TO_SERVICE):
    # Initialization
    event_list = PriorityQueue()
    sim_time = 0.0
    server = Server(mean_service_time)
    # Initializing the event_list by adding the first arrival
    interarrvial_time = random.expovariate(1.0/mean_interarrvial_time)
    event_list.push(sim_time + interarrvial_time, EventType.ARRIVAL,
                    Request(sim_time + interarrvial_time))

    # Metrics
    utilization_time = 0.0
    queue_length_area = 0

    # Main loop to process events until it is empty or number of customers handled execeeds given limit
    while not (event_list.isEmpty() or server.getNumberOfCustomersServiced() == MAX_CUSTOMERS_TO_SERVICE):
        event_start_time, event_type, request = event_list.pop()
        prev_sim_time = sim_time
        sim_time = event_start_time

        if event_type == EventType.DEPARTURE:
            utilization_time += (sim_time - prev_sim_time)
            queue_length_area += (sim_time - prev_sim_time) * \
                server.getQueueLength()
            server.handleDeparture(request, sim_time, event_list, verbose)

        elif event_type == EventType.ARRIVAL:
            if (server.getStatus() == True):
                utilization_time += (sim_time - prev_sim_time)
            queue_length_area += (sim_time - prev_sim_time) * \
                server.getQueueLength()
            server.handleArrival(request, sim_time, event_list, verbose)
            # Next arrival will happen after interarrival_time
            interarrvial_time = random.expovariate(1.0/mean_interarrvial_time)
            event_list.push(sim_time + interarrvial_time, EventType.ARRIVAL,
                            Request(sim_time + interarrvial_time))

    # Printing metrics of a run
    assert server.getNumberOfCustomersServiced() == MAX_CUSTOMERS_TO_SERVICE
    total_time = sim_time
    response_time_so_far = server.getTotalResponseTime()
    utilization = utilization_time/total_time
    queue_length = queue_length_area/total_time
    response_time = response_time_so_far/MAX_CUSTOMERS_TO_SERVICE
    throughput = MAX_CUSTOMERS_TO_SERVICE/total_time
    print("")
    print("Server Utilization: \t", utilization)
    print("Average Queue Length: \t", queue_length)
    print("Average Response Time: \t", response_time)
    print("Throughput: \t\t", throughput)
    return utilization, queue_length, response_time, throughput


# Average metrics for each run
avg_utilization = []
avg_queue_length = []
avg_response_time = []
avg_throughput = []


def mean(list_):
    """
    Returns mean of elements in a list
    """
    return sum(list_)/len(list_)


# Looping for each run to accumulate statistics
for i in range(NUM_OF_RUNS):
    print("--------------------------------------------------")
    print("Run " + str(i))
    utilization, queue_length, response_time, throughput = run(
        i, mean_service_time, mean_interarrvial_time, MAX_CUSTOMERS_TO_SERVICE)
    avg_utilization.append(utilization)
    avg_queue_length.append(queue_length)
    avg_response_time.append(response_time)
    avg_throughput.append(throughput)
print("\n################## STATISITCS ################################")
print("Server Utilization: \t", mean(avg_utilization))
print("Queue Length: \t\t", mean(avg_queue_length))
print("Response Time: \t\t", mean(avg_response_time))
print("Throughput: \t\t", mean(avg_throughput))