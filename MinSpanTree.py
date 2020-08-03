def generateMinSpanTree(segementEdgeSet,segment):
	if(debug):
		print("minspantree:",segementEdgeSet)
	sortEdges(segementEdgeSet)
	if(len(segment)==1):
		return []
	globalList = []
	skip = 0
	found2 = 0
	for edge in segementEdgeSet:
		found1 = findList(globalList,edge[0],edge[1],skip)
		if(not found1):
			found2 = findList(globalList,edge[1], edge[0],skip)
		if(not(found1) and not(found2)):
			globalList.append([edge])
	return globalList[0]

