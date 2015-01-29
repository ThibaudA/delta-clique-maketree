from CliqueMaster import CliqueMaster
from Clique import Clique
from CliqueCritique import CliqueCritique
import networkx as nx
from networkx.algorithms import bipartite
import sys
import bisect
Cm = CliqueMaster()
times = dict()
nodes = dict()
delta = int(sys.argv[1]) 
nb_lines = 0

B = nx.Graph()
for line in sys.stdin:
	contents = line.split(" ")
	t = int(contents[0])
	u = contents[1]
	v = contents[2]

	
	link = frozenset([u,v])
	time = (t,t)
	Cm.addClique(Clique((link,(t,t),(t,t)),set([])))
	
	B.add_nodes_from([u,v])
	B.add_edges_from([(u,v)])

	# Populate data structures
	if not times.has_key(link):
		times[link] = []
	times[link].append(t)

        if not u in nodes:
		nodes[u] = set()

	if not v in nodes:
		nodes[v] = set()

	nodes[u].add(v)
        nodes[v].add(u)
	nb_lines = nb_lines + 1

#print B.nodes()
print  list(nx.bfs_edges(B,'77.35.196.73'))
#bottom_nodes, top_nodes = bipartite.sets(B)
#print bottom_nodes 
#print top_nodes
Cm._times = times
Cm._nodes = nodes
sys.stderr.write("Processed " + str(nb_lines) + " from stdin\n")
#R = Cm.getTree(delta)
#Cm.printCliques()
print 'end'


