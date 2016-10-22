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
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine
from scipy import sparse
from scipy.sparse import csr_matrix

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

WORD = re.compile(r'\w+')

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

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


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
cVectorizer = CountVectorizer()
cVectorizer.fit_transform(totalTxt.split('\n'))
trainSetOne = cVectorizer.vocabulary_
#print "Vocabulary:", trainSetOne

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
cVectorizer = CountVectorizer()
cVectorizer.fit_transform(totalTxt1.split('\n'))
trainSetTwo = cVectorizer.vocabulary_

#print "Vocabulary:", trainSetTwo
# Vocabulary: {'blue': 0, 'sun': 1, 'bright': 2, 'sky': 3}

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
        vector1 = text_to_vector(totalTxt)
        vector2 = text_to_vector(text)
        cosine = get_cosine(vector1, vector2)
        print 'Cosine:', cosine
        vector1 = text_to_vector(totalTxt1)
        cosine1 = get_cosine(vector1, vector2)
        print 'Cosine1:', cosine1
        if (cosine<cosine1):
               print "This document was correctly classified as belonging in training set C02 (HIV infections)"
               correctlyClassified+=1
        else:
               print "This document was incorrectly classified as belonging in training set C01 (Tuberculosis)"
               incorrectlyClassified+=1
        print "Number of correctly classified documents (no parser): ",incorrectlyClassified
        cVectorizer = CountVectorizer()
        cVectorizer.fit_transform(text.split('\n'))   
        smallText = cVectorizer.vocabulary_
        #print "Vocabulary:", smallText
    note.close() 

#cVectorizer = CountVectorizer()
#cVectorizer.fit_transform(trainSetOne)
#trainSetOne = cVectorizer.vocabulary_
#print "Vocabulary:", trainSetOne
#freq_term_matrix = cVectorizer.transform(test_set)
#print freq_term_matrix.todense()
#tfidf = TfidfTransformer(norm="l2")
#tfidf.fit(freq_term_matrix)
#print "IDF:", tfidf.idf_
#tf_idf_matrix = tfidf.transform(freq_term_matrix)
#print tf_idf_matrix.todense()

#x=len(documents)

#x=x-2
#documents=documents[0:x]
#documents=documents+'\n'+')'
#print documents
#tfidf_matrix = TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform(documents)
#vectorizer=TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False)
#tfidf=vectorizer.fit_transform(documents)
#X=(tfidf*tfidf.T).A
#print X
#X_mat = X.todense()
#print X_mat
#array=cosine_similarity(X[0:1],X)
#print array

