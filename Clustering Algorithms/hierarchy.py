from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram,linkage,fcluster
import sys
import numpy as np
import time

filename = sys.argv[1]
choice = int(sys.argv[2])
txt = open(filename)
dim = 0

# load data
data = np.genfromtxt(filename,delimiter = "\t")
#print data[:,1:]
#plt.scatter(data[:,0],data[:,1])
#plt.show()
start = time.time()
# generate linkage matrix
Z =[]
if(choice == 1): # nearest point min algorithm
	Z = linkage(data[:,1:], 'single')

elif(choice == 2): # Farthest point max algorithm
	Z = linkage(data[:,1:],'complete')

elif(choice == 3): # averaage UPGMA algorithm
	Z = linkage(data[:,1:],'average')
else:
	print("invalid choice")
#print Z
clust = fcluster(Z,4,criterion = 'maxclust')
end = time.time()
print "time taken = "
print end - start
print "clust= "
print clust

# calculate full dendrogram
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
#plt.show()

# visualize the clusters
plt.figure(figsize = (10,8))
plt.scatter(data[:,1],data[:,2],s= 50, c= clust)
#plt.show()

