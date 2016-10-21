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

f = open(sys.argv[1]+'_histograms.pickle', 'r')
histograms = pickle.load(f)
f.close()

all_scores=[]

f1 = open(sys.argv[1]+'_tfidf.pickle', 'r')
while 1:
    try:
        all_scores.append(pickle.load(f1))
    except EOFError:
        break
f1.close()

#compute new histograms with weights
for idx,hist in enumerate(histograms):
    #normalize the histogram
    #hist = hist/float(sum(hist))

    #TFIDF weighing
    hist = hist*all_scores[idx]


path = sys.argv[1]
im_list = imtools.get_imlist(path)


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

print all_dist
print np.shape(all_dist)
