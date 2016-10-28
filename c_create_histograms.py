"""
===========================================
3. Create Histograms and Calculate TFIDF weight for image set
===========================================


"""
import numpy as np
import sys
sys.path.append('utils')
import imtools
import os
import pickle
from PIL import Image
import logging

from extract_features import ExtractFeatures

from skimage.feature import daisy
from skimage.color import rgb2gray
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from scipy.sparse import coo_matrix

logging.basicConfig(level=logging.INFO)

class PatternHistograms:
    def __init__(self,path, feature_type, vocab_size=800):
        self.path = path
        self.im_list = imtools.get_imlist(path)
        self.vocab_size = vocab_size
        self.feature_type = feature_type
        self.logger = logging.getLogger(__name__)
        self.load_model()

    def load_model(self):
            f = open(self.path+'_vocab.pickle', 'r')
            self.km = pickle.load(f)

    def create_histogram(self):
        counts=[]
        words=[]
        word_occurences=[]
        hists = []
        words_1 = []

        self.logger.info('Start histogram creation...')
        fe = ExtractFeatures(self.feature_type)
        for idx,image_name in enumerate(self.im_list):
            self.logger.debug('Processing image %s, %s out of %s', image_name, idx, len(self.im_list))
            try:
                img = np.array(Image.open(image_name))
            except Exception as e:
                self.logger.error('Failed to load image %s', e)
            features = fe.extractFeature(img)
            words = self.km.predict(features.reshape(-1, 200))
            ##counts = coo_matrix((np.ones(len(words)), (1, words)), shape=(1, 500)).toarray()
            ##counts = coo_matrix((np.ones(len(words)), (1,words)), shape=(1, 500)).toarray()
            hists.append(np.bincount(words,minlength = self.vocab_size))
            words_1.append(words)
        self.logger.debug('')
        self.logger.info('Finished histogram creation')
        return hists

    #normalize the histograms
    def normalize_hIstogram(self, histogram):
        return [word / sum(histogram) for word in float(histogram)]

    #save the histograms
    def save_histograms(self, hists):
            f1 = open(self.path+'_histograms.pickle','w')
            pickle.dump(hists,f1)
            f1.close()

if __name__ == '__main__':
    ph = PatternHistograms(path=sys.argv[1], feature_type='daisy', vocab_size=800)
    hists = ph.create_histogram()
    ph.save_histograms(hists)

