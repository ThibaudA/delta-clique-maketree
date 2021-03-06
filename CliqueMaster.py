#-*-coding:utf8*-

import sys
import operator
from collections import deque
from Clique import Clique
from CliqueCritique import CliqueCritique

class CliqueMaster:

	def __init__(self):
		# 2 contenants pour socker les cliques: après ajout de temps (_S) ou aprés ajout de noeud (_S_nodeadd)
		#interdeque et nodeinterdeque: permet de gerer les informations provenant de la tentative d'ajout de noeud
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
		#Commentaire: Potentielle solution (check de toute la liste à chaque ajout). Couteux.
		if not c in self._S_set:
			#self._S.insert(0,c)
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




	def getSpace(self, delta):
		""" Returns a set of maximal cliques. """
		token=0
		while len(self._S) != 0 or len(self._S_nodeadd) != 0:
			token+=1
			if token==1:
				#if len(self._S_set)>700000:  #reduce the memory use
					#self.halfMemory()
					#sys.stderr.write("Cleaning _S_set \n")
				sys.stderr.write("\nS:"+ str(len(self._S)) + "\n") #show advancement
				sys.stderr.write("S:node "+ str(len(self._S_nodeadd)) + "\n") #show advancement
				token=0

			#On pioche
			c = self.getClique()

			is_max = True
			time_extension=None

			# Grow time on the right side
			if c._te != c._td + delta:
				#sameclique if the new link is in the clique
				new_t,sameclique = c.getFirstTInInterval(self._times, self._nodes, c._td, delta)
				if new_t is not None:
					if sameclique: #addclique
						c_add = Clique((c._X, (c._tb, new_t)),c._candidates)
						c_add._td=c_add.getTd(self._times,delta)
						c_add._tp=c._tp

						if c_add._td != c._td:
							c_add._deltamin=max(c._deltamin,new_t-c._td)
							#On prépare l'ajout de c au set de cliquescritiques.
							c._deltamax=c_add._deltamin
							sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
							self._interdeque.append(c_add)  #Ajout dans la file si td ne bouge pas on fait suivre les info des successeurs.
						else :
							time_extension=new_t-c._td
							c_add._deltamin=c._deltamin
							sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
							self._interdeque.append(c_add)
					else:
				        #if different clique we dont want to change deltamax/min
						c_add = Clique((c._X, (c._tb, new_t)),c._candidates)
						c_add._deltamin=c._deltamin
						c_add._td=c._td
						c_add._tp=c._tp
						time_extension=new_t-c._td
						#Important: Possible conflit entre les extensions (droite/gauche)
						sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
						self._interdeque.append(c_add)
				else:
					c_add = Clique((c._X, (c._tb, c._td + delta)),c._candidates)
					c_add._td=c._td
					c_add._tp=c._tp
					c_add._deltamin=c._deltamin
					self._interdeque.append(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the right side\n")

			# Grow time on the left side
			if c._tb != c._tp - delta:
				new_t,sameclique = c.getLastTInInterval(self._times, self._nodes, c._tp, delta)
				#sameclique if the new link is in the clique
				if new_t is not None:
					if sameclique:
						c_add = Clique((c._X, (new_t , c._te)),c._candidates)
						c_add._td=  c._td
						c_add._tp = c_add.getTp(self._times, delta)
						if c._tp != c_add._tp:
							c_add._deltamin=max(c._deltamin,c._tp-new_t) #Change deltamin if needed

							#Comparaison droite/gauche
							if c._deltamax is not None:
								c._deltamax=min(c._deltamax,c._tp-new_t)
							else:
								c._deltamax=c._tp-new_t
							sys.stderr.write("Adding " + str(c_add) + " (time extension)\n")
							self._interdeque.append(c_add)  #Ajout dans la file si tp ne bouge pas on fait suivre les info des successeurs.
						else:
							c_add._deltamin=c._deltamin
							if time_extension is None:
								time_extension=c._tp-new_t
							else:
								time_extension=min(c._tp-new_t,time_extension)
							self._interdeque.append(c_add)
							sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
					else:
						#if different clique we dont want to change deltamax/min
						c_add = Clique((c._X, (new_t , c._te)),c._candidates)
						c_add._deltamin=c._deltamin
						c_add._td=c._td
						c_add._tp=c._tp
						#équivalent de time_extension
						if time_extension is None:
							time_extension=c._tp-new_t
						else:
							time_extension=min(c._tp-new_t,time_extension)
						if c._tp-new_t<c._deltamax:
							c._deltamax = None
							c_wannabe=CliqueCritique((c._X,c._deltamin,c._tp-new_t,c._td,c._tp))
							sys.stderr.write("Trying " + str(c_wannabe) + " but time extension\n")
						self._interdeque.append(c_add)
						sys.stderr.write("Adding " + str(c_add) + " (left time extension)\n")
				else:
					c_add = Clique((c._X, (c._tp - delta, c._te)),c._candidates)
					c_add._deltamin=c._deltamin
					c_add._td=c._td
					c_add._tp=c._tp
					self._interdeque.append(c_add)
					sys.stderr.write("Adding " + str(c_add) + " (left time delta extension)\n")
				is_max = False
			else:
				sys.stderr.write(str(c) + " cannot grow on the left side\n")

			# Grow node set
			candidates = c.getAdjacentNodes(self._times, self._nodes, delta)
			min_deltamin_success = None
			sys.stderr.write("    Candidates : %s.\n" % (str(candidates)))
			for node in candidates:
				isclique,first,last,maxinterval=c.isClique(self._times,node,delta)
				#first: list of first link for each couple of node (excluding "node")
				#last: idem
				#maxinterval: maximum interval between 2 link (same nodes)
				if isclique:
					Xnew = set(c._X).union([node])
					c_add = Clique((frozenset(Xnew), (c._tb, c._te)),c._candidates)
					c_add._tp = max(max(first),c._tp)
					c_add._td = min(c._td,min(last))
					c_add._deltamin=c_add.getDeltaMin(self._times)
					is_max = False

					#L'ajout de noeud n'as d'inflence sur le calcul de deltamax que lorsque les tp et td
					#des deux cliques sont identiques
					if (c._tp,c._td)==(c_add._tp,c_add._td): #Attention a l'ordre
						if c._deltamax is not None:
							c._deltamax=min(c_add._deltamin,c._deltamax)
						else:
							c._deltamax=c_add._deltamin

						#étrange je pense que time_extension est important la aussi


					self._nodeinterdeque.append(c_add)
					sys.stderr.write("Adding " + str(c_add) + " from "+ str(c) +" (node extension)\n")


			#Possibilité de manipulation du parcours de l'arbre
			for c_add in self._interdeque:
				self.addClique(c_add)
			self._interdeque=deque()

			for c_add in self._nodeinterdeque:
				self.addClique(c_add)
			self._nodeinterdeque=deque()

			if c._deltamax is not None:
				if time_extension is not None:
					if time_extension < c._deltamax:
						c._deltamax = None



			if c._deltamax is not None:
				if c._deltamax>c._deltamin:
					c_add=CliqueCritique((c._X,c._deltamin,c._deltamax,c._td,c._tp))
					self._R.add(c_add)
					sys.stderr.write("Return " + str(c_add) + "\n")
				else:
					c_add=CliqueCritique((c._X,c._deltamin,c._deltamax,c._td,c._tp))
					sys.stderr.write("Trying " + str(c_add) + " but deltamin = deltamax\n")

			if is_max : #deltamax=delta + add c to R
				sys.stderr.write(str(c) + " is maximal\n")
				c_add=CliqueCritique((c._X,c._deltamin,delta,c._td,c._tp))
				self._R.add(c_add) #ajout au set de retour
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
