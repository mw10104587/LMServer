from igraph import *


# path = [(0, 0), (3,5), (320,568)]
def create_user_graph(path):
    
	g = Graph()
    g.add_vertices(len(path))
    
	for i in range(0, len(path)-1):
        v = g.vs[i]
		v["checked"] = False
		v["nid"] = str(nodes.index(node))
		v["lat"] = node.lat
		v["lng"] = node.lng

    for node in nodes:
        v = g.vs[nodes.index(node)]
        v["checked"] = False
		v["nid"] = str(nodes.index(node))
		v["lat"] = node.lat
		v["lng"] = node.lng
		
    for i, edge in enumerate(edges):
        v1 = g.vs[nodes.index(edge.node1)]
        v2 = g.vs[nodes.index(edge.node2)]
        g.add_edges(v1,v2)
        g.es[i]["n"] = {v1["nid"]:edge.bearing1, v2["nid"]:edge.bearing2}
        g.es[i]["length"] = edge.length
		g.es[i]["n1"] = v1["nid"]
		g.es[i]["n2"] = v2["nid"]
		g.es[i]["bearing1"] = edge.bearing1
		g.es[i]["bearing2"] = edge.bearing2       
        g.es[i]["checked"] = False


    return g
