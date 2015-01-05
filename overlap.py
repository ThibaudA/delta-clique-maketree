from CliqueMaster import CliqueMaster
from Clique import Clique 
from numpy import *
from itertools import combinations
import matplotlib.pyplot as plt
import operator
import sys

sys.stderr.write('Node tb,te tlimitb,tlimite\n')
delta = int(sys.argv[1])
overlap = int(sys.argv[2])/100.
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
		
print 'data loaded'

for i in combinations(range(len(cliquesliste)),2):
    c=cliquesliste[i[0]]
    d=cliquesliste[i[1]]
    if c!=d and c[1][0]<d[1][1] and c[1][1]>d[1][0]:
        inter=c[0].intersection(d[0])
        timeoverlap=min(c[1][1],d[1][1])-max(c[1][0],d[1][0])
        percent=timeoverlap/float(c[4])*len(inter)/float(len(c[0]))*len(inter)/float(len(d[0]))*timeoverlap/float(d[4])
                
        if percent>=overlap:
		print c
		print d
                print percent
                    

