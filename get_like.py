import ParsePy
from igraph import *
from graph import *

def init_like():
	initParse()
	query = ParsePy.ParseQuery("LikeNode")
	nodes = query.fetch()
	query = ParsePy.ParseQuery("LikeEdge")
	edges = query.fetch()
	return nodes

def get_like(nodes):
	data = []

	for n in nodes:
		data.append((n.lat, n.lng))
	
	return data

# print get_like()