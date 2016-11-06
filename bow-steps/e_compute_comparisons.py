"""
===========================================
5. Compute comparisons between all images
===========================================

"""

import sys
sys.path.append('utils')
import distance as dist
import pickle
import cPickle
import imtools
import numpy as np
import logging
import itertools
from timeit import default_timer as timer
from joblib import Parallel, delayed
import multiprocessing

logging.basicConfig(level=logging.DEBUG)
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class ImageSimilarity():
    def __init__(self, path, distance_metric='chisquared'):
        self.path = path
        self.histograms = None
        self.im_list = imtools.get_imlist(path)
        self.all_scores=[]
        self.all_dist=[]
        self.logger = logging.getLogger(__name__)
        self.load_histograms()
        self.load_tfidf()

        self.dist_function = dist.distance(distance_metric)

    def load_histograms(self):
        self.logger.info('Loading histograms...')
        try:
            f = open(self.path+'_histograms.pickle', 'r')
            self.histograms = pickle.load(f)
            f.close()
            self.logger.info('Finished loading histograms')

        except Exception as e:
            self.logger.error('Failed to load histograms %s', e)

    def load_tfidf(self):
        self.logger.info('Loading TfIdf...')
        try:
            f = open(self.path+'_tfidf.pickle', 'r')
            self.all_scores = pickle.load(f)
            f.close()
            self.logger.info('Finished loading TfIdf')

        except Exception as e:
            self.logger.error('Failed to load TfIdf %s', e)

    def tfidf_weighing(self):
        self.logger.info('Computing TFIDF weighing comparison')
        #compute new histograms with weights
        for idx,hist in enumerate(self.histograms):
            #TFIDF weighing
            self.histograms[idx] = hist*self.all_scores[idx]

    def computeDistance(self, h1):
        temp_dist = []
        for h2 in self.histogram:
            self.dist_function.compute_distance(h1,h2)
            temp_dist.append(vector_distance)
        return temp_dist

    def compute_comparison_pairwise(self):
        self.logger.info('Computing pairwise comparison')
        dictionary = AutoVivification()

        for idh1, h1 in enumerate(self.histograms):
            self.logger.debug('Compute pairwise comparison %s of %s', idh1, len(self.histograms))
            start = timer()
            dist = []
            f1 = open(self.path+'_comparison.pickle', mode='a+b')
            for idh2, h2 in enumerate(self.histograms):
                if str(idh2) in dictionary:
                    if str(idh1) in dictionary[str(idh2)]:
                        dist.append(dictionary[str(idh2)][str(idh1)])
                        continue

                if str(idh1) in dictionary:
                    if str(idh2) in dictionary[str(idh1)]:
                        dist.append(dictionary[str(idh1)][str(idh2)])
                        continue

                dist.append(self.dist_function.compute_distance(h1,h2))
                dictionary[str(idh1)][str(idh2)] = self.dist_function.compute_distance(h1,h2)
            end = timer()
            self.logger.debug('Time to run iter.product(): %s', end-start)
            cPickle.dump(dist,f1)
            f1.close()

    def compute_image_similarity(self, tfidf=False):
        self.logger.info('Computing histogram distances...')
        if tfidf:
            self.tfidf_weighing()
        #self.compute_comparison_nested()
        self.compute_comparison_pairwise()
        #self.compute_comparison_parallel()


if __name__ == '__main__':
    image_similarity = ImageSimilarity(path=sys.argv[1])
    image_similarity.compute_image_similarity(tfidf=True)
