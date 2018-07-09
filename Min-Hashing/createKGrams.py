from sys import argv
import binascii
#filename = argv
import random
import time

def getText(filename):
	with open(filename) as f:
		text = f.read();
	return text

def kGramsChar(content,k):
	x = set([])
	text = "";
	txt = list(content)
	for i in range(k-1,len(txt)):
		text = ""
		for j in range(1,k+1):
			text += txt[i-k+j];	
		x.add(text)
	return x

def kGramsWords(content,k):
	x = set([])
	text = "";
	txt = content.split(" ")
	for i in range(k-1,len(txt)):
		text = ""
		for j in range(1,k+1):
			text += " " + txt[i-k+j];	
		x.add(text.strip(" "))
	return x

def Jaccard(doc1,doc2):
	unionLen = len(doc1 | doc2)
	intersectLen = len(doc1 & doc2)
	return float(float(intersectLen)/unionLen)


def generateHashCode(lst):
	hashes = set()
	for st in lst:
		hashes.add(binascii.crc32(st) & 0xffffffff)
	return hashes	

def getCoeff(k,maxNo):
	randList = []
    	while k > 0:
    		k = k-1
		randIndex = random.randint(0, maxNo) 
  		while randIndex in randList:
			randIndex = random.randint(0, maxNo) 
	    	randList.append(randIndex)
		
	return randList


files = getText(argv[1])
print files
GramChars2 = []
GramChars3 = []
GramWords2 = []
i=0;
for f in files.split("\n") :
	if f:
		content = getText(f)
		k = 2
		GramChars2.append(kGramsChar(content, k))
		k=3
		GramChars3.append(kGramsChar(content,k))
		k =2
		GramWords2.append(kGramsWords(content,k))

for i in range(0,len(GramChars2)):
	print str(len(GramChars2[i])) + " " +str(len(GramChars3[i])) + " "+ str(len(GramWords2[i])) 

#build Jaccard similarity between pairs of documents
distance1 = []
distance2 = []
distance3 = []
count = 0;
for i in range(0,len(GramChars2)):
	for j in range(i+1,len(GramChars2)):
		distance1.append(Jaccard(GramChars2[i],GramChars2[j]))
		distance2.append(Jaccard(GramChars3[i],GramChars3[j]))
		distance3.append(Jaccard(GramWords2[i],GramWords2[j]))			
print distance1
print distance2
print distance3



##################################################################################################################
################################ MIN-HASHING #####################################################################

# Generte 32 bit  hash code for D1 and D2
GramChars3HashD =[];
for m in range(0,2):
	GramChars3HashD.append(generateHashCode(GramChars3[m]))

print GramChars3[0]
# pick coeffiencients a and b for "k" hash functions
t = [20, 60, 150, 300, 600]
#t =[20]
maxNo =2**32-1;
maxPrime = 4294967311;
for k in t:
	start = time.time()
	docSign = []
	a = getCoeff(k,maxNo)
	b = getCoeff(k,maxNo)
	for doc in GramChars3HashD:
		minHashSignature = []
		'''
		print "k=" + str(k)
		print "size of a " + str(len(a))
		print "size of b " + str(len(b))
		'''
		for i in range(0,k):
			minHash = maxPrime +1
			for h in doc:
				code = (a[i] * h + b[i]) % maxPrime
				if code < minHash:
					minHash = code
			minHashSignature.append(minHash)
		docSign.append(minHashSignature)
	for i in range(0,len(docSign)):
		for j in range(i+1,len(docSign)):
			doci = docSign[i]
			docj = docSign[j]
			count = 0
			for f in range(0,k):
				if(doci[f] == docj[f]):
					count = count + 1;
			
			print "For k = "+str(k)
			print "similarity = "
			print float(float(count)/k);
	end = time.time()
	print "time taken = "+str((end-start)*1000)		
