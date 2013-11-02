import ParsePy
from igraph import *
from graph import *
from find_neighbor import *
from find_subgraph import *
# class Edge:
# edge = Edge('edgeid', "length", "node1", "node2","bearing1","bearing2")
# edge1 = Edge( 0, 133.65, 0, 1, -77, 102 )
# edges = [edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8]
# angleArray = getAngleArrayWithEdgeArray(edges)
# ranked = rankAnglesAccordingToDistanceFromRightAngle(angleArray)

def sub_graph():
    g_query = Graph()
    g_map = Graph()
    
    # load user query graph
    # load map
    initParse()
    g_query = fetchGraph()
    g_map = fetchGraph() #???
    
    
    # find the most suitable starting vertex
    edges = []
    for i, edge in enumerate(g_query.es):
        class_e = Edge(edge.index, edge["length"], edge["n1"], edge["n2"], edge["bearing1"], edge["bearing2"])
        edges.append(class_e)
    angleArray = getAngleArrayWithEdgeArray(edges)      
    ranked_ID_Angle = rankAnglesAccordingToDistanceFromRightAngle(angleArray)
    
    query_start_ID = ranked_ID_Angle[0][0]
    queue_query = []
    queue_map = []
	
    for i in range(0, len(g_query.vs)):
        queue_query.append( (query_start_ID+i) % len(g_query.vs) )

    queue_map.append( findStartingPointInMap(g_query.vs[query_start_ID], g_map) )

    results = []

    ISO(queue_query, queue_map, g_query, g_map, results)
    

def findStartingPointInMap(v_q, g_map):
    adj_eq = incident(v_q, mode=ALL)
    min_err_sum, ID = 360, 0
    for v_m in g_map.vs:
        adj_em = incident(v_m, mode=ALL)
        err_sum = 0
        for e_q in adj_eq:
            min_err = 360
            for e_m in adj_em:
                err = ang_dis(e_q, e_m, v_q, v_m) 
                if err < min_err:
                    min_err = err
            err_sum += min_err
        if err_sum < min_err_sum:
            min_err_sum = err_sum
            ID = v_m["nid"]
    return ID

def ISO( queue_query, queue_map, g_query, g_map, results ):                      # 2,4
    candidates = find_neighbor(queue_query, queue_map, g_query, g_map)          # 2,4 [5 or 6]
    
    for i in candidates:             # 5,6
        queue_map.append(i)                 # 2,4,5
        if len(queue_map) == len(queue_query):   
            iso_subgraph = []
            for vid in queue_map:
                iso_subgraph.append((g_map.vs[vid]["lat"],g_map.vs[vid]["lng"]))
            results.append(iso_subgraph)
        else:
            to_be_checked_edgeID = g_map.get_eid(queue_map[len(queue_map)-1], queue_map[len(queue_map)-2])
            g_map_copy = g_map.copy()
            g_map_copy.es[to_be_checked_edgeID]["checked"] = True
            ISO(queue_query, queue_map, g_query, g_map_copy, results)                    # 2,4,5

        queue_map.pop()                   
    
sub_graph()   