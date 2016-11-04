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

class ImageSimilarity():
    def __init__(self, path, distance_metric='chisquared'):
        self.path = path
        self.histograms = None
        self.im_list = imtools.get_imlist(path)
        self.all_scores=[]
        self.logger = logging.getLogger(__name__)
        self.load_histograms()
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
            self.histograms = pickle.load(f)
            f.close()
            self.logger.info('Finished loading TfIdf')

        except Exception as e:
            self.logger.error('Failed to load TfIdf %s', e)

    def tfidf_weighing(self):
        #compute new histograms with weights
        for idx,hist in enumerate(self.histograms):
            #TFIDF weighing
            hist = hist*all_scores[idx]

    def computeDistance(self, h1):
        temp_dist = []
        for h2 in self.histogram:
            self.dist_function.compute_distance(h1,h2)
            temp_dist.append(vector_distance)
        return temp_dist

    def compute_comparison_parallel(self):
        # what are your inputs, and what operation do you want to
        # perform on each input. For example...
        num_cores = multiprocessing.cpu_count()
        for idx,h1 in enumerate(self.histograms):
            self.logger.debug('Computing histogram distance for histogram %s of %s', idx, len(self.histograms))
            f1 = open(sys.argv[1]+'_comparison.pickle', mode='a+b')
            results = Parallel(n_jobs=num_cores)(delayed(self.computeDistance)(h1) for h1 in self.histograms)
        print len(results)

    def compute_comparison_product(self):
        temp_dist = []
         #TODO
        # try to remove double loop, we could do pairwise recursive comparison, and remove the ones which we compared
        start = timer()
        f1 = open(sys.argv[1]+'_comparison.pickle', mode='a+b')
        temp_dist = []
        i = 0
        for h1, h2 in itertools.product(self.histograms, repeat=2):
            #print h1 == h2
            # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
            vector_distance =  self.dist_function.compute_distance(h1,h2)
            if len(self.histograms)==i:
                end = timer()
                self.logger.debug('Time to run iter.product(): %s', end-start)
                cPickle.dump(temp_dist,f1)
                temp_dist = []
                start = timer()

                i=0
            i += 1

        f1.close()

    def compute_comparison_nested(self):
        temp_dist = []
        for idx,h1 in enumerate(self.histograms):
            start = timer()
            self.logger.debug('Computing histogram distance for histogram %s of %s', idx, len(self.histograms))
            f1 = open(sys.argv[1]+'_comparison.pickle', mode='a+b')
            for h2 in self.histograms:
                vector_distance =  self.dist_function.compute_distance(h1,h2)
                temp_dist.append(vector_distance)
            end = timer()
            self.logger.debug('Time to run iter.product(): %s', end-start)
            cPickle.dump(temp_dist,f1)
            temp_dist = []
            f1.close()

    def compute_comparison_pairwise(self):
        pass

    def compute_image_similarity(self):
        self.logger.info('Computing histogram distances...')
        self.compute_comparison_nested()
        #self.compute_comparison_parallel()


if __name__ == '__main__':
    image_similarity = ImageSimilarity(path=sys.argv[1])
    image_similarity.compute_image_similarity()
