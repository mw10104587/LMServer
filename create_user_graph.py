from igraph import *
import math


 
def create_user_graph(path):
    #path = [(0, 0), (3,5), (320,568)]   

    g = Graph()
    g.add_vertices(len(path))
    
    for i in range(0, len(path)):
        v = g.vs[i]
        v["checked"] = False
        v["nid"] = str(v.index)
        v["lat"] = path[i][1]
        v["lng"] = path[i][0]
    
    edge_length = 0
    if path[0] == path[len(path)-1]:
        edge_length = len(path)-1
    else:
        edge_length = len(path)

    for i in range(0, edge_length-1):
        v1 = g.vs[i]
        v2 = g.vs[i+1]
        g.add_edges((v1.index,v2.index))
        (bearing1, bearing2) = bearing(v1, v2)		
        g.es[i]["n"] = {v1["nid"]:bearing1, v2["nid"]:bearing2}
        length = math.hypot(v1["lng"]-v2["lng"], v1["lat"]-v2["lat"])
        g.es[i]["length"] = length
        g.es[i]["n1"] = v1["nid"]
        g.es[i]["n2"] = v2["nid"]
        g.es[i]["bearing1"] = bearing1
        g.es[i]["bearing2"] = bearing2       
        g.es[i]["checked"] = False

    if path[0] == path[len(path)-1]:
        v1 = g.vs[edge_length-1]
        v2 = g.vs[0]
        g.add_edges((v1.index,v2.index))
        (bearing1, bearing2) = bearing(v1, v2)		
        g.es[edge_length-1]["n"] = {v1["nid"]:bearing1, v2["nid"]:bearing2}
        length = math.hypot(v1["lng"]-v2["lng"], v1["lat"]-v2["lat"])
        g.es[edge_length-1]["length"] = length
        g.es[edge_length-1]["n1"] = v1["nid"]
        g.es[edge_length-1]["n2"] = v2["nid"]
        g.es[edge_length-1]["bearing1"] = bearing1
        g.es[edge_length-1]["bearing2"] = bearing2       
        g.es[edge_length-1]["checked"] = False        
		
        print g
    return g
	
	

def bearing(v1, v2):
    y = abs(v1["lng"]-v2["lng"])
    x = abs(v1["lat"]-v2["lat"])
    theta1 = math.degrees(math.atan2(y,x))
    theta2 = -90 + theta1
    return (theta1, theta2)

	

path = [(0,0), (3,5), (5,6), (320,568), (0,0)] 
create_user_graph(path)	
