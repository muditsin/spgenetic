'''
Created on May 1, 2009

@author: opedge
'''

from applications.shortestpath.modules.genengine.organism import Organism, OrganismFactory
from applications.shortestpath.modules.genengine.population import Population
from applications.shortestpath.modules.genengine.solution import Solution
from applications.shortestpath.modules.shortestpath.graph import Graph
from random import choice

class SPOrganismFactory(OrganismFactory):

    def __init__(self, graph):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            raise TypeError("Must be 'Graph' object")

    def newOrganism(self, genes):
        return SPOrganism(genes, self.graph)

class SPOrganism(Organism):

    def __init__(self, gens, graph):
        Organism.__init__(self, gens)
        self.graph = graph

    def makeChild(self, gens):
        return self.__class__(gens, self.graph)

    def fitness(self):
        return self.graph.pathCost(self.genes)

class SPSolution(Solution):
    '''
    Solution of shortest path problem
    '''
    def __init__(self, graph, start, stop, initPopulationLength=1000,
                 genesCount=10, populationCount=300,
                 childCull=200, childCount=1000, goodParents=10, mutants=0.1):
        Solution.__init__(self, SPOrganismFactory(graph))
        self.graph = graph
        self.start, self.stop = start, stop
        self.initPopulationLength = initPopulationLength
        self.genesCount = genesCount
        self.populationCount = populationCount
        self.childCull = 200
        self.childCount = childCount
        self.goodParents = goodParents
        self.mutants = mutants

    def generateRandomSPOrganism(self):
        genes = [self.start]
        for i in range(self.genesCount - 2):
            genes.append(choice(self.graph.getVertexes()))
        genes.append(self.stop)
        return self.orgFactory.newOrganism(genes)

    def generateInitPopulation(self):
        '''
        Generate random init population
        '''
        p = Population(childCull=self.childCull, childCount=self.childCount,
                       goodParents=self.goodParents, mutants=self.mutants)
        for i in range(self.initPopulationLength):
            p.add(self.generateRandomSPOrganism())
        return p

    def bestIterator(self):
        population = self.generateInitPopulation()
        for i in range(self.populationCount):
            population.generate()
            yield population.best()

    def solve(self):
        '''
        Main method
        '''

        population = self.generateInitPopulation()
        for i in range(self.populationCount):
            population.generate()
        return population.best()
