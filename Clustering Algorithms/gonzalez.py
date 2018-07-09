from matplotlib import pyplot as plt
import sys
import numpy as np
import math
from random import randint

def distance(p1,p2):
	sum = 0.0
	for i in range(len(p1)):
		sum += (p1[i]-p2[i])**2
	return math.sqrt(sum)

filename = sys.argv[1]
k = int(sys.argv[2])
txt = open(filename)
dim = 0

# load data
data = np.genfromtxt(filename,delimiter = "\t")
#print data
n = len(data)
phi = np.zeros(len(data))
C = []
#C.append(data[randint(0,n),1:])
C.append(data[0,1:])
for i in range(1,k):
	M =0
	C.append(data[0,1:])
	for j in range(n):
		if distance(C[int(phi[j])],data[j,1:]) > M :
			M = distance(C[int(phi[j])], data[j,1:])
			C[i] = data[j,1:]
	for j in range(n):
		if distance(data[j,1:],C[int(phi[j])]) > distance(data[j,1:],C[i]):
			phi[j] = i

print C
#print phi
# 3-center cost and 3-means cost
tCC = 0.0
tMC = 0.0
for i in range(n):
	d = distance(data[i,1:],data[int(phi[j]),1:])
	if(tCC < d):
		tCC = d	
	tMC += d**2

#print "3 center cost"
#print tCC
#print "3 mean cost"
#print math.sqrt(tMC/n)
#print phi
#for i in range(n):
#	print phi[i]
plt.figure(figsize = (10,8))
plt.scatter(data[:,1],data[:,2],s= 50, c= phi)
#plt.show()
