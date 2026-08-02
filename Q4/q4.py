import heapq

class node():
    def __init__(self,name ):
        self.name = name
        self.nighber_distance = []

    def add_nighber(self, nighber , distance) :
        self.nighber_distance.append((nighber , distance))


class Solution(object):
    def networkDelayTime(self, times, n, k):
        """
        :type times: List[List[int]]
        :type n: int
        :type k: int
        :rtype: int
        """
        nodes = {}
        for i in range(1, n + 1):
            nodes[i] = node(i)

        for source, neighber, weight in times:
            nodes[source].add_nighber(neighber, weight)


        distance_source = {}
        min_heap = []
        heapq.heappush(min_heap , (0 , k))
        while min_heap :
            distance , source =heapq.heappop(min_heap)
            if source in distance_source:
                continue
            distance_source[source] = distance
            for j in nodes[source].nighber_distance :
                heapq.heappush(min_heap , (distance + j[1] , j[0]))

        if len(distance_source) < n :
            return -1 
        return max(distance_source.values)
