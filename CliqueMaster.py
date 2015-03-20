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
                self._S_nodeadd=deque()
		self._interdeque=deque()
		self._nodeinterdeque=deque()
		self._R = set()
		self._times = dict()
		self._nodes = dict()

	def addClique(self, c):
		""" Adds a clique to S, checking beforehand that this clique is not already present in S. """
		if not c in self._S_set:
			#self._S.appendleft(c)
                        self._S.append(c)
			self._S_set.add(c)


	def addCliquenodeadd(self, c):
		""" Adds a clique to S, checking beforehand that this clique is not already present in S. """
		if not c in self._S_set:
			self._S_nodeadd.appendleft(c)
                        #self._S_nodeadd.append(c)
			self._S_set.add(c)



	def halfMemory(self):
		#Memory saver
		length=len(self._S_set)
		while len(self._S_set) > length/2:
			trash=self._S_set.pop()
	


	def getClique(self):
		c = self._S.pop()
		sys.stderr.write("\nGetting clique " + str(c) + "\n")
		return c


	def getCliquefromnode(self):
		c = self._S_nodeadd.pop()
		sys.stderr.write("\nGetting clique " + str(c) + "\n")
		return c

	def getTree(self, delta):
		""" Returns a set of maximal cliques. """
		token=0
		while len(self._S) != 0 or len(self._S_nodeadd) != 0:
                        token+=1
			if token==10000:
				#if len(self._S_set)>700000:  #reduce the memory use
					#self.halfMemory()
					#sys.stderr.write("Cleaning _S_set \n")
				sys.stderr.write("S:"+ str(len(self._S)) + "\n") #show advancement
				token=0
                        if len(self._S)!=0:
			    c = self.getClique()
                        else:
                            c=self.getCliquefromnode()
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
						
					    sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")	
				            self.addClique(c_add)  #ATTENTION peut etre necessaire de differencier si pas de changement de deltamin
					else:
 				            #if different clique we dont want to change deltamax/min
					    c_add = Clique((c._X, (c._tb, new_t),(c._tlimitb,c._tlimite)),c._candidates)
                                            c_add._deltamin=c._deltamin
					    time_extension=new_t-td

					    sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
					    self._interdeque.append(c_add)
				else:
					c_add = Clique((c._X, (c._tb, td + delta),(c._tlimitb,c._tlimite)),c._candidates)
					c_add._deltamin=c._deltamin
					self._interdeque.append(c_add)
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
							if tp-new_t<=time_extension: 
								c._deltamax=tp-new_t
							else:
								#sinon
				                        	c_wannabe=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,time_extension,td,tp))
								sys.stderr.write("Trying " + str(c_wannabe) + " but time extension\n")
						else: c._deltamax=tp-new_t
					    	
                                        	self.addClique(c_add)
						sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
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
							c_wannabe=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,tp-new_t,td,tp))
							sys.stderr.write("Trying " + str(c_wannabe) + " but time extension\n")

						self._interdeque.append(c_add)
						sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
				else:
					c_add = Clique((c._X, (tp - delta, c._te),(c._tlimitb,c._tlimite)),c._candidates)
					c_add._deltamin=c._deltamin
					self._interdeque.append(c_add)
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
				isclique,first,last,maxinterval=c.isClique(self._times,node,delta)
				#first: list of first link for each couple of node (excluding "node") 
				#last: idem
				#maxinterval: maximum interval between 2 link (same nodes)
				if isclique:
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te),(min(c._tlimitb,min(first)),max(c._tlimite,max(last)))),c._candidates) #determination of limitb/e
					#deltamin determination, maybe the use of last and first is useless here
					
					c_add._deltamin=max(c._deltamin,maxinterval,c_add._tlimite-min(last),max(first)-c_add._tlimitb,c_add._tlimite-td,tp-c_add._tlimitb)
					
		
					sys.stderr.write("Adding " + str(c_add) + " from "+ str(c) +" (node extension)\n")


					#if c._deltamax is not None:
                                        #            if c._deltamax>c._deltamin:
				        #                c_wannabe=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,c._deltamax,td,tp))
					#                sys.stderr.write("Trying " + str(c_wannabe) + " but node extension\n")
					#	    c._deltamax=None
                                      	if (tp,td)==(max(first),min(last)): #Attention a l'ordre 
						if c._min_deltamin_success is not None:
							c._min_deltamin_success=min(c_add._deltamin,c._min_deltamin_success)
						else:
							c._min_deltamin_success=c_add._deltamin

                                                print c._min_deltamin_success

					#if is_max == True :
					if c._deltamax is not None:
						if c._min_deltamin_success is not None:
							c._deltamax=min(c._min_deltamin_success,c._deltamax)
					else:
						c._deltamax=c._min_deltamin_success
			            	

					self._nodeinterdeque.append(c_add)
					
					is_max = False
			
			#Possibilité de manipulation du parcours de l'arbre

			for c_add in self._interdeque:
				c_add._min_deltamin_success=c._min_deltamin_success
                                self.addClique(c_add)
			self._interdeque=deque()
			

			for c_add in self._nodeinterdeque:
				self.addCliquenodeadd(c_add)
			self._nodeinterdeque=deque()
			

			if c._deltamax is not None:
				if c._deltamax>c._deltamin:
					c_add=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,c._deltamax,td,tp))
					self._R.add(c_add)
					sys.stderr.write("Return " + str(c_add) + "\n")
				else:
					c_add=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,c._deltamax,td,tp))
					sys.stderr.write("Trying " + str(c_add) + " but deltamin = deltamax\n")

			if is_max : #deltamax=delta + add c to R
				sys.stderr.write(str(c) + " is maximal\n")
				c_add=CliqueCritique((c._X,(c._tlimitb,c._tlimite),c._deltamin,delta,td,tp))
				self._R.add(c_add)
				sys.stderr.write("Return " + str(c_add) + "\n")

				
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




