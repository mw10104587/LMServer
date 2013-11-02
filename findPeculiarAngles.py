import math

class Node:
    def __init__(self, nodeId, edgeArray):
        self.nodeId = nodeId
        self.edgeArray = edgeArray

class Edge:
    def __init__(self, edgeId, length, node1, node2, bearing1, bearing2):
        self.edgeId = edgeId
        self.length = length
        self.node1  = node1
        self.node2  = node2
        self.bearing1 = bearing1
        self.bearing2 = bearing2      


# edge1 = Edge( 0, 133.65, 0, 1, -77, 102 )
# edge2 = Edge( 1, 151.63, 1, 2, 175, -4 )
# edge3 = Edge( 2, 283.85, 2, 3, 144, -35 )
# edge4 = Edge( 3, 342.09, 3, 4, 68, -111 )
# edge5 = Edge( 4, 126.56, 4, 5, 2, -177 )
# edge6 = Edge( 5, 133.05, 5, 6, -84, 95 )
# edge7 = Edge( 6, 142.67, 6, 7, -109, 70 )
# edge8 = Edge( 7, 168.65, 7, 0, -27, 152 )
# edges = [edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8]

# node1 = Node(0, [0,1])
# node2 = Node(1, [1,2])
# node3 = Node(2, [2,3])
# node4 = Node(3, [3,4])
# node5 = Node(4, [4,5])
# node6 = Node(5, [5,6])
# node7 = Node(6, [6,7])
# node8 = Node(7, [7,0])
# nodes = [node1, node2, node3, node4, node5, node6, node7, node8]


angles = []

#get the middle node first.
def getMiddleNodeWithTwoEdges(edge1, edge2):
    node1 = edge1.node1
    node2 = edge1.node2
    node3 = edge2.node1
    node4 = edge2.node2
    if node1 == node3:
        return node1
    if node1 == node4:
        return node1
    if node2 == node3:
        return node2
    if node2 == node4:
        return node2


def getBearingFromEdgeWithNodeId(nodeId, edge):
    if nodeId == edge.node1:
        return edge.bearing1
    if nodeId == edge.node2:
        return edge.bearing2


def calculateTheAngleWithTwoBearing(b1, b2):
    #if they are on different direction (compared with north)
    if b1*b2 < 0:
        return math.fabs(b1) + math.fabs(b2)
    #if they are on same direction (compared with north)
    if b1*b2 > 0:
        if math.fabs(b1) > math.fabs(b2):
            return math.fabs(b1) - math.fabs(b2)
    else:
        return math.fabs(b2) - math.fabs(b1) 

# The most important function
def getAngleArrayWithEdgeArray(edges):
    
    for i in range(len(edges)):
        #to cope with the last one, when the subgraph ends
        if i == 7:
            x = 0
        else:
            x = i+1
        middleNode = getMiddleNodeWithTwoEdges(edges[i], edges[x])
        b1 = getBearingFromEdgeWithNodeId(middleNode, edges[i])
        b2 = getBearingFromEdgeWithNodeId(middleNode, edges[x])
        # print "b1 = " + str(b1) + ", b2 = " + str(b2)
        angles.append(calculateTheAngleWithTwoBearing(b1,b2) )
        
    #print getBearingFromEdgeWithNodeId(0, edge1)
        #print getBearingFromEdgeWithNodeId(7, edge8)
    return angles

def isCloseToRightAngle(angle):
    return angle < 100 and angle > 80

def isCloseToTwiceRightAngle(angle):
    return angle < 190 and angle > 170

def isCloseToThirdRightAngle(angle):
    return angle < 280 and angle > 260

def rankAnglesAccordingToDistanceFromRightAngle(angles):
    _angles = list(angles)
    nodeIds = []   
    print "nodeIds = ", nodeIds 

    #generate a list to map index
    for x in range(len(angles)):
        nodeIds.append(x)

    print "nodeIds = ", nodeIds

    #print _angles
    index = 0
    for i in range(len(_angles) ):
        a = _angles[index]
    if isCloseToRightAngle(a) or isCloseToTwiceRightAngle(a) or isCloseToThirdRightAngle(a):
        #print "so close, leave it there and move the index"
        #index = index + 1
        _angles.append( _angles[index] )
        del _angles[index]
        nodeIds.append( nodeIds[index] )
        del nodeIds[index]
    else:
        #_angles.append( _angles[index] )
        #del _angles[index]
        index = index + 1
    #print _angles

    return zip(nodeIds, _angles)

# angleArray = getAngleArrayWithEdgeArray(edges)
# print angleArray
# ranked = rankAnglesAccordingToDistanceFromRightAngle(angleArray)
# print ranked
# print "the weirdest angle = "
# print ranked[0]
