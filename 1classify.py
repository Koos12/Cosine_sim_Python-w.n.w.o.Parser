import sklearn
import os
import sys
import re
import pandas
import numpy as np
import scipy
import unicodedata
import nltk 
import StringIO
from os import path
import cPickle as pickle
import sklearn.preprocessing as pp
import string
import math
from collections import Counter
from decimal import Decimal
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer


class HashTable:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self,key,data):
      hashvalue = self.hashfunction(key,len(self.slots))

      if self.slots[hashvalue] == None:
        self.slots[hashvalue] = key
        self.data[hashvalue] = data
      else:
        if self.slots[hashvalue] == key:
          self.data[hashvalue] = data  #replace
        else:
          nextslot = self.rehash(hashvalue,len(self.slots))
          while self.slots[nextslot] != None and \
                          self.slots[nextslot] != key:
            nextslot = self.rehash(nextslot,len(self.slots))

          if self.slots[nextslot] == None:
            self.slots[nextslot]=key
            self.data[nextslot]=data
          else:
            self.data[nextslot] = data #replace

    def hashfunction(self,key,size):
         return key%size

    def rehash(self,oldhash,size):
        return (oldhash+1)%size

    def get(self,key):
      startslot = self.hashfunction(key,len(self.slots))

      data = None
      stop = False
      found = False
      position = startslot
      while self.slots[position] != None and  \
                           not found and not stop:
         if self.slots[position] == key:
           found = True
           data = self.data[position]
         else:
           position=self.rehash(position,len(self.slots))
           if position == startslot:
               stop = True
      return data

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,data):
        self.put(key,data)


def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    else:
         return False

def definition():
	global T   #Here you give a value to bilbodog (even None)
	T=HashTable()



#WORD = re.compile(r'\w+')
f = open("/Perl/cosineTriples")
tripleWords = []
lines = f.readlines()
for line in lines:
	#print line
	line2=line.split("|")
	line2Length=len(line2)
	for i,a in enumerate(line2):
		if (isNotBlank(a)):
			T=HashTable()
			T[i]=a
			tripleWord=T[i]
			tripleWords.append(tripleWord.lower())
#for element in tripleWords:
#	print element
				
				
	
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



def text_to_vector(text, tripleWords):
		gramWords=[]
		WORD = re.compile(r'\w+')
		words = WORD.findall(text)
		#print Counter(words)
		c=Counter(words)
		mylist=list(c.elements())
		myset = set(mylist)
		mynewlist = list(myset)
		length=len(mynewlist)
		#for element in mynewlist:
			#print element
		#print "******"
		for el in tripleWords:
			if el in myset:
				#print "Gram Word found!!"
				#print el
				gramWords.append(el.lower())
		#print Counter(gramWords)
		return Counter(gramWords)
		
		
path = "/Python27/training/C01"
def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
count = 0
totalTxt=""
full_file_paths = get_filepaths("/Python27/training/C01")

for file in full_file_paths:
    #f = os.path.basename(file)
    note = open(file, "r")
    txt=note.read()
    totalTxt+=txt
    count+=1
    note.close() 
for c in string.punctuation:
     totalTxt= totalTxt.replace(c,"")   
totalTxt=re.sub(r'\s+',' ',totalTxt)
totalTxt='\''+totalTxt+'.\''
#print totalTxt

#text_to_vector(totalTxt, tripleWords)


path = "/Python27/training/C02"


def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
count = 0
totalTxt1=""
full_file_paths = get_filepaths("/Python27/training/C02")


for file in full_file_paths:
#f = os.path.basename(file)
    note = open(file, "r")
    txt=note.read()
    totalTxt1+=txt
    count+=1
    note.close() 
for c in string.punctuation:
     totalTxt1= totalTxt1.replace(c,"")   
totalTxt1=re.sub(r'\s+',' ',totalTxt1)
totalTxt1='\''+totalTxt1+'.\''
#print totalTxt1



path = "/Python27/test/C01"


def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
count = 0

full_file_paths = get_filepaths("/Python27/test/C01")

correctlyClassified=0
incorrectlyClassified=0

for file in full_file_paths:
    #f = os.path.basename(file)
    note = open(file, "r")
    text=note.read()
    #print txt
    H=HashTable()
    H[count]=text
    #print count
    #print H[count]
    if count < 400:
        count+=1
        for c in string.punctuation:
           text= text.replace(c,"")
        text=re.sub(r'\s+',' ',text)
        text='\''+text+'.\''
        #print text
        vector1 = text_to_vector(totalTxt, tripleWords)
        vector2 = text_to_vector(text,tripleWords)
        cosine = get_cosine(vector1, vector2)
        print 'Cosine', cosine
        vector1 = text_to_vector(totalTxt1,tripleWords )
        cosine1 = get_cosine(vector1, vector2)
        print 'Cosine1:', cosine1
        if (cosine<cosine1):
               print "This document was correctly classified as belonging in training set C02 (HIV infections)"
               correctlyClassified+=1
        else:
               print "This document was incorrectly classified as belonging in training set C01 (Tuberculosis)"
               incorrectlyClassified+=1
        print "Number of correctly classified documents (parser): ",correctlyClassified
    note.close() 



