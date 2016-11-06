from vgg16 import VGG16
from keras.preprocessing import image
from imagenet_utils import preprocess_input
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import theano
from keras import backend as K

from scipy import spatial

model = VGG16(weights='imagenet', include_top=True)
# model.add(Flatten())
# model.compile()
inputs = [K.learning_phase()] + model.inputs
_convout1_f = K.function(inputs, [model.layers[21].output])
def convout1_f(X):
    # The [0] is to disable the training phase flag
    return _convout1_f([0] + [X])

img_path = 'images_vgg16/_530_4198.jpeg'
img = image.load_img(img_path, target_size=(224, 224))
x1 = image.img_to_array(img)
x1 = np.expand_dims(x1, axis=0)
x1 = preprocess_input(x1)

features1 = model.predict(x1)

img_path = 'images_vgg16/_531_4975.jpeg'
img = image.load_img(img_path, target_size=(224, 224))
x2 = image.img_to_array(img)
x2 = np.expand_dims(x2, axis=0)
x2 = preprocess_input(x2)

features2 = model.predict(x2)

img_path = 'images_vgg16/_537_5867.jpeg'
img = image.load_img(img_path, target_size=(224, 224))
x3 = image.img_to_array(img)
x3 = np.expand_dims(x3, axis=0)
x3 = preprocess_input(x3)

i = 4600

# Visualize the first layer of convolutions on an input image
C1 = convout1_f(x1)
C2 = convout1_f(x2)
C3 = convout1_f(x3)


print np.shape(C1)
C1 = np.squeeze(C1)
C2 = np.squeeze(C2)
C3 = np.squeeze(C3)
print "C1 shape : ", C1.shape

features3 = model.predict(x3)

print np.shape(features1)
print np.shape(features2)
print np.shape(features3)

print "closest", 1 - spatial.distance.cosine(features1, features2)
print "farthest", 1 - spatial.distance.cosine(features1, features3)


print "closest", 1 - spatial.distance.cosine(C1, C2)
print "farthest", 1 - spatial.distance.cosine(C1, C3)