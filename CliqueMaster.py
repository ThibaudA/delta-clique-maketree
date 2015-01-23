#-*-coding:utf8*-

import sys
import operator
from collections import deque
from Clique import Clique
from CliqueCritique import CliqueCritique

class CliqueMaster:
	
	def __init__(self):
		self._S = deque()
		self._S_set = set()
		self._R = set()
		self._times = dict()
		self._nodestop = dict()
		self._nodesbot = dict()

	def addClique(self, c):
		""" Adds a clique to S, checking beforehand that this clique is not already present in S. """
		if not c in self._S_set:
			#self._S.appendleft(c)
                        self._S.append(c)
			self._S_set.add(c)


	def halfMemory(self):
		#Memory saver
		length=len(self._S_set)
		while len(self._S_set) > length/2:
			trash=self._S_set.pop()
	


	def getClique(self):
		c = self._S.pop()
		sys.stderr.write("Getting clique " + str(c) + "\n")
		return c

	def getTree(self, delta):
		""" Returns a set of maximal cliques. """
		token=0
		while len(self._S) != 0:
                        token+=1
			if token==10000:
				if len(self._S_set)>700000:  #reduce the memory use
					self.halfMemory()
					sys.stderr.write("Cleaning _S_set \n")
				sys.stderr.write("S:"+ str(len(self._S)) + "\n") #show advancement
				token=0

			c = self.getClique()
			is_max = True 
			time_extension=None
			# Grow time on the right side
			td = c.getTd(self._times, delta)
			if c._te != td + delta:
				#sameclique if the new link is in the clique
				new_t,sameclique = c.getFirstTInInterval(self._times, self._nodes, td, delta)
				if new_t is not None:
                                        if sameclique: #addclique
				            c_add = Clique((c._X, (c._tb, new_t),(c._tlimitb,new_t)),c._candidates)
                                            if new_t-td>c._deltamin: 
						    c_add._deltamin=new_t-td #Change deltamin if needed
                                            else: c_add._deltamin=c._deltamin
					
                                            if c._deltamax is not None:
                                                c._deltamax=min(c._deltamax,new_t-td)
					    else: c._deltamax=new_t-td

					else:
 				            #if different clique we dont want to change deltamax/min
					    c_add = Clique((c._X, (c._tb, new_t),(c._tlimitb,c._tlimite)),c._candidates)
                                            c_add._deltamin=c._deltamin
					    time_extension=new_t-td

					sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					self.addClique(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta),(c._tlimitb,c._tlimite)),c._candidates)
					c_add._deltamin=c._deltamin
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side 
			tp = c.getTp(self._times, delta)
			if c._tb != tp - delta:
				new_t,sameclique = c.getLastTInInterval(self._times, self._nodes, tp, delta)

				#sameclique if the new link is in the clique
				if new_t is not None:
                                        if sameclique:
				        	c_add = Clique((c._X, (new_t , c._te),(new_t,c._tlimite)),c._candidates)
                                                if tp-new_t>c._deltamin: 
							c_add._deltamin=tp-new_t #Change deltamin if needed
                                                else: c_add._deltamin=c._deltamin
                                        	
						if c._deltamax is not None:
							c._deltamax=min(c._deltamax,tp-new_t)
						elif time_extension is not None:
							if tp-new_t<=time_extension: c._deltamax=tp-new_t
						else: c._deltamax=tp-new_t
					    	
					else:	
 				            	#if different clique we dont want to change deltamax/min
                                                c_add = Clique((c._X, (new_t , c._te),(c._tlimitb,c._tlimite)),c._candidates)       
						c_add._deltamin=c._deltamin
						if time_extension is not None:
							if tp-new_t<time_extension:
								time_extension=tp-new_t
						else: time_extension=tp-new_t
						
						if tp-new_t<c._deltamax:
							c._deltamax = None


                                        self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te),(c._tlimitb,c._tlimite)),c._candidates)
					c_add._deltamin=c._deltamin
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

			for node in candidates:
				#if c._deltamax is not None:
                                #	isclique,first,last,maxinterval=c.isClique(self._times,node,min(delta,c._deltamax)) 
				#else:
				if node in self._nodestop:
					innodestop=True
				else:
					innodestop=False
				isclique,first,last,maxinterval=c.isClique(self._times,node,delta,self._nodestop if  node not in self._nodestop else self._nodesbot)
				#first: list of first link for each couple of node (excluding "node") 
				#last: idem
				#maxinterval: maximum interval between 2 link (same nodes)
				if isclique:
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te),(min(c._tlimitb,min(first)),max(c._tlimite,max(last)))),c._candidates) #determination of limitb/e
					#deltamin determination, maybe the use of last and first is useless here
					
					c_add._deltamin=max(c._deltamin,maxinterval,c_add._tlimite-min(last),max(first)-c_add._tlimitb,c_add._tlimite-td,tp-c_add._tlimitb)
					
					#if time_extension is not None :
					#	if c._deltamax is not None:
					#		if c_add._deltamin<=time_extension:
					#			c._deltamax=min(c_add._deltamin,c._deltamax)
					#	elif c_add._deltamin<=time_extension:
					#		c._deltamax=c_add._deltamin
					#
					#elif c._deltamax is not None:
					#	c._deltamax=min(c_add._deltamin,c._deltamax)
					#else:
					#	c._deltamax=c_add._deltamin

					if c._deltamax is not None:
						#if c._deltamax>=c_add._deltamin:
						c._deltamax=None



					sys.stderr.write("adding " + str(c_add) + " from "+ str(c) +" (node extension)\n")
					
                                        self.addClique(c_add)
					
					is_max = False
			

			if c._deltamax is not None and c._deltamax>c._deltamin:
				c_add=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,c._deltamax,td,tp))
				self._R.add(c_add)
				sys.stderr.write("adding " + str(c_add) + " to Return\n")

			if is_max: #deltamax=delta + add c to R
				sys.stderr.write(str(c) + " is maximal\n")
				c_add=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,delta,td,tp))
				self._R.add(c_add)
				sys.stderr.write("adding " + str(c_add) + " to Return\n")

				
		return self._R



	def getDeltaCliques(self, delta): #old function (see delta-cliques)
		""" Returns a set of maximal cliques. """

		while len(self._S) != 0:
                        sys.stderr.write("S:"+ str(len(self._S)) + "\n")
			c = self.getClique()
			is_max = True

			# Grow time on the right side
			td = c.getTd(self._times, delta)
			if c._te != td + delta:
				new_t = c.getFirstTInInterval(self._times, self._nodes, td, delta)
				if new_t is not None:
					c_add = Clique((c._X, (c._tb, new_t)))
					sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					self.addClique(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side 
			tp = c.getTp(self._times, delta)
			if c._tb != tp - delta:
				new_t = c.getLastTInInterval(self._times, self._nodes, tp, delta)
				if new_t is not None:
					c_add = Clique((c._X, (new_t , c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + "(left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			#else:
				#sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			#sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))

			for node in candidates:
				if c.isClique(self._times, node, delta):
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te)))
					self.addClique(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (node extension)\n")
					is_max = False

			if is_max:
				#sys.stderr.write(str(c) + " is maximal\n")
				self._R.add(c)
		return self._R
	



	def printCliques(self):
		out=sorted(list(self._R),key=operator.attrgetter('_deltamin'))
		for c in out:
			sys.stdout.write(str(c) + " \n")

	def __str__(self):
		msg = ""
		for c in self._R:
			msg += str(c) + "\n"
		return msg




