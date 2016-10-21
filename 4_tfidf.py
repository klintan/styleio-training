"""
===========================================
4. Calculate TFIDF weight for image set
===========================================

"""

import numpy as np
import Image
import sys
sys.path.append('utils')
import imtools
import os
import pickle

from scipy.cluster.vq import *

f = open(sys.argv[1]+'_histograms.pickle', 'r')
histograms = pickle.load(f)
f.close()

path = sys.argv[1]

nbr_images = imtools.get_imlist(path)

#word, the index of 200 in the histogram
#im, the histogram of the specific image
#histograms, the list of histograms


#tf(word, histogram) computes "term frequency" which is the number of times a word appears in a image
def tf(word, im):
    return float(word) / sum(im)


#n_containing(word, histograms) returns the number of documents containing word.
def n_containing(wordidx, word, histograms):
    noOfContainingIms=[]
    count=0
    for idx,im in enumerate(histograms):
        if im[wordidx]>0:
            count+=1

    #print "Total no of docs containing the word"
    #print count
    #word needs to be the index  in im of the word. If it is >0 it contains the word.
    return count
    #return sum(1 for im in histograms if im[wordidx] >0)

#idf(wordidx, word, histograms) computes "inverse document frequency" which measures how common a word is among all documents in bloblist
def idf(wordidx,word, histograms):
    #print n_containing(word, histograms)
    return np.log(len(histograms) / (1 + n_containing(wordidx, word, histograms)))

#tfidf(word, im, im_list) computes the TF-IDF score.
def tfidf(wordidx,word, im, histograms):
   #print tf(word, im)
    #print idf(wordidx, word,histograms)
    #print word
    #print im
    #print wordidx
    return tf(word, im) * idf(wordidx, word, histograms)
all_scores=[]
#print np.shape(histograms)
#print histograms
f1 = open(sys.argv[1]+'_tfidf.pickle','w')
for i, im in enumerate(histograms):
    print i
    #print np.shape(histograms)
    #print("Top words in document {}".format(i + 1))
    scores = [tfidf(wordidx,word, im, histograms) for wordidx,word in enumerate(im)]
    #print scores
    all_scores.append(scores)

    #sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    pickle.dump(scores,f1)


    #for word, score in sorted_words[:3]:
    #    print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

f1.close()

#print all_scores


#for imwords in histograms:
#    print("Top words in document {}".format(i + 1))
#    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #occurrences of words in each image
#    nbr_occurences = sum( (imwords > 0)*1)
#    print nbr_occurences
    #calculate idf
#    idf = np.log( (1.0*len(nbr_images)) / (1.0*nbr_occurences+1) )
#    print idf


