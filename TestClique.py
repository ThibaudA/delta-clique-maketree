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

	def test_delta_is_0(self):
		self.Cm._S = deque([
			Clique((frozenset([1,2]), (1,1),(1,1)),set([]))
		])	
		self.Cm._times = {frozenset([1,2]):[1]}
		self.Cm._nodes = {1:set([2]), 2:set([1])}
		R = self.Cm.getTree(10)
		self.assertEqual(R, set([CliqueCritique((frozenset([1,2]), (1,1),0,10,1,1))]))

	def test_negative_delta(self):
		pass

	def test_big_delta(self):
		self.Cm._S = deque([
			Clique((frozenset([1,2]), (1,1),(1,1)),set([]))
		])	
		self.Cm._times = {frozenset([1,2]):[1]}
		self.Cm._nodes = {1:set([2]), 2:set([1])}
		R = self.Cm.getTree(100)
		self.assertEqual(R, set([CliqueCritique((frozenset([1,2]), (1,1),0,100,1,1))]))

	def test_simple_triangle_when_delta_is_5(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([1, 3]), (2, 2),(2,2)),set([])),
		    Clique((frozenset([2, 3]), (3, 3),(3,3)),set([]))
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [2], frozenset([1, 2]): [1], frozenset([2, 3]): [3]}

		R = self.Cm.getTree(5)
		R_expected = set([

			CliqueCritique((frozenset([1,2,3]), (1,3),2,5,1,3)),
			CliqueCritique((frozenset([1,2]), (1,1),0,5,1,1)),
			CliqueCritique((frozenset([2,3]), (3,3),0,5,3,3)),
			CliqueCritique((frozenset([1,3]), (2,2),0,5,2,2))
		])

		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"

		self.assertEqual(R, R_expected, debug_msg)		

	def test_two_links_alterning(self):
		pass
	
	def test_single_link_occurring_every_delta(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([1, 2]), (3, 3),(3,3)),set([]))
		])
		self.Cm._nodes = {1: set([2]), 2: set([1])}
		self.Cm._times = {frozenset([1, 2]): [1, 3]}
		
		R = self.Cm.getTree(5)
		R_expected = set([

			CliqueCritique((frozenset([1,2]), (1,1),0,2,1,1)),
			CliqueCritique((frozenset([1,2]), (3,3),0,2,3,3)),
			CliqueCritique((frozenset([1,2]), (1,3),2,5,3,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_single_link_not_occurring_every_delta(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([1, 2]), (3, 3),(3,3)),set([]))
		])
		self.Cm._nodes = {1: set([2]), 2: set([1])}
		self.Cm._times = {frozenset([1, 2]): [1, 3]}
		
		R = self.Cm.getTree(1)
		

		R_expected = set([
			CliqueCritique((frozenset([1,2]), (1,1),0,1,1,1)),
			CliqueCritique((frozenset([1,2]), (3,3),0,1,3,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)
		
	def test_triangle_and_many_occurrences_with_delta_too_small(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([2, 3]), (2, 2),(2,2)),set([])),
		    Clique((frozenset([1, 3]), (3, 3),(3,3)),set([])),
		    Clique((frozenset([1, 2]), (4, 4),(4,4)),set([]))
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getTree(2)
		R_expected = set([
			CliqueCritique((frozenset([1,2]), (1,1),0,2,1,1)),
			CliqueCritique((frozenset([1,2]), (4,4),0,2,4,4)),
			CliqueCritique((frozenset([1,3]), (3,3),0,2,3,3)),
			CliqueCritique((frozenset([2,3]), (2,2),0,2,2,2)),
			CliqueCritique((frozenset([1,2,3]), (1,3),2,2,1,3)),
			CliqueCritique((frozenset([1,2,3]), (2,4),2,2,2,4))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"

		self.assertEqual(R, R_expected, debug_msg)		

	def test_triangle_and_many_occurrences_with_delta_big(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([2, 3]), (2, 2),(2,2)),set([])),
		    Clique((frozenset([1, 3]), (3, 3),(3,3)),set([])),
		    Clique((frozenset([1, 2]), (4, 4),(4,4)),set([]))
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getTree(5)
		R_expected = set([
			CliqueCritique((frozenset([1,2]), (1,1),0,3,1,1)),
			CliqueCritique((frozenset([1,2]), (4,4),0,3,4,4)),
			CliqueCritique((frozenset([1,2]), (1,4),3,5,4,1)),

			CliqueCritique((frozenset([1,3]), (3,3),0,5,3,3)),
			CliqueCritique((frozenset([2,3]), (2,2),0,5,2,2)),

			CliqueCritique((frozenset([1,2,3]), (1,3),2,3,1,3)),
			CliqueCritique((frozenset([1,2,3]), (2,4),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]), (1,4),3,5,2,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_triangle_and_many_occurrences_with_delta_huge(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1)),set([])),
		    Clique((frozenset([2, 3]), (2, 2),(2,2)),set([])),
		    Clique((frozenset([1, 3]), (3, 3),(3,3)),set([])),
		    Clique((frozenset([1, 2]), (4, 4),(4,4)),set([]))
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getTree(100)
		R_expected = set([
			CliqueCritique((frozenset([1,2]), (1,1),0,3,1,1)),
			CliqueCritique((frozenset([1,2]), (4,4),0,3,4,4)),
			CliqueCritique((frozenset([1,2]), (1,4),3,100,4,1)),

			CliqueCritique((frozenset([1,3]), (3,3),0,100,3,3)),
			CliqueCritique((frozenset([2,3]), (2,2),0,100,2,2)),

			CliqueCritique((frozenset([1,2,3]), (1,3),2,3,1,3)),
			CliqueCritique((frozenset([1,2,3]), (2,4),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]), (1,4),3,100,2,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)



	def test_simultaneouslinks(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1))),
		    Clique((frozenset([2, 3]), (1, 1),(1,1))),
		    Clique((frozenset([1, 3]), (1, 1),(1,1))),
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [1], frozenset([1, 2]): [1], frozenset([2, 3]): [1]}

		R = self.Cm.getTree(100)
		R_expected = set([
			CliqueCritique((frozenset([1,2,3]), (1,1),0,100,1,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_simultaneouslinkswithadoublelink(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1))),
		    Clique((frozenset([2, 3]), (1, 1),(1,1))),
		    Clique((frozenset([1, 3]), (1, 1),(1,1))),
		    Clique((frozenset([2, 3]), (2, 2),(2,2)))
		])
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [1], frozenset([1, 2]): [1], frozenset([2, 3]): [1,2]}

		R = self.Cm.getTree(5)
		R_expected = set([
			CliqueCritique((frozenset([1,2,3]), (1,2),1,5,1,1)),
			CliqueCritique((frozenset([1,2,3]), (1,1),0,1,1,1)),
			CliqueCritique((frozenset([2,3]), (1,2),1,5,2,1)),
			CliqueCritique((frozenset([2,3]), (2,2),0,1,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_extensionvsdeltamax(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 2]), (1, 1),(1,1))),
		    Clique((frozenset([2, 3]), (2, 2),(2,2))),
		    Clique((frozenset([1, 2]), (3, 3),(3,3))),
		    Clique((frozenset([1, 2]), (6, 6),(6,6))),

		])
		self.Cm._nodes = {1: set([2]), 2: set([1, 3]), 3: set([2])}
		self.Cm._times = {frozenset([1, 2]): [1,3,6], frozenset([2, 3]): [2]}

		R = self.Cm.getTree(10)
		R_expected = set([
			
			CliqueCritique((frozenset([2,3]), (2,2),0,10,2,2)),
			CliqueCritique((frozenset([1,2]), (1,1),0,2,1,1)),
			CliqueCritique((frozenset([1,2]), (3,3),0,2,3,3)),
			CliqueCritique((frozenset([1,2]), (1,3),2,3,3,1)),
			CliqueCritique((frozenset([1,2]), (6,6),0,3,6,6)),
			CliqueCritique((frozenset([1,2]), (1,6),3,10,6,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)


	def test_ajoutdenoeudwhenmax(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 3]), (1, 1),(1,1))),
		    Clique((frozenset([1, 2]), (2, 2),(2,2))),
		    Clique((frozenset([2, 3]), (2, 2),(2,2))),
		    Clique((frozenset([1, 3]), (4, 4),(4,4))),

		])
		self.Cm._nodes = {1: set([2,3]), 2: set([1, 3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [2], frozenset([2, 3]): [2],frozenset([1, 3]): [1,4]}

		R = self.Cm.getTree(5)
		R_expected = set([
			
			CliqueCritique((frozenset([1,3]), (4,4),0,3,4,4)),
			CliqueCritique((frozenset([1,3]), (1,1),0,3,1,1)),
			CliqueCritique((frozenset([1,3]), (1,4),3,5,4,1)),
			CliqueCritique((frozenset([1,2]), (2,2),0,3,2,2)),
			CliqueCritique((frozenset([2,3]), (2,2),0,3,2,2)),

			CliqueCritique((frozenset([1,2,3]), (1,2),1,3,1,2)),
			CliqueCritique((frozenset([1,2,3]), (2,4),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]), (1,4),3,5,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)




	def test_ajoutdenoeudwhenmaxsuivitdajoutdelien(self):
		self.Cm._S = deque([
		    Clique((frozenset([1, 3]), (1, 1),(1,1))),
		    Clique((frozenset([1, 2]), (2, 2),(2,2))),
		    Clique((frozenset([2, 3]), (2, 2),(2,2))),
		    Clique((frozenset([1, 3]), (3, 3),(3,3))),
		    Clique((frozenset([1, 3]), (5, 5),(5,5))),
		])
		self.Cm._nodes = {1: set([2,3]), 2: set([1, 3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [2], frozenset([2, 3]): [2],frozenset([1, 3]): [1,3,5]}

		R = self.Cm.getTree(5)
		R_expected = set([
			
			CliqueCritique((frozenset([1,3]), (4,4),0,3,4,4)),
			CliqueCritique((frozenset([1,3]), (1,1),0,3,1,1)),
			CliqueCritique((frozenset([1,3]), (1,4),3,5,4,1)),
			CliqueCritique((frozenset([1,2]), (2,2),0,3,2,2)),
			CliqueCritique((frozenset([2,3]), (2,2),0,3,2,2)),

			CliqueCritique((frozenset([1,2,3]), (1,2),1,3,1,2)),
			CliqueCritique((frozenset([1,2,3]), (2,4),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]), (1,4),3,5,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestClique)
	unittest.TextTestRunner(verbosity=2).run(suite)
