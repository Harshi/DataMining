import sys
import numpy as np
import random
import binascii

def misraGries(txt, k):
	count = []
	labels = []
#	initialize
	for i in range(k):
		count.append(0)
		labels.append("")

	for i in txt:
		if(i in labels):
			j = labels.index(i)
			count[j] = count[j] + 1
		elif(0 in count):
			j = count.index(0)
			labels[j] = i
			count[j] = count[j]+1
		else:
			for e in range(len(labels)):
				if(count[e] is not 0):
					count[e] = count[e]-1
					#if(count[e] is 0):
					#	labels[e] = ""
		#print labels
		#print count
	print labels
	print count

	# Check how many occur 20% of the time
	tot = 0
	print "objects that might occur 20% of the time are"
	for e in range(len(labels)):
		tot += count[e]
	for e in range(len(labels)):
		if(float(count[e])/float(tot) > 0.2):
			print labels[e]	
	tot = 0
	em = 1/float(k)
	print em 
	print "objects that must occur 20% of the time are"
	for e in range(len(labels)):
		tot += count[e]
	for e in range(len(labels)):
		if(float(count[e])/float(tot) > 0.2-em):
			print labels[e]	


	return labels



def getCoeff(k,maxNo):
        randList = []
        while k > 0:
                k = k-1
                randIndex = random.randint(0, maxNo)
                while randIndex in randList:
                        randIndex = random.randint(0, maxNo)
                randList.append(randIndex)

        return randList


def getHashCode(c):
	return binascii.crc32(c) & 0xffffffff


def countMinSketch(txt,k,t):
	C = np.zeros(shape=(t,k))
	#print C
	maxNo =2**32-1;
	a = getCoeff(t,maxNo)
	b = getCoeff(t,maxNo)
	print a
	for c in txt:
#		print c
		for i in range(t):
			#print getHashCode(c)
			col = (a[i]*getHashCode(c)+b[i])%k
			if(col > -1 and col < k):
				C[i][col] += 1
#			else:
#				print col
	print C
	# min counts for 'a','b','c' are:
	cola=0
	colb=0
	colc=0
	print "counts of a,b,c are:"
	print "a\tb\tc"
	for i in range(t):
		cola = (a[i]*getHashCode('a')+b[i])%k
		colb = (a[i]*getHashCode('b')+b[i])%k
		colc = (a[i]*getHashCode('b')+b[i])%k
		print str(C[i][cola])+"\t"+str(C[i][colb])+"\t"+str(C[i][colc])
		
	return C




filename = sys.argv[1]
txt = open(filename)
stream = txt.read()
print "size of stream is " +str(len(stream))
labels = misraGries(stream,10)
counts = countMinSketch(stream,10,5)
