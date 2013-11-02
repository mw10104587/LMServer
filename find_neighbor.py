import math
from igraph import *

def find_neighbor(queue, queue_m, g_q, g_m):
    cand = []
    # print queue
    queue_q = queue[0:len(queue_m)]
    v_q = g_q.vs[queue_q[len(queue_q)-1]]
    v_m = g_m.vs[queue_m[len(queue_m)-1]]
    adj_edge_q_ids = g_q.incident(v_q, mode=ALL)
    adj_edge_m_ids = g_m.incident(v_m, mode=ALL)

    print "adj_edge_q_ids: ", adj_edge_q_ids
    print "adj_edge_m_ids: ", adj_edge_m_ids

    for adj_edge_q_id in adj_edge_q_ids:
        adj_edge_q = g_q.es[adj_edge_q_id]
        if adj_edge_q["checked"] == False:
            for adj_edge_m_id in adj_edge_m_ids:
                adj_edge_m = g_m.es[adj_edge_m_id]
                if adj_edge_m["checked"] == False:
                    err = ang_dis(adj_edge_q, adj_edge_m, v_q["nid"], v_m["nid"])
                    if err == -1:
                        continue
                    else:
                        if adj_edge_m["n1"] != v_m["nid"]:
                            cand.append(int(adj_edge_m["n1"]))
                        else:
                            cand.append(int(adj_edge_m["n2"]))
                else:
                    continue
        else:
            continue
    return cand

def ang_dis(e_q, e_m, nid_q, nid_m, tolerance = 90):    #Tolerence: Degree
    # print e_q["n"][nid_q], e_m["n"][nid_m]
    ang_err = math.fabs(e_q["n"][nid_q] - e_m["n"][nid_m])
    print "|(", e_q["n1"], ",", e_q["n2"], ") - (", e_m["n1"], ",", e_m["n2"], ")|: ",  ang_err
    if ang_err < tolerance:
        return ang_err
    else:
        return -1