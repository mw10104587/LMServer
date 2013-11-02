import math
from igraph import *

def find_neighbor(queue_q, queue, g_q, g_m):
    cand = []
    queue_m = queue[0:len(queue_q)]
    v_q = g_q.vs[queue_m[len(queue_m)-1]]
    v_m = g_m.vs[queue_q[len(queue_q)-1]]
    adj_edge_q_ids = incident(v_q["nid"], mode=ALL)
    adj_edge_m_ids = incident(v_m["nid"], mode=ALL)

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
                        cand.append(adj_edge_m_id)
                        adj_edge_q["checked"] = True
                else:
                    continue
        else:
            continue


def ang_dis(e_q, e_m, nid_q, nid_m, tolerance = 10):    #Tolerence: Degree
    ang_err = math.fabs(e_q["n"][nid_q] - e_m["n"][nid_m])
    if ang_err < tolerance:
        return ang_err
    else:
        return -1