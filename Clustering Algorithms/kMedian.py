from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram,linkage,fcluster
import sys
import numpy as np
import math 
from random import random,randint
from bisect import bisect


def distance(p1,p2):
        sum = 0.0
        for i in range(len(p1)):
                sum += (p1[i]-p2[i])**2
        return math.sqrt(sum)



def kMeansPlusInit(data,phi,k):
	n = len(data)
	C = []
	c1 = randint(0,n-1)
	C.append(data[c1,1:])

	#print C
	for i in range(1,k):
		Pr = []
		tot = 0.0
		for j in range(n):
			dist  = (distance(data[j,1:],C[int(phi[j])]))**2
			tot += dist
			Pr.append(dist)
		cdf = 0.0
		for j in range(n):
			Pr[j] = Pr[j]/tot
			cdf += Pr[j]
			Pr[j] = cdf
		randomint = bisect(Pr,random())
		#print randomint
		C.append(data[randomint,1:])
		#find minimum dist
		for j in range(n):
			if distance(C[int(phi[j])],data[j,1:]) > distance(C[-1],data[j,1:]) :
				phi[j] = len(C)-1
	#print phi
	#print C
	return C

def kMedian(data,C, phi,k):
	changes = 2.0
	n = len(data)	
	while changes > 0.01:
		# get clusters
		jumps = 0
		clusters = []
		for i in range(k):
			clusters.append([])
		for i in range(n):
			for j in range(k):
				flag = 1
				if distance(data[i,1:],C[j]) < distance(data[i,1:],C[int(phi[i])]):
					phi[i] = j
					flag = 0
			if(flag == 0):
				jumps = jumps + 1
			clusters[int(phi[i])].append(i)
				
		

		#print clusters

		for i in range(k):
			# get the median center
			mindist = 0.0
			minind = 0
			flag = 1
			for j in clusters[i]:
				s = 0.0 
				for l in clusters[i]:
					s += distance(data[j,1:],data[l,1:])	
				if(flag == 1):
					mindist = s
					minind = j
					flag =0
				elif(s < mindist):
					mindist = s
					minind = j
				
			C[i] = data[minind,1:]
		changes = float(jumps)/n


filename = sys.argv[1]
k = int(sys.argv[2])
txt = open(filename)
dim = 0
# load data
data = np.genfromtxt(filename,delimiter = "\t")
n = len(data)
#print phi
phi =  np.empty(n)
phi.fill(0)

# run with [1,2,3]

C = []

for i in range(k):
	C.append(data[randint(0,k-1),1:])
#print len(C)
kMedian(data,C,phi,k)

# get cost
cost = 0.0 
for i in range(n):
	cost += distance(data[i,1:],C[int(phi[i])])
cost /= n

print cost

for i in range(k):
	tmp = C[i]
	print str(i)+"\t"+str(tmp[0])+"\t"+str(tmp[1])+"\t"+str(tmp[2])+"\t"+str(tmp[3])+"\t"+str(tmp[4])

