import heapq


class PriorityQueue:
    """
    A priority queue specialized as event list
    """

    def __init__(self):
        self.heap = []
        heapq.heapify(self.heap)

    def __str__(self):
        return ' '.join([str(i) for i in self.heap])

    def isEmpty(self):
        return len(self.heap) == 0

    def push(self, event_start_time, event_type, request=None):
        heapq.heappush(self.heap, [event_start_time, event_type, request])

    def pop(self):
        event_start_time, event_type, request = heapq.heappop(self.heap)
        return event_start_time, event_type, request
