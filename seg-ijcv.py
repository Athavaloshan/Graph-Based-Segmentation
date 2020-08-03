# convention (i,j) i - row, j - column (0.0) top left corner  x axis left to right y axis top to bottom
# x = column y = row
#image shape no of rows * no of columns
#larger K means big components
#rest of the work i deal it a img as matrix and convention index is row,column
#edge representation (v1,v2) , v1 = x + y * nuber of columns , v1> v2
import skimage.io
import operator
from heapSort import *
import numpy as np
# from kuruskal_minspantree import *
k = 100
debug = False
size  = 100
def readImage():
	image = skimage.io.imread(fname = "img.jpg")
	# image = image[0:size,0:size,0] ## reduce image size
	image = image[:,:,0]
	image = image.astype(np.int16)
	if(debug): print("imageShape:",image.shape,"\n")
	return image

def populateVertix(image):
	imageShape = image.shape
	if(debug): print("image shape[0]:",imageShape[0], "image shape[1]:", imageShape[1])
	vertexDict= {}
	for y in range (imageShape[0]):
		for x in range(imageShape[1]):
			vertexDict.update({x + y * imageShape[1] : [x,y,x + y * imageShape[1]]})
	return vertexDict

def populateEdges(image,vertexDict):
	# print(image)
	imageShape = image.shape
	edgeDict = {}
	offsetList = [[1,0],[0,1],[1,1],[-1,1]] ##[-1,-1],[0,-1],[1,-1],[-1,0],[-1,0],[-1,1],[0,1],[1,1]]
	for vertexid,coor in vertexDict.items():
		x = coor[0]
		y = coor[1]
		for offset in offsetList:
			if( (dimx > x + offset[0] >= 0) and (dimy > y + offset[1] >= 0)):
				w = abs(image[y,x] - image[y+offset[1],x+offset[0]])
				# print ("x: ",x, " y:", y ," image[x,y]: ",image[x,y]," image[x+offset[0],y+offset[1]]:",image[x+offset[0],y+offset[1]]," w:", w)
				edgeCoor = maximize((x,y),(x+offset[0],y+offset[1]))
				edgeDict.update({edgeCoor : w})
	return edgeDict

def initSegmentMap(segmentMap,vertixDict,edgeSegmentMap):
	for key,value in vertixDict.items():
		x = value[0]
		y = value[1]
		segmentId = value[2]
		segmentMap.update({segmentId:[key]})
		edgeSegmentMap.update({segmentId:[]})

def findMinimumWeight(component2,component1,edgeList):
	if(debug):
		print("component1:",component1)
		print("component2:",component2)
	vertexId2 = component2[0]
	segmentId2 = vertexDict[vertexId2][2]
	edgeWeightList = []
	for vertexId in component1:
		x,y,segmentId = vertexDict[vertexId]
		for offsety in [-1,0,1]:
			for offsetx in [-1,0,1]:
				if((-1 < x + offsetx < dimx ) and (-1 < y + offsety < dimy)):
					if(vertexDict[(x + offsetx) + (y + offsety)*dimx][2] == segmentId2):
						if((x + offsetx) + (y + offsety)*dimx > x + y*dimx):
							edgeList.append(((x + offsetx) + (y + offsety)*dimx, x + y*dimx))
						else:
							edgeList.append((x + y*dimx ,(x + offsetx) + (y + offsety) * dimx))
				
	for edge in edgeList:
		edgeWeightList.append(edgeDict[edge])
	return min(edgeWeightList)

