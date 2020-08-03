import math
debug = False
def getNumberOfLevels(index): ##if index is 0 level will be 1
	if(debug):
		print("index:",index,"nooflevels:",math.floor(math.log(index+1,2))+1)
	return math.floor(math.log(index+1,2))+1

def findIndex(index): ##if index is 0 level will be 0 and pos will be 0 
	l = getNumberOfLevels(index)
	maximum = pow(l - 1,2) - 1
	localPos = index - maximum  ## make index start form 0
	levelIndex = l - 1  ## make index start form 0
	if(debug):
		print("number:",index,"localPos:",localPos,"levelIndex:",levelIndex,"\n")
	return (localPos , levelIndex)

# print(getNumberOfLevels(1), "\n")
# (localPos,levelIndex) = findIndex(0)
# print("levelIndex: ", levelIndex, "localPos: ", localPos, "\n")
def findChild(index):
	(localPos , levelIndex) = findIndex(index)
	child1 =  pow(levelIndex,2) - 1 + localPos*2
	return child1
def heapify(inArray, unsortedIndex):
	noOfIteration = getNumberOfLevels(len(inArray)) 
	for i in range(noOfIteration-1):
		for j in range (pow(2,(noOfIteration-i -2))-1,pow(2,(noOfIteration-i-1))-1):
			# print("noOfIteration:",noOfIteration,"pow((noOfIteration-i -2),2)-1:",(noOfIteration-i -2),"i:",i,"j:",j, "n:",inArray[j])
			(localPos , levelIndex) = findIndex(j)
			offset = pow(levelIndex,2) + localPos
			if (j+offset <len(inArray)):
				if(inArray[j] < inArray[j+offset]):
					inArray[j] = inArray[j] + inArray[j+offset]
					unsortedIndex[j] = unsortedIndex[j] + unsortedIndex[j+offset]
					inArray[j+offset] = inArray[j] - inArray[j+offset]
					unsortedIndex[j+offset] = unsortedIndex[j] - unsortedIndex[j+offset]
					inArray[j] = inArray[j] - inArray[j+offset]
					unsortedIndex[j] = unsortedIndex[j] - unsortedIndex[j+offset]
			if(j+offset+1 < len(inArray)):
				if (inArray[j] < inArray[j+ offset + 1]):
					inArray[j] = inArray[j] + inArray[j+offset+1]
					unsortedIndex[j] = unsortedIndex[j] + unsortedIndex[j+offset+1]
					inArray[j+offset+1] = inArray[j] - inArray[j+offset+1]
					unsortedIndex[j+offset+1] = unsortedIndex[j] - unsortedIndex[j+offset+1]
					inArray[j] = inArray[j] - inArray[j+offset+1]
					unsortedIndex[j] = unsortedIndex[j] - unsortedIndex[j+offset+1]
def swap(inArray,j,i):
	inArray[j] = inArray[j] + inArray[i]
	inArray[i] = inArray[j] - inArray[i]
	inArray[j] = inArray[j] - inArray[i]

def sort(unsortedList,unsortedIndex,sortedList,sortedIndex):
	sortedList.append(unsortedList[0])
	sortedIndex.append(unsortedIndex[0])
	unsortedList[0] = unsortedList[-1]
	unsortedIndex[0] = unsortedIndex[-1]
	if(debug):
		print("sortedList[-1]:",sortedList[-1],"unsortedList[0]:",unsortedList[0])
	del unsortedList[-1]
	del unsortedIndex[-1]

def adjustList(unsortedList,unsortedIndex):
	currentIndex = 0
	change = 0
	while(1):
		child1 = findChild(currentIndex)
		if(child1+1 < len(unsortedList)):
			if(unsortedList[child1] > unsortedList[child1+1]):
				bigChild = child1
			else:
				bigChild = child1 + 1
		elif(child1 < len(unsortedList)):
			bigChild = child1
		else:
			break

		if (unsortedList[bigChild] > unsortedList[currentIndex]):
			swap(unsortedList,bigChild,currentIndex)
			swap(unsortedIndex,bigChild,currentIndex)
			currentIndex = bigChild
		else:
			break


def heapSortWeights(weightList,weightIndex):
	sortedArray = []
	sortedIndex = []
	heapify(weightList, weightIndex)
	while(len(weightList)>0):
		sort(weightList,weightIndex,sortedArray,sortedIndex)
		adjustList(weightList,weightIndex)
	weightList = sortedArray
	weightIndex = sortedIndex
def testAlgo():
	unsortedArray = [12,10,20,0,30,5,40,100]
	duplicateunsortedArray = [12,10,20,0,30,5,40,100]
	unsortedIndex = [0,1,2,3,4,5,6,7]
	heapify(unsortedArray, unsortedIndex)
	print(unsortedArray)
	sortedArray = []
	sortedIndex = []
	while(len(unsortedArray)>0):
		sort(unsortedArray,unsortedIndex,sortedArray,sortedIndex)
		adjustList(unsortedArray,unsortedIndex)
	print(sortedArray)
	print("sortedIndex \n")
	for i in sortedIndex:
		print(duplicateunsortedArray[i]," ")

def main():
	testAlgo()
	
if(__name__ == "__main__"):
	main()


