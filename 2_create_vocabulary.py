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

#import PIL.Image
#sys.modules['Image'] = PIL.Image
#import Image

from skimage.feature import daisy
from skimage.color import rgb2gray
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

class vocabulary:
    def __init__(self,img_type,vocab_size=800,feature):
        self.img_type = img_type
        self.vocab_size = vocab_size
        self.feature = feature

if __name__ == '__main__':
    path = sys.argv[1]
    vocab_size = 800
    init_size = vocab_size*3

    print path
    im_list = imtools.get_imlist(path)

    print im_list

    #%%time
    all_features = []
    for idx,image_name in enumerate(im_list):
        gray_img = rgb2gray(np.array(Image.open(image_name)))
        features = daisy(gray_img, step=8)
        print features.shape
        print image_name

        all_features.append(features.reshape(-1, 200))
        print idx
        #print features.reshape(-1, 200)
        # f = open('data/features/'+sys.argv[1]+'_'+os.path.basename(image_name)+'.feature', 'w')
        # pickle.dump(features,f)
        # f.close()



    X = np.vstack(all_features)
    print X.shape

    # f = open('data/features/'+sys.argv[1]+'_all_features.feature', 'w')
    # pickle.dump(all_features,f)
    # f.close()

    #f = open(sys.argv[1]+'_features.pickle', 'w')
    #pickle.dump(km,f)
    #f.close()

    #%%time
    km = MiniBatchKMeans(n_clusters=vocab_size,max_iter=200,verbose=1)
    #km = KMeans(n_clusters=200,n_jobs=-1,verbose=1)
    km.fit(X)


    f = open(sys.argv[1]+'_vocab.pickle', 'w')
    pickle.dump(km,f)
    f.close()

