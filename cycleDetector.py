import numpy as np
debug = True
def replace(segmentList, v1, v2):
	boolArr = segmentList == segmentList[v1]
	indexArr = np.where(boolArr)
	for index in indexArr:
		segmentList[index] = segmentList[v2]

def detectCycle(edges, n):
	segmentList = np.full(n, -1)
	for edge in edges:
		(v1, v2) = edge
		if(segmentList[v1] == segmentList[v2] and segmentList[v1] != -1):
			return True
		if(segmentList[v1] == -1 and segmentList[v2] == -1):
			if (v1 > v2):
				segmentList[v1] = v2
				segmentList[v2] = v2
			else:
				segmentList[v1] = v1
				segmentList[v2] = v1
		elif (segmentList[v1] == -1 and segmentList[v2] >= 0):
			segmentList[v1] = segmentList[v2]
		elif (segmentList[v1] >= 0 and segmentList[v2] == -1):
			segmentList[v2] = segmentList[v1]
		else:
			if(segmentList[v1] > segmentList[v2]):
				replace(segmentList, v1, v2)
			else:
				replace(segmentList, v2, v1)
	if(debug): print("segList:",segmentList);
	return False

def test():
	edges = [(0,1),(1,2),(2,3),(0,2)]
	if(detectCycle(edges, 4)):
		print("graph has cycle")
	else:
		print("no cycles")
test()				


