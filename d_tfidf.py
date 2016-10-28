"""
===========================================
4. Calculate TFIDF weight for image set
===========================================

"""
import numpy as np
from PIL import Image
import sys
sys.path.append('utils')
import imtools
import os
import pickle
import logging

from scipy.cluster.vq import *

logging.basicConfig(level=logging.INFO)

class TfIdf():
    def __init__(self, path):
        self.path = path
        self.histograms = None
        self.im_list = imtools.get_imlist(path)
        self.all_scores=[]
        self.logger = logging.getLogger(__name__)
        self.load_histograms()

    def load_histograms(self):
        self.logger.info('Loading histograms...')
        try:
            f = open(self.path+'_histograms.pickle', 'r')
            self.histograms = pickle.load(f)
            f.close()
            self.logger.info('Finished loading histograms')

        except Exception as e:
            self.logger.error('Failed to load histograms %s', e)

    #n_containing(word, histograms) returns the number of documents containing word.
    def n_containing(self, wordidx, word, histograms):
        noOfContainingIms=[]
        count=0
        for idx,im in enumerate(histograms):
            if im[wordidx]>0:
                count+=1

        #print "Total no of docs containing the word"
        #word needs to be the index  in im of the word. If it is >0 it contains the word.
        return count
        #return sum(1 for im in histograms if im[wordidx] >0)

    #tf(word, histogram) computes "term frequency" which is the number of times a word appears in a image
    def tf(self, word, im):
        return float(word) / sum(im)

    #idf(wordidx, word, histograms) computes "inverse document frequency" which measures how common a word is among all documents in bloblist
    def idf(self, wordidx,word, histograms):
        return np.log(len(histograms) / (1 + self.n_containing(wordidx, word, histograms)))

    #tfidf(word, im, im_list) computes the TF-IDF score.
    def tfidf(self, wordidx,word, im, histograms):
        return self.tf(word, im) * self.idf(wordidx, word, histograms)

    #tfidf(word, im, im_list) computes the TF-IDF score.
    def save_tfidf(self):
        self.logger.info('Saving tfidf...')
        f1 = open(sys.argv[1]+'_tfidf.pickle','w')
        pickle.dump(self.all_scores,f1)
        f1.close()

    def compute_tfidf_scores(self):
        self.logger.info('Computing tfidf score')
        self.logger.debug('Histograms length %s', np.shape(self.histograms))
        for i, im in enumerate(self.histograms):
            self.logger.debug('Processing histogram %s out of %s', i, len(self.histograms))
            scores = [self.tfidf(wordidx,word, im, self.histograms) for wordidx,word in enumerate(im)]
            self.all_scores.append(scores)
        self.save_tfidf()


if __name__ == '__main__':
    tfidf = TfIdf(path=sys.argv[1])
    tfidf.compute_tfidf_scores()

