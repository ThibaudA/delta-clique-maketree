import random
import unittest
from CliqueMaster import CliqueMaster
from Clique import Clique
from CliqueCritique import CliqueCritique
from collections import deque
import sys
import os

		#(X,(tlimitb,tlimite),deltamin,deltamax,tp,td) = c

class TestClique(unittest.TestCase):
	def setUp(self):
		self.Cm = CliqueMaster()
		self.seq = range(10)
		sys.stderr = open(os.devnull, 'w')


	def test_singlelinktopbot(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)))

		])
		self.Cm._nodestop = {1: set([2])}
		self.Cm._nodesbot = {2: set([1])}
		self.Cm._nodes = {1: set([2]),2: set([1])}

		self.Cm._times = {frozenset([1, 2]): [1]}

		R = self.Cm.getTree(10)
		R_expected = set([
			
			CliqueCritique((frozenset([1,2]), (1,1),0,10,1,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

 	def test_SimpleTriangle(self):
 		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1))),
		    Clique((frozenset([1, 3]), (2, 2),(2,2)))
		])
		
		self.Cm._nodestop = {1: set([2,3])}
		self.Cm._nodesbot = {2: set([1]), 3: set([1])}
		self.Cm._nodes = {1: set([2,3]), 2: set([1]), 3: set([1])}
		self.Cm._times = {frozenset([1, 2]): [1],frozenset([1,3]): [2]}

		R = self.Cm.getTree(10)
		R_expected = set([
			
			CliqueCritique((frozenset([1,2]), (1,1),0,10,1,1)),
			CliqueCritique((frozenset([1,3]), (2,2),0,10,2,2)),
			CliqueCritique((frozenset([1,2,3]), (1,2),1,10,1,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

 	def test_Simplesquare(self):
 		self.Cm._S = deque([
		    Clique((frozenset([1, 3]), (1, 1),(1,1))),
		    Clique((frozenset([1, 4]), (2, 2),(2,2))),
		    Clique((frozenset([2, 3]), (3, 3),(3,3))),
		    Clique((frozenset([2, 4]), (4, 4),(4,4)))
		])
		
		self.Cm._nodestop = {1: set([4,3]), 2: set([4,3])}
		self.Cm._nodesbot = {3: set([1,2]), 4: set([1,2])}
		self.Cm._nodes = {1: set([4,3]), 2: set([3,4]), 3: set([1,2]), 4: set([1,2])}
		self.Cm._times = {frozenset([1, 3]): [1],frozenset([1,4]): [2],frozenset([2,3]): [3],frozenset([4,2]): [4]}

		R = self.Cm.getTree(10)
		R_expected = set([
			
			CliqueCritique((frozenset([1,2]), (1,1),0,10,1,1)),
			CliqueCritique((frozenset([1,3]), (2,2),0,10,2,2)),
			CliqueCritique((frozenset([4,2]), (3,3),0,10,3,3)),
			CliqueCritique((frozenset([4,3]), (4,4),0,10,4,4)),
			CliqueCritique((frozenset([1,2,3]), (1,3),2,10,1,3)),
			CliqueCritique((frozenset([2,3,4]), (2,4),2,10,2,4)),
			CliqueCritique((frozenset([1,3,4]), (1,2),1,10,1,2)),
			CliqueCritique((frozenset([2,3,4]), (3,4),1,10,3,4)),
			CliqueCritique((frozenset([1,2,3,4]), (1,4),3,10,1,4))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestClique)
	unittest.TextTestRunner(verbosity=2).run(suite)
