'''
Created on Apr 30, 2009

@author: opedge
'''

from organism import Organism, BaseOrganism
from random import randrange
from math import sqrt

class Population:
    '''
    Organisms population
    '''

    def __init__(self, childCull=200, childCount=1000, goodParents=10, mutants=0.1):
        self.sorted = False
        self.organisms = []
        self.childCull = childCull
        self.childCount = childCount
        self.goodParents = goodParents
        self.mutants = mutants

    def add(self, *args):
        for arg in args:
            if isinstance(arg, tuple) or isinstance(arg, list):
                self.add(*arg)
            if issubclass(arg.__class__, BaseOrganism):
                self.organisms.append(arg)
            elif issubclass(arg.__class__, Population):
                self.organisms.extend(arg)
            else:
                raise TypeError("Only organisms and populations can be added")

    def __repr__(self):
        return str(self.organisms)

    def __getitem__(self, n):
        self.sort();
        return self.organisms[n]

    def __len__(self):
        return len(self.organisms)

    def fitness(self):
        fitnesses = map(lambda org: org.fitness(), self.organisms)
        return sum(fitnesses) / len(fitnesses)

    def best(self):
        self.sort()
        return self[0]

    def sort(self):
        if not self.sorted:
            self.organisms.sort()
            self.sorted = True

    def generate(self, nfittest=None, nchildren=None):
        if not nfittest:
            nfittest = self.childCull
        if not nchildren:
            nchildren = self.childCount

        children = []

        self.sort()
        nadults = len(self)
        n2adults = nadults * nadults

        #wild orgy
        for i in range(nchildren):
            #pick random parent
            i1 = i2 = int(sqrt(randrange(n2adults)))
            parent1 = self[-i1]

            while i2 == i1:
                i2 = int(sqrt(randrange(n2adults)))
            parent2 = self[-i2]

            child1, child2 = parent1 + parent2

            children.extend([child1, child2])

        if self.goodParents:
            children.extend(self[:self.goodParents])

        children.sort()

        #add a proportion of mutants
        nchildren = len(children)
        n2children = nchildren * nchildren
        mutants = []
        numMutants = int(nchildren * self.mutants)

        for i in range(numMutants):
            #pick one random child
            id = int(sqrt(randrange(n2children)))
            child = children[-id]
            mutants.append(child)

        children.extend(mutants)

        children.sort()

        #make new population
        self.organisms[:] = children[:nfittest]

        self.sorted = True
