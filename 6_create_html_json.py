"""
===========================================
6. Create HTML and JSON views for closest matching images
===========================================

"""
import sys
sys.path.append('utils')
import imtools
import pickle
import cPickle
import numpy as np



f = open(sys.argv[1]+'_comparison.pickle', 'r')

#all_dist = pickle.load(f)

all_dist = []
while 1:
    try:
        all_dist.append(pickle.load(f))
    except EOFError:
        break

f.close()
path = sys.argv[1]

html = '<html><head></head><body>'
json = []

#print type(all_dist)
#print np.shape(all_dist)

#print all_dist[0]

#print np.shape(all_dist)
im_list = imtools.get_imlist(path)

for idx,dist in enumerate(all_dist):

    #print np.shape(dist)
#for dist in xrange(0,2000):
    #pass
    #print type(dist)
    print idx
    #print dist
    #print np.shape(dist)
    #print dist
    sort_index = np.argsort(dist)
    top20 = sort_index[0:20]
    #print top20
    #print np.shape(top20)
    json.append({"img":"","similar":[]})
    html+="<p>"+str(idx)+"</p>"

    for idy,image in enumerate(top20):
        print json[idx]['img']
        print image
        if idy == 0:
            json[idx]['img'] = im_list[image];
            continue
        #json.image = m_list[image]
        #json.similar =
        html += '<img src='+ im_list[image]+'>'
        #html += '<p>Score:'+ str(dist[image])+'</p>'
        json[idx]['similar'].append({"img":im_list[image],"pattern": str(dist[image]),"color":""})


    html += '<hr>'
    if idx == 1000:
        break


html += '</body></html>'
print json
f1 = open(sys.argv[1]+'.html', 'wb')
cPickle.dump(html,f1)
f1.close()
