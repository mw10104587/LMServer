from igraph import *

def growing(g, sub_g):

    output_g = sub_g.copy()
    outer_v = sub_g.vs.find(checked==False)
	for i, vertex in enumerate(outer_v):
	    output_g.add_vertices(len(g.neighbors(int(vertex["nid"])))
    outer_e = 
		
		
		
# checked = True