"""
Created on Apr 30, 2009

@author: opedge

    Example of 'graph': G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 
                           'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}
"""

from random import randint, random

class Graph:
    graph = {}

    def __init__(self, graph):
        self.graph = graph

    def findAllPaths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not self.graph.has_key(start):
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                newpaths = self.findAllPaths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def __len__(self):
        return len(self.graph)

    def getVertexes(self):
        return self.graph.keys()

    def pathExist(self, path):
        for i in range(len(path) - 1):
            if not self.graph[path[i]].has_key(path[i + 1]): return False
        return True

    def pathCost(self, path):
        if not self.pathExist(path): return float('inf')
        return sum(self.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def findShortestPathDijkstra(self, start, end, path=[]):
        '''
        Simple implementation of Dijkstra algorithm.
        May be used for testing purpose.
        '''
        path = path + [start]
        if start == end:
            return path
        if not self.graph.has_key(start):
            return None
        shortest = None
        for node in self.graph[start].keys():
            if node not in path:
                newpath = self.findShortestPathDijkstra(node, end, path)
                if newpath:
                    if not shortest or self.pathCost(newpath) < self.pathCost(shortest):
                        shortest = newpath
        return shortest

    def __getitem__(self, n):
        return self.graph[n]

def generateRandomGraph(numVertex, maxLength=100, oriented=False, connectivity=0.5):
    '''
    Generates random graph
    '''
    gd = {}
    for i in range(numVertex):
        costs = {}
        for k in range(numVertex):
            if k != i:
                if random() > connectivity:
                    costs[k] = float('inf')
                if not oriented and gd.has_key(k) and gd[k].has_key(i):
                    costs[k] = gd[k][i]
                else:
                    if not costs.has_key(k):
                        costs[k] = randint(1, maxLength)
            else:
                costs[k] = 0
        gd[i] = costs
    return Graph(gd)
