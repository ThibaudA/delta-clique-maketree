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

nodesextensionsuccess=dict()
nodesextensionpredecess=dict()

nodescritiques=dict()
reversenodescritiques=dict()

nodescritiquespotentiel=dict()
reversenodescritiquespotentiel=dict()

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
		tlimitb=line.strip().split(" ")[4].split(",")[0]
		tlimite=line.strip().split(" ")[4].split(",")[1]
        
		u = Clique((frozenset(X),(tb,te),(tlimitb,tlimite)))
		if u in stock:
			stock.remove(u)
			read=True
		        if not u in nodessuccess:
				nodessuccess[u] = set()
				nodespredecess[u]=set()
				nodesextensionsuccess[u]=set()
				nodesextensionpredecess[u]=set()
				nodes.add(u)
		else:
			read=False
	
	    elif (line[0] == "A" and read and line.strip().split(" ")[6][0] != "f"):
	        X = line.strip().split(" ")[1].split(",") 
	        tb = line.strip().split(" ")[2].split(",")[0]
	        te = line.strip().split(" ")[2].split(",")[1]
	        tlimitb=line.strip().split(" ")[3].split(",")[0]
		tlimite=line.strip().split(" ")[3].split(",")[1]
		
		v = Clique((frozenset(X),(tb,te),(tlimitb,tlimite)))
		
		if not v in nodessuccess:
			nodessuccess[v] = set()
			nodespredecess[v]=set()
			nodesextensionsuccess[v]=set()
			nodesextensionpredecess[v]=set()
			nodes.add(v)
			stock.add(v)


		nodessuccess[u].add(v)
		nodespredecess[v].add(u)
		
	    elif (line[0] == "A" and read and line.strip().split(" ")[6][0] == "f"):
	        X = line.strip().split(" ")[1].split(",") 
	        tb = line.strip().split(" ")[2].split(",")[0]
	        te = line.strip().split(" ")[2].split(",")[1]
	        tlimitb=line.strip().split(" ")[3].split(",")[0]
		tlimite=line.strip().split(" ")[3].split(",")[1]
		
                
                v = Clique((frozenset(X),(tb,te),(tlimitb,tlimite)))
		if not v in nodessuccess:
			nodessuccess[v] = set()
			nodespredecess[v]=set()
			nodesextensionsuccess[v]=set()
			nodesextensionpredecess[v]=set()
			nodes.add(v)
			stock.add(v)


		nodesextensionsuccess[u].add(v)
		nodesextensionpredecess[v].add(u)

	    elif (line[0] == "T" and read):
		X = line.strip().split(" ")[1].split(",") 
	        tlimitb=line.strip().split(" ")[2].split(",")[0]
		tlimite=line.strip().split(" ")[2].split(",")[1]
		deltamin=line.strip().split(" ")[3]
		deltamax=line.strip().split(" ")[4]
		td=line.strip().split(" ")[5]
		tp=line.strip().split(" ")[6]

		c=CliqueCritique(((frozenset(X),(tlimitb,tlimite),deltamin,deltamax,tp,td)))
		if not c in nodescritiquespotentiel:
			nodescritiquespotentiel[c]=set()
		reversenodescritiquespotentiel[u]=c

		nodescritiquespotentiel[c].add(u)

	    elif (line[0] == "R"  and read):
		nodes.remove(u)
		X = line.strip().split(" ")[1].split(",") 
	        tlimitb=line.strip().split(" ")[2].split(",")[0]
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

	f.seek(0)
	sys.stderr.write("Iteration\n")

sys.stderr.write("Data Loaded")

for u in reversenodescritiquespotentiel:
	
	if reversenodescritiquespotentiel[u] in nodescritiques:
		nodes.remove(u)
		c=reversenodescritiquespotentiel[u]
		reversenodescritiques[u]=c
		nodescritiques[c].add(u)


for c in nodes:
	for u in nodessuccess[c]:
		nodespredecess[u].remove(c)
		for v in nodespredecess[c]:
			nodespredecess[u].add(v)
                 
                if c not in  reversenodescritiques:
		        for v in nodesextensionsuccess[c]:
			        nodesextensionsuccess[u].add(v)
				nodesextensionpredecess[v].add(u)

                if c not in  reversenodescritiques:
		        for v in nodesextensionpredecess[c]:
			        nodesextensionpredecess[u].add(v)
				nodesextensionsuccess[v].add(u)


	for u in nodespredecess[c]:
		nodessuccess[u].remove(c)
		for v in nodessuccess[c]:
			nodessuccess[u].add(v)

        if c not in reversenodescritiques: 
            for u in nodesextensionsuccess[c]:
                nodesextensionpredecess[u].remove(c)
        
            for u in nodesextensionpredecess[c]:
                nodesextensionsuccess[u].remove(c)
            


	nodessuccess.pop(c)
	nodespredecess.pop(c)
	nodesextensionsuccess.pop(c)
	nodesextensionpredecess.pop(c)

nodesconfig=dict()
for cc in nodescritiques:
	nodesconfig[cc]=set()
	for u in nodescritiques[cc]:
		for v in nodessuccess[u]:
			if not reversenodescritiques[v] == cc:
				nodesconfig[cc].add(reversenodescritiques[v])

		for v in nodesextensionsuccess[u]:
                        if not reversenodescritiques[v] == cc:

				nodesconfig[cc].add(reversenodescritiques[v])


nodes = set()
links = ""

ordinate=list()
ordinatelinks=""

ranks=dict()

deltaminmax=0

sys.stdout.write("graph G {\n")
sys.stdout.write("ranksep=equally;\n")
for u in nodesconfig:
	deltaminmax=max(int(deltaminmax),int(u._deltamin))
	if  u._deltamin not in ranks:
		ranks[u._deltamin]=set()


for i in range(deltaminmax+1):
	ordinate.append(str(i))


for i in range(deltaminmax):
	ordinatelinks+="\""+str(i) + "\" -- \"" + str(i+1)+ "\";\n"


for node in ordinate:
	if node in ranks:
    		sys.stdout.write("\"" + node + "\" [shape=ellipse];\n")
	else:

    		sys.stdout.write("\"" + node + "\" [shape=point];\n")


sys.stdout.write(ordinatelinks)


for cc in nodesconfig:
	
        u = "({" + str(tuple(cc._X)) +"}, [" + str(cc._tlimitb) + ";" + str(cc._tlimite) + "], ["+str(cc._deltamin)+ ";" + str(cc._deltamax) + "])"
	nodes.add(u + "\"")
	ranks[cc._deltamin].add(u)
	for c in nodesconfig[cc]:
        	v = "({" + str(tuple(c._X)) +"}, [" + str(c._tlimitb) + ";" + str(c._tlimite) +"], ["+str(c._deltamin)+ ";" + str(c._deltamax) + "])"
		nodes.add(v + "\"")
		ranks[c._deltamin].add(v)
        	links +=  "\"" + u + "\" -- \"" + v +"\" [color=black];\n"

for node in nodes:
    sys.stdout.write("\"" + node + " [shape=ellipse];\n")


sys.stdout.write(links)

for deltamin in ranks:
	ranklist=""
	for u in ranks[deltamin]:
		ranklist+="; \""+str(u)+"\""
	sys.stdout.write("{ rank = same; \"" + str(deltamin) + "\"" + ranklist  + "}\n")

sys.stdout.write("}\n")
