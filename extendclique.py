import sys
from CliqueCritique import CliqueCritique
from CliqueMaster import CliqueMaster
from Clique import Clique
from numpy import *
import matplotlib.pyplot as plt
import operator

delta = int(sys.argv[1])
cliques=[]
cliquesliste=[]
for line in sys.stdin:
	contents = line.split(" ")[:-1]
	#print contents
	#if int(contents[2])<=delta and delta < int(contents[3]):
	if int(contents[3]>delta):
		contents[0]=map(int,contents[0].split(","))
		contents[1]=map(int,contents[1].split(","))
		contents[2:]=map(int,contents[2:])
		cliques.append(Clique((set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1])))
		cliquesliste.append([set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1],len(set(contents[0]))])
		
print 'data loaded'
for c in cliques:
	print c
#NB de noeud par clique
histo=range(len(cliques))
for i in range(len(cliques)):
	histo[i]=len(cliques[i]._X)

cliquesnbnodesmax=sorted(cliquesliste,key=operator.itemgetter(3))[-100:]
for c in cliquesnbnodesmax:
	print c[3],c[2][1]-c[2][0]

plt.subplot(211)
valueshisto, basehisto=histogram(histo,bins=1000)
cumulativehisto=cumsum(valueshisto)
plt.plot(basehisto[:-1],cumulativehisto,c='blue')
plt.title("Nombre de Clique a n noeud")

#temps des cliques

histo=range(len(cliques))
for i in range(len(cliques)):
	histo[i]=cliques[i]._te-cliques[i]._tb
plt.subplot(212)
valueshisto, basehisto=histogram(histo,bins=1000)
cumulativehisto=cumsum(valueshisto)
plt.plot(basehisto[:-1],cumulativehisto,c='blue')

plt.title("Nombre de Clique de dure d(en seconde)")
plt.show()
