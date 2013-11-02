import ParsePy
from igraph import *

def initParse():
    ParsePy.APPLICATION_ID = "9viWGl0x5YuJqhwg8dbYG16snlA2WG5X26JJrI7d"
    ParsePy.MASTER_KEY = "WWEZS3H9LCadSHLhwBPIbVk3nDEjeBAhEMGWDIJr"
    
def fetchGraph():
    
    g = Graph()

    print "Start Downloading"

    query = ParsePy.ParseQuery("Node")
    nodes = query.fetch()
    query = ParsePy.ParseQuery("Edge")
    edges = query.fetch()

    print "Download Complete"
    
    g.add_vertices(len(nodes))

    for node in nodes:
        v = g.vs[nodes.index(node)]
        v["checked"] = False
        v["nid"] = str(nodes.index(node))
        v["objectId"] = node.objectId()
        v["lat"] = node.lat
        v["lng"] = node.lng
        
    for i, edge in enumerate(edges):
        v1 = g.vs.select(objectId = edge.node1.objectId())[0]
        v2 = g.vs.select(objectId = edge.node2.objectId())[0]

        g.add_edges( (int(v1["nid"]), int(v2["nid"])) )
        g.es[i]["n"] = {v1["nid"]:edge.bearing1, v2["nid"]:edge.bearing2}
        g.es[i]["length"] = edge.length
        g.es[i]["n1"] = v1["nid"]
        g.es[i]["n2"] = v2["nid"]
        g.es[i]["bearing1"] = edge.bearing1
        g.es[i]["bearing2"] = edge.bearing2       
        g.es[i]["checked"] = False


    return g
