import sys
import math

def distOf(p1,p2):
	return math.sqrt((p1(1)-p2(1))**2+(p1(2)-p2(2))**2+(p1(3)-p2(3))**2) 

def getClustersToMerge(distances,clusters,choice)
	for i in range(len(clusters)):
		for j in range(i+1,len(clusters)):
			# check for distance between i and j clusters
			if(choice == 1):
			# min metric
				getMin(clusters[i],cluster[j])				
			else if(choice == 2):
			# max metric
				getMax(clusters[i],clusters[j])
			else if(choice == 3):
			# average choice
				getMean(clusters[i],clusters[j])
			
												

def getMin(clusters[i],clusters[j])
	
# Data is in the format index dim1 dim2 ...
filename = sys.argv[1]
choice = int(sys.argv[2])
txt = open(filename)
data = []
dim = 0
for t in txt.readlines():
	temp = []
	for i in t.split("\t"):
		temp.append(float(i))
	dim = len(temp) -1
	data.append(temp)
#print data
# create a list of clusters
clusters =[]
# initialize cluseters
distances = [] 
minDist = 0
c1 = 0
c2 = 0
for i in range(len(data)):
	clusters.append([int(data[i][0])])
	for j in range(i+1,len(data)):
		distances.append(distOf(data[i][1:dim],data[j][1:dim]))	
		if(i == 0 && j == 1):
			minDist = distances[-1]
			c1 = i
			c2 = j
		else if(minDist > distances[-1])
			minDist = distances[-1]
			c1 = i
			c2 = j
# find all pairs of distances 
# choice of distance metric 
choice = 1
# desired target for clusters
k = 4
noClusters = len(clusters);
	
while(len(clusters) > k):
	for i in 
	indexes = getClustersToMerge(distances,clusters,choice)
	merger(indexes,distances,clusters)

