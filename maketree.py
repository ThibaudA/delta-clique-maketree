from CliqueMaster import CliqueMaster
from Clique import Clique
from CliqueCritique import CliqueCritique
import networkx as nx
from networkx.algorithms import bipartite
import sys
import bisect
from collections import deque


Cm = CliqueMaster()
times = dict()
nodes = dict()
delta = int(sys.argv[1]) 
nb_lines = 0

def bipartite(nodes):
    nodes_set=set()
    nodesbot=set()
    nodestop=set()
    stock=deque()
    for u in nodes:
        nodes_set.add(u)
    while len(nodes_set) != 0:
        if len(stock)==0:
            stock.append(nodes_set.pop())
            u=stock.pop()
            nodestop.add(u)
            #stock.extend(nodes[u])
            #nodes_set.discard(nodes[u])
        else:
            u=stock.pop()
        if nodes[u] is not None:
            if u in nodestop:
                if nodes[u].difference(nodesbot) is not None: 
                    stock.extend(nodes[u].difference(nodesbot))
                nodesbot.update(nodes[u])
            else:
                if nodes[u].difference(nodestop) is not None: 
                    stock.extend(nodes[u].difference(nodestop))
                nodestop.update(nodes[u])
            nodes_set.difference_update(nodes[u])


    print nodestop
    print nodesbot

    return nodestop,nodesbot

B = nx.Graph()
for line in sys.stdin:
	contents = line.split(" ")
	t = int(contents[0])
	u = int(contents[1])
	v = int(contents[2])

	
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
#print  list(nx.bfs_edges(B,'77.35.196.73'))

#bottom_nodes, top_nodes = bipartite.sets(B)
#print bottom_nodes 
#print top_nodes
Cm._times = times
Cm._nodes = nodes

Cm._nodestop,Cm._nodesbot=bipartite(nodes)


sys.stderr.write("Processed " + str(nb_lines) + " from stdin\n")
R = Cm.getTree(delta)
Cm.printCliques()
print 'end'


      















