"""
===========================================
2. Create Vocabulary
===========================================
Make sure all image are same width and height (keep aspect ratio)

"""
import numpy as np
import sys
sys.path.append('utils')
import imtools
import os
import pickle
from PIL import Image
from extract_features import extract_features
import logging
#import PIL.Image
#sys.modules['Image'] = PIL.Image
#import Image

from skimage.feature import daisy
from skimage.color import rgb2gray
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

logging.basicConfig(level=logging.INFO)


class Vocabulary:
    def __init__(self,imgs_path, feature_type, img_type='test', vocab_size=800):
        self.im_list = imtools.get_imlist(imgs_path)
        self.img_type = img_type
        self.vocab_size = vocab_size
        self.feature_type = feature_type
        self.vocab_model = None
        self.logger = logging.getLogger(__name__)

    def feature_extraction(self):
        self.logger.info('Start feature extraction...')
        feature_extractor = extract_features(self.feature_type)

        #Feature list
        all_features = []
        for idx,image_name in enumerate(self.im_list):
            self.logger.debug('Processing image %s, %s out of %s', image_name, idx, len(self.im_list))
            try:
                img = np.array(Image.open(image_name))
            except Exception as e:
                self.logger('Failed to load image %s', e)

            features = feature_extractor.extractFeature(img)
            self.logger.debug('Feature shape %s', features.shape)

            all_features.append(features.reshape(-1, 200))
        self.logger.info('Finished feature extraction')
        return all_features

    def create_vocabulary(sefl, feature_list):
        self.logger.info('Start vocabulary creation')
        X = np.vstack(all_features)
        self.vocab_model = MiniBatchKMeans(n_clusters=vocab_size,max_iter=200,verbose=1)
        #km = KMeans(n_clusters=200,n_jobs=-1,verbose=1)
        self.vocab_model.fit(X)
        self.logger.info('Finished vocabulary creation')

    def save_vocabulary(self):
        self.logger.info('Save vocabulary')
        f = open(sys.argv[1]+'_vocab.pickle', 'w')
        pickle.dump(self.vocab_model,f)
        f.close()
        self.logger.info('Vocabulary saved succesfully')


if __name__ == '__main__':
    voc = vocabulary(imgs_path=sys.argv[1], vocab_size = 800, feature_type='daisy')
    all_features = voc.feature_extraction()
    voc.create_vocabulary(all_features)
    voc.save_vocabulary()





