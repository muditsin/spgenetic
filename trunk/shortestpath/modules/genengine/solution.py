'''
Created on May 1, 2009

@author: opedge
'''

from organism import OrganismFactory

class Solution(object):
    '''
    Base class for problem solution
    '''
    def __init__(self, orgFactory):
        if issubclass(orgFactory.__class__, OrganismFactory):
            self.orgFactory = orgFactory
        else:
            raise TypeError("Only 'OrganismFactory' is allowed")

    def solve(self):
        raise NotImplementedError("Method 'solve' not implemented")
