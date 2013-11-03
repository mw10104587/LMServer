import ParsePy
from igraph import *
from graph import *
from find_neighbor import *
from findPeculiarAngles import *
# from create_user_graph import *

# class Edge:
# edge = Edge('edgeid', "length", "node1", "node2","bearing1","bearing2")
# edge1 = Edge( 0, 133.65, 0, 1, -77, 102 )
# edges = [edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8]
# angleArray = getAngleArrayWithEdgeArray(edges)
# ranked = rankAnglesAccordingToDistanceFromRightAngle(angleArray)
def initAll():
    # load user query graph
    # load map
    initParse()
    g_query = Graph()
    g_map = Graph()
    
    g_query = fetchGraph()
    # path = [(159,326), (248,345), (296,441), (385,412), (477,424), (477,489), (270,571), (167,428), (159,326)] 
    # g_query = create_user_graph(path)   

    g_map = fetchGraph("HeartMap")        # HeartMap or ""
    return [g_query, g_map]

def sub_graph(g_query, g_map): ## New ARG


    # # load user query graph
    # # load map
    # initParse()
    # g_query = Graph()
    # g_map = Graph()
    
    # g_query = fetchGraph()
    # # path = [(159,326), (248,345), (296,441), (385,412), (477,424), (477,489), (270,571), (167,428), (159,326)] 
    # # g_query = create_user_graph(path)   

    # g_map = fetchGraph("HeartMap")        # HeartMap or ""
    
    for i, edge in enumerate(g_query.es):
        print g_query.es[i]["bearing1"], ",", g_query.es[i]["bearing2"]
    for i, edge in enumerate(g_map.es):
        print g_map.es[i]["bearing1"], ",", g_map.es[i]["bearing2"]

    # find the most suitable starting vertex
    edges = []
    for i, edge in enumerate(g_query.es):
        class_e = Edge(edge.index, edge["length"], edge["n1"], edge["n2"], edge["bearing1"], edge["bearing2"])
        edges.append(class_e)

    # print edges[0].edgeId
    angleArray = getAngleArrayWithEdgeArray(edges)     
    ranked_ID_Angle = rankAnglesAccordingToDistanceFromRightAngle(angleArray)
    
    query_start_ID = ranked_ID_Angle[0][0]
    queue_query = []
    results = []

    for i in range(0, len(g_query.vs)):
        queue_query.append( (query_start_ID+i) % len(g_query.vs) )

    ### NEW
    cand_s = findStartingPointGroupInMap(g_query.vs[query_start_ID], g_query, g_map)
    for s in cand_s:
        queue_map = []
        queue_map.append( int(s) )
        g_query_copy = g_query.copy()
        g_query_copy.vs[query_start_ID]["checked"] = True
        g_map_copy = g_map.copy()
        g_map_copy.vs[queue_map[0]]["checked"] = True

        print "Start QID: ", query_start_ID, "Start MID: ", queue_map[0]

        ISO(queue_query, queue_map, g_query_copy, g_map_copy, results)
    ###

    ### OLD
    # queue_map = []
    # queue_map.append( int(findStartingPointInMap(g_query.vs[query_start_ID], g_query, g_map)) )
    # g_query.vs[query_start_ID]["checked"] = True
    # g_map.vs[queue_map[0]]["checked"] = True

    # print "Start QID: ", query_start_ID, "Start MID: ", queue_map[0]

    # ISO(queue_query, queue_map, g_query, g_map, results)
    ###
    return results

def findStartingPointInMap(v_q, g_query, g_map):
    adj_eq = g_query.incident(v_q, mode=ALL)
    min_err_sum, ID = 360, 0
    for v_m in g_map.vs:
        adj_em = g_map.incident(v_m, mode=ALL)
        err_sum = 0
        for e_q in adj_eq:
            min_err = 360
            for e_m in adj_em:
                err = ang_dis(g_query.es[e_q], g_map.es[e_m], v_q["nid"], v_m["nid"]) 
                if err < min_err:
                    min_err = err
            err_sum += min_err
        if err_sum < min_err_sum:
            min_err_sum = err_sum
            ID = v_m["nid"]
    return ID

def findStartingPointGroupInMap(v_q, g_query, g_map, tolerance = 50):
    adj_eq = g_query.incident(v_q, mode=ALL)
    cand_ID = set()
    for v_m in g_map.vs:
        adj_em = g_map.incident(v_m, mode=ALL)
        err_sum = 0
        for e_q in adj_eq:
            min_err = 360
            for e_m in adj_em:
                err = ang_dis(g_query.es[e_q], g_map.es[e_m], v_q["nid"], v_m["nid"]) 
                if err < min_err:
                    min_err = err
            err_sum += min_err
        if err_sum < tolerance:
            cand_ID.add(v_m["nid"])
    return cand_ID

def ISO( queue_query, queue_map, g_query, g_map, results ):                      # 2,4
    candidates = find_neighbor(queue_query, queue_map, g_query, g_map)          # 2,4 [5 or 6]
    print "queue_map: ", queue_map
    print "Cand: ", candidates

    for i in candidates:             # 5,6
        queue_map_copy = list(queue_map)
        queue_map_copy.append(i)                 # 2,4,5
        if len(queue_map_copy) == len(queue_query):   
            iso_subgraph = []
            for vid in queue_map_copy:
                iso_subgraph.append((g_map.vs[vid]["lat"],g_map.vs[vid]["lng"]))
            results.append(iso_subgraph)
            print "ISO: ", iso_subgraph
        else:
            # print queue_map_copy[len(queue_map)-1], queue_map_copy[len(queue_map)-2]
            # print queue_query[len(queue_map)-1], queue_query[len(queue_map)-2]
            to_be_checked_m_edgeID = g_map.get_eid(queue_map_copy[len(queue_map_copy)-1], queue_map_copy[len(queue_map_copy)-2])
            to_be_checked_q_edgeID = g_query.get_eid(queue_query[len(queue_map_copy)-1], queue_query[len(queue_map_copy)-2])
            g_map_copy = g_map.copy()
            g_map_copy.es[to_be_checked_m_edgeID]["checked"] = True
            g_map_copy.vs[queue_map_copy[len(queue_map_copy)-1]]["checked"] = True

            
            
            g_query.es[to_be_checked_q_edgeID]["checked"] = True
            g_query.vs[queue_query[len(queue_map)-1]]["checked"] = True
            
            ISO(queue_query, queue_map_copy, g_query, g_map_copy, results)                    # 2,4,5                 

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
    x = v2["lng"]-v1["lng"]
    y = v2["lat"]-v1["lat"]
    theta1 = rectify( math.degrees(math.atan2(y,x))+90 )
    theta2 = rectify( -180 + theta1 )
    return (theta1, theta2)

def rectify(theta):
    if theta > 180:
        return (theta - 360)
    elif theta < -180:
        return (theta + 360)
    else:
        return theta
    
# sub_graph()   