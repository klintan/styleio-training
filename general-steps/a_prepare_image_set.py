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
import yaml
import skimage
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import logging

logging.basicConfig(level=logging.DEBUG)

#TODO
#Error handling:
#File not found, directory not created
class PrepareImages:
    def __init__(self):
        self.config = yaml.safe_load(open("../config.yml"))['preprocessing']
        self.logger = logging.getLogger(__name__)
        self.path = self.config['path']
        self.experiment_name = self.config['experiment_name']
        self.im_list = imtools.get_imlist(self.config['path'])
        self.all_images_data = []
        self.size = self.config['img_size']
        self.datagen = ImageDataGenerator(
                featurewise_center=True,
                featurewise_std_normalization=False)

    def kerasPrep(self):
        try:
            os.makedirs(self.path+'_processed')
        except Exception as e:
            self.logger.warning('Folder %s already exists', self.path+'_processed' )

        #images is (nb_samples, height, width)
        all_images = np.asarray(self.all_images_data)
        self.logger.info('Start processing images using Keras...')
        for idx, im_name in enumerate(self.im_list):
            self.logger.debug("Processing image %s, %s out of %s ", im_name, idx, len(self.im_list))
            if idx==0:
                img = load_img(im_name, target_size=self.size)  # this is a PIL image
                all_images = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
                all_images = all_images.reshape((1,) + all_images.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
                self.logger.debug('Processing image %s', all_images.shape)
            else:
                img = load_img(im_name, target_size=self.size)  # this is a PIL image
                x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
                x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)
                self.logger.debug('Processing image %s', x.shape)
                all_images = np.concatenate((all_images, x), axis=0)

        self.logger.info('All images done, shape %s', all_images.shape)
        self.datagen.fit(all_images)
        self.logger.info('Datagen fit done')

        #the .flow() command below generates batches of randomly transformed images
        #and saves the results to the `preview/` directory
        i = 0
        for batch in self.datagen.flow(all_images, shuffle=False, batch_size=1,save_to_dir=self.path+'_processed', save_format='jpeg'):
            i += 1
            if i > len(self.im_list):
                break  # otherwise the generator would loop indefinitely


    def imagePrep(self):
        self.logger.info('Start processing images...')
        all_images_data = []
        for idx, im_name in enumerate(self.im_list):
            try:
                im = Image.open(im_name)
            except Exception as e:
                self.logger.error(e)
                continue
            im.thumbnail(self.size, Image.ANTIALIAS)
            im_name_nospaces = im_name.replace(" ","")
            im.save(self.path+'_new/'+os.path.basename(im_name_nospaces))
            print np.shape(np.asarray(im))
            print "image shape", np.shape(im)
            self.logger.debug("Processing image %s, %s out of %s ", im_name, idx, len(self.im_list))
        self.logger.info('Finished processing images')

if __name__ == '__main__':
    prepIm = PrepareImages()
    #prepIm.imagePrep()
    prepIm.kerasPrep()

