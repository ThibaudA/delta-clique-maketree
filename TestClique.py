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
                sousflot   = list([
			Clique((frozenset([1,2]),(1,1)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._times = {frozenset([1,2]):[1]}
		self.Cm._nodes = {1:set([2]), 2:set([1])}
		R = self.Cm.getSpace(10)
		self.assertEqual(R, set([CliqueCritique((frozenset([1,2]),0,10,1,1))]))

	def test_negative_delta(self):
		pass

	def test_big_delta(self):
                sousflot   = list([
			Clique((frozenset([1,2]),(1,1)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._times = {frozenset([1,2]):[1]}
		self.Cm._nodes = {1:set([2]), 2:set([1])}
		R = self.Cm.getSpace(100)
		self.assertEqual(R, set([CliqueCritique((frozenset([1,2]),0,100,1,1))]))

	def test_simple_triangle_when_delta_is_5(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([1, 3]),(2,2)),set([])),
		    Clique((frozenset([2, 3]),(3,3)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [2], frozenset([1, 2]): [1], frozenset([2, 3]): [3]}

		R = self.Cm.getSpace(5)
		R_expected = set([

			CliqueCritique((frozenset([1,2,3]),2,5,1,3)),
			CliqueCritique((frozenset([1,2]),0,5,1,1)),
			CliqueCritique((frozenset([2,3]),0,5,3,3)),
			CliqueCritique((frozenset([1,3]),0,5,2,2))
		])

		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"

		self.assertEqual(R, R_expected, debug_msg)

	def test_two_links_alterning(self):
		pass

	def test_single_link_occurring_every_delta(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([1, 2]),(3,3)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2]), 2: set([1])}
		self.Cm._times = {frozenset([1, 2]): [1, 3]}

		R = self.Cm.getSpace(5)
		R_expected = set([

			CliqueCritique((frozenset([1,2]),0,2,1,1)),
			CliqueCritique((frozenset([1,2]),0,2,3,3)),
			CliqueCritique((frozenset([1,2]),2,5,3,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_single_link_not_occurring_every_delta(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([1, 2]),(3,3)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2]), 2: set([1])}
		self.Cm._times = {frozenset([1, 2]): [1, 3]}

		R = self.Cm.getSpace(1)


		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,1,1,1)),
			CliqueCritique((frozenset([1,2]),0,1,3,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_triangle_and_many_occurrences_with_delta_too_small(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([2, 3]),(2,2)),set([])),
		    Clique((frozenset([1, 3]),(3,3)),set([])),
		    Clique((frozenset([1, 2]),(4,4)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getSpace(2)
		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,2,1,1)),
			CliqueCritique((frozenset([1,2]),0,2,4,4)),
			CliqueCritique((frozenset([1,3]),0,2,3,3)),
			CliqueCritique((frozenset([2,3]),0,2,2,2)),
			CliqueCritique((frozenset([1,2,3]),2,2,1,3)),
			CliqueCritique((frozenset([1,2,3]),2,2,2,4))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"

		self.assertEqual(R, R_expected, debug_msg)

	def test_triangle_and_many_occurrences_with_delta_big(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([2, 3]),(2,2)),set([])),
		    Clique((frozenset([1, 3]),(3,3)),set([])),
		    Clique((frozenset([1, 2]),(4,4)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getSpace(5)
		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,3,1,1)),
			CliqueCritique((frozenset([1,2]),0,3,4,4)),
			CliqueCritique((frozenset([1,2]),3,5,4,1)),

			CliqueCritique((frozenset([1,3]),0,5,3,3)),
			CliqueCritique((frozenset([2,3]),0,5,2,2)),

			CliqueCritique((frozenset([1,2,3]),2,3,1,3)),
			CliqueCritique((frozenset([1,2,3]),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]),3,5,2,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_triangle_and_many_occurrences_with_delta_huge(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1)),set([])),
		    Clique((frozenset([2, 3]),(2,2)),set([])),
		    Clique((frozenset([1, 3]),(3,3)),set([])),
		    Clique((frozenset([1, 2]),(4,4)),set([]))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [3], frozenset([1, 2]): [1, 4], frozenset([2, 3]): [2]}

		R = self.Cm.getSpace(100)
		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,3,1,1)),
			CliqueCritique((frozenset([1,2]),0,3,4,4)),
			CliqueCritique((frozenset([1,2]),3,100,4,1)),

			CliqueCritique((frozenset([1,3]),0,100,3,3)),
			CliqueCritique((frozenset([2,3]),0,100,2,2)),

			CliqueCritique((frozenset([1,2,3]),2,3,1,3)),
			CliqueCritique((frozenset([1,2,3]),2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]),3,100,2,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)



	def test_simultaneouslinks(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([2, 3]),(1,1))),
		    Clique((frozenset([1, 3]),(1,1))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [1], frozenset([1, 2]): [1], frozenset([2, 3]): [1]}

		R = self.Cm.getSpace(100)
		R_expected = set([
			CliqueCritique((frozenset([1,2,3]),0,100,1,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_simultaneouslinkswithadoublelink(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([2, 3]),(1,1))),
		    Clique((frozenset([1, 3]),(1,1))),
		    Clique((frozenset([2, 3]),(2,2)))
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2, 3]), 2: set([1, 3]), 3: set([1, 2])}
		self.Cm._times = {frozenset([1, 3]): [1], frozenset([1, 2]): [1], frozenset([2, 3]): [1,2]}

		R = self.Cm.getSpace(5)
		R_expected = set([
			CliqueCritique((frozenset([1,2,3]),0,5,1,1)),
			CliqueCritique((frozenset([2,3]),1,5,2,1)),
			CliqueCritique((frozenset([2,3]),0,1,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_extensionvsdeltamax(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([2, 3]),(2,2))),
		    Clique((frozenset([1, 2]),(3,3))),
		    Clique((frozenset([1, 2]),(6,6))),

		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2]), 2: set([1, 3]), 3: set([2])}
		self.Cm._times = {frozenset([1, 2]): [1,3,6], frozenset([2, 3]): [2]}

		R = self.Cm.getSpace(10)
		R_expected = set([

			CliqueCritique((frozenset([2,3]), 0,10,2,2)),
			CliqueCritique((frozenset([1,2]), 0,2,1,1)),
			CliqueCritique((frozenset([1,2]), 0,2,3,3)),
			CliqueCritique((frozenset([1,2]), 2,3,3,1)),
			CliqueCritique((frozenset([1,2]), 0,3,6,6)),
			CliqueCritique((frozenset([1,2]), 3,10,6,1))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)


	def test_ajoutdenoeudwhenmax(self):
                sousflot   = list([
		    Clique((frozenset([1, 3]),(1,1))),
		    Clique((frozenset([1, 2]),(2,2))),
		    Clique((frozenset([2, 3]),(2,2))),
		    Clique((frozenset([1, 3]),(4,4))),

		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2,3]), 2: set([1, 3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [2], frozenset([2, 3]): [2],frozenset([1, 3]): [1,4]}

		R = self.Cm.getSpace(5)
		R_expected = set([

			CliqueCritique((frozenset([1,3]), 0,3,4,4)),
			CliqueCritique((frozenset([1,3]), 0,3,1,1)),
			CliqueCritique((frozenset([1,3]), 3,5,4,1)),
			CliqueCritique((frozenset([1,2]), 0,3,2,2)),
			CliqueCritique((frozenset([2,3]), 0,3,2,2)),

			CliqueCritique((frozenset([1,2,3]), 1,3,1,2)),
			CliqueCritique((frozenset([1,2,3]), 2,3,2,4)),
			CliqueCritique((frozenset([1,2,3]), 3,5,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_ajoutdenoeudwhenmaxsuivitdajoutdelien(self):
                sousflot   = list([
		    Clique((frozenset([1, 3]),(1,1))),
		    Clique((frozenset([1, 2]),(2,2))),
		    Clique((frozenset([2, 3]),(2,2))),
		    Clique((frozenset([1, 3]),(3,3))),
		    Clique((frozenset([1, 3]),(5,5))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)
		self.Cm._nodes = {1: set([2,3]), 2: set([1, 3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [2], frozenset([2, 3]): [2],frozenset([1, 3]): [1,3,5]}

		R = self.Cm.getSpace(7)
		R_expected = set([

			CliqueCritique((frozenset([1,3]), 0,2,1,1)),
			CliqueCritique((frozenset([1,3]), 0,2,3,3)),
			CliqueCritique((frozenset([1,3]), 0,2,5,5)),
			CliqueCritique((frozenset([1,2]), 0,2,2,2)),
			CliqueCritique((frozenset([3,2]), 0,2,2,2)),

			CliqueCritique((frozenset([1,3]), 2,7,5,1)),


			CliqueCritique((frozenset([1,2,3]), 1,2,1,2)),
			CliqueCritique((frozenset([1,2,3]), 1,2,2,3)),
			CliqueCritique((frozenset([1,2,3]), 2,7,2,2))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)


	def test_complexexemple_passageorder(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([1, 2]),(2,2))),
		    Clique((frozenset([1, 3]),(2,2))),
		    Clique((frozenset([1, 4]),(3,3))),
		    Clique((frozenset([2, 3]),(5,5))),
		    Clique((frozenset([4, 3]),(5,5))),
		    Clique((frozenset([2, 4]),(5,5))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)

		self.Cm._nodes = {1: set([2,3,4]), 2: set([1,3,4]), 3: set([1,2,4]),4: set([1,2,3])}
		self.Cm._times = {frozenset([1, 2]): [1,2], frozenset([1, 3]): [2],frozenset([1, 4]): [3],frozenset([2, 3]): [5],frozenset([2, 4]): [5],frozenset([3, 4]): [5]}

		R = self.Cm.getSpace(10)
		R_expected = set([

			CliqueCritique((frozenset([1,2]),0,1,1,1)),
			CliqueCritique((frozenset([1,2]),0,1,2,2)),
			CliqueCritique((frozenset([2,3,4]),0,10 ,5,5)),
			CliqueCritique((frozenset([1,3]),0,10,2,2)),
			CliqueCritique((frozenset([1,4]),0,10,3,3)),
			CliqueCritique((frozenset([1,2]),1,10,2,1)),
			CliqueCritique((frozenset([1,2,3,4]),3,10,2,5))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)



	def test_varianteajoutwhenmax(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([3, 1]),(4,4))),
		    Clique((frozenset([2, 3]),(5,5))),
		    Clique((frozenset([3, 1]),(6,6))),
		    Clique((frozenset([2, 1]),(6,6))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)

		self.Cm._nodes = {1: set([2,3]), 2: set([1,3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [1,6], frozenset([1, 3]): [4,6],frozenset([2, 3]): [5]}

		R = self.Cm.getSpace(10)
		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,5,1,1)),
			CliqueCritique((frozenset([1,2]),0,5,6,6)),
			CliqueCritique((frozenset([1,3]),0,2,4,4)),
			CliqueCritique((frozenset([2,3]),0,5,5,5)),
			CliqueCritique((frozenset([1,2,3]),5,10,5,5)),
			CliqueCritique((frozenset([1,3]),0,2,6,6)),
			CliqueCritique((frozenset([1,2,3]),4,5,1,5)),
			CliqueCritique((frozenset([1,2,3]),1,5,5,6)),
			CliqueCritique((frozenset([1,2]),5,10,6,1)),
			CliqueCritique((frozenset([1,3]),2,10,6,4))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)



	def test_transfertsuccess_same_td_tp(self):
                sousflot   = list([
		    Clique((frozenset([1, 2]),(1,1))),
		    Clique((frozenset([3, 2]),(3,3))),
		    Clique((frozenset([1, 3]),(3,3))),
		    Clique((frozenset([3, 1]),(4,4))),
		    Clique((frozenset([2, 1]),(4,4))),
		    Clique((frozenset([2, 3]),(4,4))),
		    Clique((frozenset([2, 1]),(9,9))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)

		self.Cm._nodes = {1: set([2,3]), 2: set([1,3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [1,4,9], frozenset([1, 3]): [3,4],frozenset([2, 3]): [3,4]}

		R = self.Cm.getSpace(10)
		R_expected = set([
			CliqueCritique((frozenset([1,2]),0,3,1,1)),
			CliqueCritique((frozenset([2,3]),0,1,3,3)),
			CliqueCritique((frozenset([1,2,3]),3,10,4,3)),
			CliqueCritique((frozenset([1,2,3]),0,3,4,4)),
			CliqueCritique((frozenset([1,2]),0,5,9,9)),
			CliqueCritique((frozenset([1,2]),3,5,4,1)),
			CliqueCritique((frozenset([1,2]),5,10,9,1)),
			CliqueCritique((frozenset([1,3]),0,1,3,3)),
			CliqueCritique((frozenset([2,3]),1,3,4,3)),
			CliqueCritique((frozenset([1,3]),1,3,4,3)),
			CliqueCritique((frozenset([1,2,3]),2,3,1,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)

	def test_ajoutdeneouddivers(self):
                sousflot   = list([
		    Clique((frozenset([3, 2]),(1,1))),
		    Clique((frozenset([1, 2]),(2,2))),
		    Clique((frozenset([1, 3]),(3,3))),
		    Clique((frozenset([3, 2]),(3,3))),
		    Clique((frozenset([2, 1]),(5,5))),
		])
                for c in sousflot:
                    c._td,c._tp = c._tb,c._tb
                    self.Cm.addClique(c)

                self.Cm._nodes = {1: set([2,3]), 2: set([1,3]), 3: set([1,2])}
		self.Cm._times = {frozenset([1, 2]): [2,5], frozenset([1, 3]): [3],frozenset([2, 3]): [1,3]}

		R = self.Cm.getSpace(10)
		R_expected = set([
			CliqueCritique((frozenset([1,3]),0,3,3,3)),
			CliqueCritique((frozenset([2,3]),0,2,3,3)),
			CliqueCritique((frozenset([2,3]),0,2,1,1)),
			CliqueCritique((frozenset([1,2]),0,3,2,2)),
			CliqueCritique((frozenset([1,2]),0,3,5,5)),
			CliqueCritique((frozenset([1,2,3]),1,3,2,3)),
			CliqueCritique((frozenset([1,2,3]),2,3,3,5)),
			CliqueCritique((frozenset([2,3]),2,10,3,1)),
			CliqueCritique((frozenset([1,2]),3,10,5,2)),
			CliqueCritique((frozenset([1,2,3]),3,10,3,3))
		])
		debug_msg = "\nGot :\n" + str(self.Cm)
		debug_msg += "\nExpected :\n"
		for c in R_expected:
			debug_msg += str(c) + "\n"
		self.assertEqual(R, R_expected, debug_msg)



if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestClique)
	unittest.TextTestRunner(verbosity=2).run(suite)
