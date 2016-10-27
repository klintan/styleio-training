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

class ImageSimilarity():
    def __init__(self, path):
        self.path = path
        self.histograms = None
        self.im_list = imtools.get_imlist(path)
        self.all_scores=[]
        self.load_histograms()
        self.logger = logging.getLogger(__name__)

    def load_histograms(self)
            self.logger.info('Loading histograms...')
            try:
                f = open(self.path+'_histograms.pickle', 'r')
                self.histograms = pickle.load(f)
                f.close()
                self.logger.info('Finished loading histograms')

            except Exception as e:
                self.logger.error('Failed to load histograms %s', e)

    def load_tfidf(self)
            self.logger.info('Loading TfIdf...')
            try:
                f = open(self.path+'_tfidf.pickle', 'r')
                self.histograms = pickle.load(f)
                f.close()
                self.logger.info('Finished loading TfIdf')

            except Exception as e:
                self.logger.error('Failed to load TfIdf %s', e)

    def tfidf_weighing(self, histograms):
        #compute new histograms with weights
        for idx,hist in enumerate(histograms):
            #normalize the histogram
            #hist = hist/float(sum(hist))

            #TFIDF weighing
            hist = hist*all_scores[idx]

    def compute_image_similarity(self, histograms):
        dist_function = dist.distance('chisquared')
        temp_dist = []
        all_dist = []
        #print dist_function
        for idx,h1 in enumerate(histograms):
            f1 = open(sys.argv[1]+'_comparison.pickle', mode='a+b')
            for h2 in histograms:
                vector_distance = dist_function.compute_distance(h1,h2)
                #print type(vector_distance)
                temp_dist.append(vector_distance)
                #print type(temp_dist)

            #all_dist.append(temp_dist)
            cPickle.dump(temp_dist,f1)

            print idx

            #print temp_dist
            #print np.shape(all_dist)
            temp_dist = []
            f1.close()

# f1 = open(sys.argv[1]+'_tfidf.pickle', 'r')
# while 1:
#     try:
#         all_scores.append(pickle.load(f1))
#     except EOFError:
#         break
# f1.close()

if __name__ == '__main__':
image_similarity = ImageSimilarity(path=sys.argv[1])
image_similarity.compute_image_similarity()
