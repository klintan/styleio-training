from vgg16 import VGG16
from keras.preprocessing import image
from imagenet_utils import preprocess_input
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import theano
from keras import backend as K
from scipy import spatial
import yaml
import logging
import sys
import pickle
import cPickle
import os
from timeit import default_timer as timer

sys.path.append('../general-steps/utils')
import imtools
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

logging.basicConfig(level=logging.DEBUG)

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class DeepFeatureComparison:
    def __init__(self):
        self.model = VGG16(weights='imagenet', include_top=True)
        self.config = yaml.safe_load(open("../config.yml"))['deep_feature_extraction']
        self.logger = logging.getLogger(__name__)
        self.path = self.config['path']
        self.experiment_name = self.config['experiment_name']
        self.im_list = imtools.get_imlist(self.config['path'])
        self.all_images_data = []
        self.size = self.config['img_size']
        self.save_features = self.config['save_features']
        self.datagen = ImageDataGenerator(
                featurewise_center=True,
                featurewise_std_normalization=False)



    #extract features
    def feature_extraction(self, img_array):
        def convout1_f( X):
            # The [0] is to disable the training phase flag
            return _convout_f([0] + [X])
        inputs = [K.learning_phase()] + self.model.inputs
        _convout_f = K.function(inputs, [self.model.layers[21].output])
        feature = convout1_f(img_array)
        return np.squeeze(feature)

    #save features
    def save_features_func(self):
            self.logger.info('Save features')
            f = open(self.path+'_features.pickle','w')
            pickle.dump(self.all_images_data, f)
            f.close()

    #save features
    def load_features_func(self):
            self.logger.info('Load features')
            f = open(self.path+'_features.pickle','r')
            self.all_images_data = pickle.load(f)
            f.close()
            self.logger.debug('Loaded features, %s', np.shape(self.all_images_data))

    #compute image similiarity
    def compute_similiarity(self):
        self.logger.info('Computing pairwise comparison')
        if not os.path.exists(self.path+'_features.pickle'):
            for idx, img_path in enumerate(self.im_list):
                start = timer()

                self.logger.debug('Extracting feature %s of %s', idx, len(self.im_list))
                img = image.load_img(img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                #get all image features
                self.all_images_data.append(self.feature_extraction(x))
                end = timer()
                self.logger.debug('Time to run iter.product(): %s', end-start)

            if self.save_features:
                self.save_features_func()
        else:
            print 'load'
            self.load_features_func()

        dictionary = AutoVivification()

        for idh1, h1 in enumerate(self.all_images_data):
            self.logger.debug('Compute pairwise comparison %s of %s', idh1, len(self.all_images_data))
            start = timer()
            dist = []
            f1 = open(self.path+'_comparison.pickle', mode='a+b')
            for idh2, h2 in enumerate(self.all_images_data):
                if str(idh2) in dictionary:
                    if str(idh1) in dictionary[str(idh2)]:
                        dist.append(dictionary[str(idh2)][str(idh1)])
                        continue

                if str(idh1) in dictionary:
                    if str(idh2) in dictionary[str(idh1)]:
                        dist.append(dictionary[str(idh1)][str(idh2)])
                        continue

                dist.append(spatial.distance.cosine(h1, h2))
                dictionary[str(idh1)][str(idh2)] = spatial.distance.cosine(h1, h2)
            end = timer()
            self.logger.debug('Time to run iter.product(): %s', end-start)
            cPickle.dump(dist,f1)
            f1.close()


if __name__ == '__main__':
    dfc = DeepFeatureComparison()
    dfc.compute_similiarity()

