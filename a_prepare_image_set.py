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
import logging

#logging.basicConfig(level=logging.INFO)

#TODO
#Error handling:
#File not found, directory not created
class PrepareImages:
    def __init__(self, path, size=[200,200]):
        self.logger = logging.getLogger(__name__)
        self.path = path
        self.im_list = imtools.get_imlist(path)
        self.size = size#200,200

    def imagePrep(self):
        self.logger.info('Start processing images...')

        for idx, im_name in enumerate(self.im_list):
            try:
                im = Image.open(im_name)
            except Exception as e:
                self.logger.error(e)
                continue
            im.thumbnail(self.size, Image.ANTIALIAS)
            im_name_nospaces = im_name.replace(" ","")
            im.save(self.path+'_new/'+os.path.basename(im_name_nospaces))
            self.logger.debug("Processing image %s, %s out of %s ", im_name, idx, len(self.im_list))
        self.logger.info('Finished processing images')

if __name__ == '__main__':
    prepIm = prepareImages(sys.argv[1])
    prepIm.imagePrep()