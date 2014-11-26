import sys
from CliqueCritique import CliqueCritique
from CliqueMaster import CliqueMaster
from Clique import Clique

delta = int(sys.argv[1])
cliques=[]
for line in sys.stdin:
	contents = line.split(" ")[:-1]
	#print contents
	if int(contents[2])<=delta and delta < int(contents[3]):
		contents[0]=map(int,contents[0].split(","))
		contents[1]=map(int,contents[1].split(","))
		contents[2:]=map(int,contents[2:])
		cliques.append(Clique((set(contents[0]),(contents[4]-delta,contents[5]+delta),contents[1])))

for c in cliques:
	print c
