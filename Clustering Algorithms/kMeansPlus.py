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

def kMeans(data,C, phi,k):
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
			# get the mean center
			s = np.zeros(len(data[0,1:]))
			for j in clusters[i]:
				for d in range(len(data[j,1:])):
					s[d] += data[j,d+1]/len(clusters[i])
		
			C[i] = s
		changes = float(jumps)/n


filename = sys.argv[1]
k = int(sys.argv[2])
txt = open(filename)
dim = 0
gon = np.genfromtxt('gonzaPhi.txt',delimiter = "\n")
print "gon"
print gon
# load data
data = np.genfromtxt(filename,delimiter = "\t")
n = len(data)
#print phi
TMC = []
s = 0.0
count = 0
for runs in range(25):
	# Kmeans++ initialisation
	phi =  np.empty(n)
	phi.fill(0)

	C = kMeansPlusInit(data,phi,k)
	#print C
	#print phi
	# get clusters :
	kMeans(data, C,phi,k)
	#print phi
	#print C
	#compute the 3-mean cost
	flag = 1
 	for f in range(n):
		if(phi[f] != gon[f]) :
			flag = 0
			break
	if(flag == 1):
		count = count+1
	tmc = 0.0
	for i in range(n):
		tmc += distance(data[i,1:], C[int(phi[i])])
	tmc = math.sqrt(tmc/n)
	s += tmc
	TMC.append(tmc)

# get CDF 
cum = 0.0
print " matched gonza "
print float(count)/25
for t in range(25):
	TMC[t] /= s
	cum += TMC[t]
	TMC[t] = cum
print TMC
plt.figure(figsize = (10,8))
plt.plot(TMC)
plt.show()		
'''
plt.figure(figsize = (10,8))
plt.scatter(data[:,1],data[:,2],s= 50, c= phi)
plt.show()
'''
