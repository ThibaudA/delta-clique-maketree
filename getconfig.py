from CliqueMaster import CliqueMaster
from Clique import Clique
from CliqueCritique import CliqueCritique
from numpy import *
from itertools import combinations
from collections import deque
import matplotlib.pyplot as plt
import operator
import sys
nodes=set()
nodessuccess = dict()
nodespredecess= dict()
nodescritiques=dict()
reversenodescritiques=dict()
read=False
stock=set()
f=open(sys.argv[1])
stock.add(Clique((frozenset(sys.argv[2].strip().split(",")),(sys.argv[3].strip().split(",")[0],sys.argv[3].strip().split(",")[1]),(sys.argv[4].strip().split(",")[0],sys.argv[4].strip().split(",")[1]))))

while len(stock)!=0:
	for line in f:
	    if line[0] == "G":
	        X = line.strip().split(" ")[2].split(",")
	        tb = line.strip().split(" ")[3].split(",")[0]
	        te = line.strip().split(" ")[3].split(",")[1]
		tlimitb=line.strip().split(" ")[4].split(",")[1]
		tlimite=line.strip().split(" ")[4].split(",")[1]
        
		u = Clique((frozenset(X),(tb,te),(tlimitb,tlimite)))
		if u in stock:
			stock.remove(u)
			read=True
		        if not u in nodessuccess:
				nodessuccess[u] = set()
				nodespredecess[u]=set()
				nodes.add(u)
		else:
			read=False
	
	    elif (line[0] == "A" and read):
	        X = line.strip().split(" ")[1].split(",") 
	        tb = line.strip().split(" ")[2].split(",")[0]
	        te = line.strip().split(" ")[2].split(",")[1]
	        tlimitb=line.strip().split(" ")[3].split(",")[1]
		tlimite=line.strip().split(" ")[3].split(",")[1]
		
		v = Clique((frozenset(X),(tb,te),(tlimitb,tlimite)))
		
		if not v in nodessuccess:
			nodessuccess[v] = set()
			nodespredecess[v]=set()
			nodes.add(v)
			stock.add(v)


		nodessuccess[u].add(v)
		nodespredecess[v].add(u)
		

	    elif (line[0] == "R" and read):
		nodes.remove(u)
	 #       print u
		X = line.strip().split(" ")[1].split(",") 
	        tlimitb=line.strip().split(" ")[2].split(",")[1]
		tlimite=line.strip().split(" ")[2].split(",")[1]
		deltamin=line.strip().split(" ")[3]
		deltamax=line.strip().split(" ")[4]
		td=line.strip().split(" ")[5]
		tp=line.strip().split(" ")[6]

		c=CliqueCritique(((frozenset(X),(tlimitb,tlimite),deltamin,deltamax,tp,td)))
		if not c in nodescritiques:
			nodescritiques[c]=set()
		reversenodescritiques[u]=c

		nodescritiques[c].add(u)


	#print map(str,stock)
	f.seek(0)




for c in nodes:
	for u in nodessuccess[c]:
		nodespredecess[u].remove(c)
		for v in nodespredecess[c]:
			nodespredecess[u].add(v)

	for u in nodespredecess[c]:
		nodessuccess[u].remove(c)
		for v in nodessuccess[c]:
			nodessuccess[u].add(v)
	nodessuccess.pop(c)
	nodespredecess.pop(c)

nodesconfig=dict()

for cc in nodescritiques:
	nodesconfig[cc]=set()
	for u in nodescritiques[cc]:
		for v in nodessuccess[u]:
			nodesconfig[cc].add(reversenodescritiques[v]) 
	#	for v in nodespredecess[u]:
	#		nodesconfig[cc].add(reversenodescritiques[v])		
nodes = set()
links = ""

sys.stdout.write("graph G {\n")


for cc in nodesconfig:
	
        u = "({" + str(tuple(cc._X)) +"}, [" + str(cc._tlimitb) + ";" + str(cc._tlimite) + "])"
	nodes.add(u)
	for c in nodesconfig[cc]:
        	v = "({" + str(tuple(c._X)) +"}, [" + str(c._tlimitb) + ";" + str(c._tlimite) + "])"
		nodes.add(v)	
        	links +=  "\"" + u + "\" -- \"" + v +"\" [color=green];\n"

for node in nodes:
    sys.stdout.write("\"" + node + "\" [shape=ellipse];\n")

sys.stdout.write(links)

sys.stdout.write("}\n")
