'''
Created on Apr 28, 2009

@author: opedge
'''

from random import random, choice, randint

class BaseOrganism:
    '''
    Abstract organism
    '''
    def __add__(self, partner):
        return self.cross(partner)

    def fitness(self):
        raise NotImplementedError("Method 'fitness' not implemented")

    def __cmp__(self, other):
        return cmp(self.fitness(), other.fitness())

    def cross(self, partner):
        '''
        Mates with another organism
        '''
        raise NotImplementedError("Method 'cross' not implemented")

    def __repr__(self):
        return str(self.__class__.__name__)

    def mutate(self):
        raise NotImplementedError("Method 'mutate' not implemented")

class Organism(BaseOrganism):
    '''
    Simple organism with simple sequence of genes
    '''
    genes = []

    crossoverRate = 0.5

    def __init__(self, genes, **kw):
        if isinstance(genes, tuple) or isinstance(genes, list):
            self.genes = genes
            self.kw = kw
        else:
            raise TypeError("Only list and tuple allowed")

    def cross(self, partner):
        genes1 = []
        genes2 = []

        for i in range(len(self.genes)):
            ourGene = self.genes[i]
            partnerGene = partner[i]
            if random() < self.crossoverRate:
                genes1.append(ourGene)
                genes2.append(partnerGene)
            else:
                genes1.append(partnerGene)
                genes2.append(ourGene)

        child1 = self.makeChild(genes1)
        child2 = self.makeChild(genes2)
        return (child1, child2)

    def makeChild(self, genes):
        return self.__class__(genes)

    def copy(self):
        return self.__class__(self.genes)

    def mutate(self):
        mutant = self.copy()
        gene = choice(self.genes)
        mutant[randint(0, len(mutant) - 1)] = gene
        return mutant

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, n):
        return self.genes[n]

    def __repr__(self):
        return str(self.genes)

class OrganismFactory():

    def newOrganism(self, genes):
        raise NotImplementedError("Method 'newOrganism' not implemented")