def sortEdge(edgelist,value,i,j):
	if(debug):
		print("i:",i," j:",j," i + (j-i)/2", round(i + (j-i)/2) ," edgeDict[edgelist[i]]: ",edgeDict[edgelist[i]], "edgeDict[edgelist[i + (j - i)/2]]: ", edgeDict[edgelist[round(i + (j - i)/2)]],"value: ", value,"\n")
	if(i == j):
		if(edgeDict[edgelist[i]] > value):
			return i
		else:
			return i+1
	else:
		if(edgeDict[edgelist[math.ceil(i + (j - i)/2)]] == value):
			return math.ceil(i+ (j - i)/2)
		elif(edgeDict[edgelist[math.ceil(i + (j - i)/2)]] > value):
			return sortEdge(edgelist,value,i,math.ceil(i - 1  + (j - i)/2))
		else:
			return sortEdge(edgelist,value,math.ceil(i + (j - i)/2),j)

def assignSegment(value, lowvalue, edgeList):
	component1 = segmentMap[value]
	component2 = segmentMap[lowvalue]

	segmentComponent1 = edgeSegmentMap[value]
	segmentComponent2 = edgeSegmentMap[lowvalue]

	for edge in segmentComponent1:
		if(len(segmentComponent2)==0):
			segmentComponent2.append(edge)
		else:
			w = edgeDict[edge]
			index = sortEdge(segmentComponent2,w,0,len(segmentComponent2) - 1)
			# print("index ", index , " edge:" , edge, "\n")
			segmentComponent2.insert(index,edge)

	for edge in edgeList:
		if(len(segmentComponent2)==0):
			segmentComponent2.append(edge)
		else:
			w = edgeDict[edge]
			index = sortEdge(segmentComponent2,w,0,len(segmentComponent2) - 1)
			# print("index ", index , " edge:" , edge, "\n")
			segmentComponent2.insert(index,edge)

	for vertex_id in component1:
		component2.append(vertex_id)
		vertexDict[vertex_id][2] = lowvalue
	del segmentMap[value]
	del edgeSegmentMap[value]
	edgeSegmentMap[lowvalue] = segmentComponent2

		
def mergeSegment(edge,edgeList):
	v1_id = edge[0]
	v2_id = edge[1]
	v1 = vertexDict[v1_id]
	v2 = vertexDict[v2_id]
	smallestID = 0
	if(v1[2] < v2[2]):
		assignSegment(v2[2],v1[2],edgeList)
	else:
		assignSegment(v1[2],v2[2],edgeList)
	if(debug):
		print("merging v1:",v1_id, " v2:", v2_id) 

def isMergeSegments(edge,edgeList):
	v1 = vertexDict[edge[0]]
	v2 = vertexDict[edge[1]]
	if (v1[2] == v2[2]):
		return False
	else:
		component1 = segmentMap[v1[2]]
		component2 = segmentMap[v2[2]]
		intdiff1 = findInternalDifference(component1)
		intdiff2 = findInternalDifference(component2)
		minimumWeight = findMinimumWeight(component2,component1,edgeList)
		minOfInternalDiff = min(intdiff1 + k/len(component1), intdiff2 + k/len(component2))
		if(debug):
			print("v1:",edge[0]," v2:",edge[1]," minimum weight:",minimumWeight," min of internal difference:",minOfInternalDiff)
		if(minimumWeight > minOfInternalDiff):
			return False
		else:
			return True
def findNeighbourVertices(vetice):
	offsetList = [(-1,-1),(0.-1),(1,-1)]
def maximize(v1,v2):
	idv1 = v1[0] + v1[1]*dimx
	idv2 = v2[0] + v2[1]*dimx
	if(idv1 > idv2):
		return (idv1,idv2)
	else:
		return (idv2,idv1)

def findList(globalList,e1,e2,skip):
	found1 = 0
	for subList in globalList:
		if(subList.count(e1 != 0)):
			found1 = 1
			if(subList.count(e2 != 0)):
				
				break
			else:
				found2 = 0
				for secondSubList in globalList:
					if(secondSubList == subList):
						continue
					else:
						if(secondSubList.count(e2 != 0)):
							tempList = secondSubList
							globalList.remove(secondSubList)
							subList = subList + tempList
							sublist.append(e1)
							sublist.append(e2)
							
							found2 =1
							break
				if (not found2):
					globalList.append([e2])
			break
	return found1
