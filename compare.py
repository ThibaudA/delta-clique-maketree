import sys
from CliqueCritique import CliqueCritique
from CliqueMaster import CliqueMaster
from Clique import Clique 
from numpy import *
import matplotlib.pyplot as plt
import operator

def findgroscliques(cliquesliste,nbnoeud,nbcliques):
    #plus gros cliques a 3 noeuds:
    groscliques=[]
    for c in cliquesliste:
        if c[3]==nbnoeud:
            groscliques.append(c)
    groscliques=sorted(groscliques,key=operator.itemgetter(4))[-nbcliques:]
    return groscliques

delta = int(sys.argv[1])
cliques=[]
cliquesliste=[]
for line in sys.stdin:
	contents = line.split(" ")[:-1]
	#print contents
	if int(contents[2])<=delta and delta < int(contents[3]):
	#if int(contents[3])>delta:
		contents[0]=map(int,contents[0].split(","))
		contents[1]=map(int,contents[1].split(","))
		contents[2:]=map(int,contents[2:])
                #print contents
		cliques.append(Clique((set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1])))
		cliquesliste.append([set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1],len(set(contents[0])),contents[5]+delta-(contents[4]-delta)])

for c in cliques:
	sys.stdout.write(','.join(map(str, list(c._X)))  + " " + str(c._tb) + "," + str(c._te)  +  " \n")


    
