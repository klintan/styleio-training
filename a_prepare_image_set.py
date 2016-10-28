"""
===========================================
1. Prepare image set
===========================================
Make sure all image are same width and height (keep aspect ratio)

"""
import numpy as np
import sys
from PIL import Image
import sys
sys.path.append('utils')
import imtools
import os

import skimage
from keras.preprocessing.image import ImageDataGenerator

import logging

logging.basicConfig(level=logging.DEBUG)

#TODO
#Error handling:
#File not found, directory not created
class PrepareImages:
    def __init__(self, path, size=[200,200]):
        self.logger = logging.getLogger(__name__)
        self.path = path
        self.im_list = imtools.get_imlist(path)
        self.all_images_data = []
        self.size = size#200,200
        self.datagen = ImageDataGenerator(
                featurewise_center=True,
                featurewise_std_normalization=True)

    def kerasPreprocessing(self):
        #os.makedirs('images')
        #images is (nb_samples, height, width)
        self.datagen.fit(self.all_images_data)
        # for X_batch, y_batch in datagen.flow(X_train, y_train, batch_size=9, save_to_dir='images', save_prefix='aug', save_format='png'):
        #     # create a grid of 3x3 images
        #     for i in range(0, 9):
        #         pyplot.subplot(330 + 1 + i)
        #         pyplot.imshow(X_batch[i].reshape(28, 28), cmap=pyplot.get_cmap('gray'))
        #     # show the plot
        #     pyplot.show()
        #     break

    def imagePrep(self, keras=False):
        self.logger.info('Start processing images...')
        all_images_data = []
        for idx, im_name in enumerate(self.im_list):
            try:
                im = Image.open(im_name)
                im = skimage.io.imread()
            except Exception as e:
                self.logger.error(e)
                continue
            im.thumbnail(self.size, Image.ANTIALIAS)
            im_name_nospaces = im_name.replace(" ","")
            if keras:
                self.all_images_data.append((im_name,im))
            else:
                im.save(self.path+'_new/'+os.path.basename(im_name_nospaces))
            print np.shape(np.asarray(im))
            print "image shape", np.shape(im)
            self.logger.debug("Processing image %s, %s out of %s ", im_name, idx, len(self.im_list))
        if keras:
            prepIm.kerasPreprocessing()
        self.logger.info('Finished processing images')

if __name__ == '__main__':
    prepIm = PrepareImages(sys.argv[1])
    prepIm.imagePrep(keras=True)
