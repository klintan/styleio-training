from vgg16 import VGG16
from keras.preprocessing import image
from imagenet_utils import preprocess_input
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import theano
from keras import backend as K
from scipy import spatial

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
        self.datagen = ImageDataGenerator(
                featurewise_center=True,
                featurewise_std_normalization=False)

    def convout1_f(X):
            # The [0] is to disable the training phase flag
            return _convout1_f([0] + [X])

    #extract features
    def feature_extraction(self, img_array):
        inputs = [K.learning_phase()] + model.inputs
        _convout1_f = K.function(inputs, [model.layers[21].output])
        feature = convout1_f(img)
        return np.squeeze(feature)

    #save features
    def save_features(self):
            f1 = open(self.path+'_features.pickle','w')
            pickle.dump(self.all_images_data, f1)
            f1.close()

    #compute image similiarity
    def compute_similiarity(self):
        self.logger.info('Computing pairwise comparison')

        for idx, img_path in enumerate(self.im_list):
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            #get all image features
            self.all_images_data.append(self.feature_extraction(x))

         if self.save_features:
            self.save_features()


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

                dist.append(1 - spatial.distance.cosine(h1, h2))
                dictionary[str(idh1)][str(idh2)] = 1 - spatial.distance.cosine(h1, h2)
            end = timer()
            self.logger.debug('Time to run iter.product(): %s', end-start)
            cPickle.dump(dist,f1)
            f1.close()


if __name__ == '__main__':
    dfc = DeepFeatureComparison()
    dfc.feature_extraction()


# img_path = 'images_vgg16/_530_4198.jpeg'
# img = image.load_img(img_path, target_size=(224, 224))
# x1 = image.img_to_array(img)
# x1 = np.expand_dims(x1, axis=0)
# x1 = preprocess_input(x1)

# features1 = model.predict(x1)

# img_path = 'images_vgg16/_531_4975.jpeg'
# img = image.load_img(img_path, target_size=(224, 224))
# x2 = image.img_to_array(img)
# x2 = np.expand_dims(x2, axis=0)
# x2 = preprocess_input(x2)

# features2 = model.predict(x2)

# img_path = 'images_vgg16/_537_5867.jpeg'
# img = image.load_img(img_path, target_size=(224, 224))
# x3 = image.img_to_array(img)
# x3 = np.expand_dims(x3, axis=0)
# x3 = preprocess_input(x3)

# i = 4600

# # Visualize the first layer of convolutions on an input image

# C2 = convout1_f(x2)
# C3 = convout1_f(x3)


# print np.shape(C1)
# C1 = np.squeeze(C1)
# C2 = np.squeeze(C2)
# C3 = np.squeeze(C3)
# print "C1 shape : ", C1.shape

# features3 = model.predict(x3)

# print np.shape(features1)
# print np.shape(features2)
# print np.shape(features3)

# print "closest", 1 - spatial.distance.cosine(features1, features2)
# print "farthest", 1 - spatial.distance.cosine(features1, features3)


# print "closest", 1 - spatial.distance.cosine(C1, C2)
# print "farthest", 1 - spatial.distance.cosine(C1, C3)