def findMaxWeightEdge(edgeList):
	if(debug):
		print("findMaxWeightEdge:",edgeList)
	maxWeight = 0
	for edge in edgeList:
		if(maxWeight < edgeDict[edge]):
			maxWeight = edgeDict[edge]
	if(debug):
		print("max weight:",maxWeight," for edge list:",edgeList)
	return maxWeight

def generateMinSpanTree(segment):
	idx = vertexDict[segment[0]][2]
	segementEdgeList = edgeSegmentMap[idx]
	# sortEdges(segementEdgeSet)
	# sortedSegementEdgeDict = sorted(segementEdgeDict.items(), key=operator.itemgetter(1))
	if(debug):
		print("minspantree:",segementEdgeList,"idx:",idx)
	globalList = []
	skip = 0
	found2 = 0
	for edge in segementEdgeList:
		found1 = findList(globalList,edge[0],edge[1],skip)
		if(not found1):
			found2 = findList(globalList,edge[1], edge[0],skip)
		if(not(found1) and not(found2)):
			globalList.append([edge])
		if(len(globalList[0]) == (len(segmentMap[idx]) - 1)):
			break 
	return globalList[0]


def findInternalDifference(segment):
	if(debug):
		print("findInternalDifference:segment:",segment)
	if(len(segment) == 1):
		return 0
	minSpanEdgeList = generateMinSpanTree(segment)
	# print("generateMinSpanTree:",minSpanEdgeList)
	return findMaxWeightEdge(minSpanEdgeList)

def paint(segDict):
	img = skimage.io.imread(fname = "img.jpg")
	# img = img[0:size,0:size] ## reduce image size
	# (r,g,b) = (0,0,0)
	for index,vertexList in segDict.items():
		(cx,cy,ci) = vertexDict[vertexList[0]]
		(r,g,b) = img[cy][cx]
		for vertex in vertexList:
			(x,y,i) = vertexDict[vertex]
			img[y][x][0] = r 
			img[y][x][1] = g 
			img[y][x][2] = b
		# r = r + 5
		# g = g + 5
		# b = b + 5
	img = img.astype(np.uint8)
	skimage.io.imsave("imgprocessed.jpg",img)
	skimage.io.imshow(img)
	return
# def sortEdges():
img = readImage()
if(debug):
	print("img:",img)
# img = img[:][:][0]
# print("img:",img)
dimx = img.shape[1]
dimy = img.shape[0]
# if(debug): print(img)
vertexDict = populateVertix(img) ##{x + y * imageShape(1):[x,y,segmentId]}
if(debug):
	print("img:",img)
	print ("vertexDict","\n")
# print(vertexDict)
for vertexId,value in vertexDict.items():
	if(debug):
		print("(",vertexId,",",value[0],",",value[1],",",value[2],")")

edgeDict = populateEdges(img,vertexDict) ## {(v1 id,v2 id):w}
if(debug):
	print ("edgeDict","\n")
	print("size of edgeDict:",len(edgeDict))
for coor,weight in edgeDict.items():
	id1 = coor[0]
	id2 = coor[1]
	if(debug):
		print("(",id1,",",id2,",",weight,")")
sortedEdgeDict = sorted(edgeDict.items(), key=operator.itemgetter(1))
segmentMap = {}	##id,vertix
edgeSegmentMap = {} ##id , edges as tuples(v1,v2)
initSegmentMap(segmentMap,vertexDict, edgeSegmentMap)
# select smallest weight edge
# if veritxes in same segment
# skip
# else 
# ismerge()
# create segment pool
# initialize segment pool
edgeList = []
for edge,w in sortedEdgeDict:
	edgeList = []
	if(isMergeSegments(edge,edgeList)):
		mergeSegment(edge,edgeList)

for key,item in segmentMap.items():
	print("key:",key," vertix:",item)

paint(segmentMap)






