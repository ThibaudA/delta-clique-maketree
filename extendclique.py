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
	#if int(contents[2])<=delta and delta < int(contents[3]):
	if int(contents[3])>delta:
		contents[0]=map(int,contents[0].split(","))
		contents[1]=map(int,contents[1].split(","))
		contents[2:]=map(int,contents[2:])
                print contents
		cliques.append(Clique((set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1])))
		cliquesliste.append([set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1],len(set(contents[0])),contents[5]+delta-(contents[4]-delta)])
		
print 'data loaded'
groscliques=findgroscliques(cliquesliste,4,10)
for c in groscliques:
    print c


#NB de noeud par clique
histo=range(len(cliques))
for i in range(len(cliques)):
	histo[i]=len(cliques[i]._X)

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





    
