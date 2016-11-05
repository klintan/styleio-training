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
from jinja2 import Template, Environment, PackageLoader
import logging

logging.basicConfig(level=logging.INFO)

class EvaluationFramework():
    def __init__(self, path):
        self.path = path
        self.histograms = None
        self.im_list = imtools.get_imlist(path)
        self.all_scores=[]
        self.logger = logging.getLogger(__name__)
        self.html= None
        self.all_dist = []

        #jinja 2
        self.template = None
        #self.env = Environment(loader=PackageLoader('yourapplication', 'templates'))
        self.load_comparison()


    def load_comparison(self):
        self.logger.info('Loading comparison scores...')
        f = open(self.path+'_comparison.pickle', 'r')
        #all_dist = pickle.load(f)
        while 1:
            try:
                self.all_dist.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        self.logger.info('Succesfully loaded comparison scores')

    def generate_html(self):
        #jinja 2
        # template = env.get_template('layout.html')
        # self.template = Template('Hello {{ name }}!')
        # template.render(name='John Doe')
        # old
        self.logger.info('Generate HTML...')
        self.html = '<html><head></head><body>'
        json = []
        for idx,dist in enumerate(self.all_dist):
            sort_index = np.argsort(dist)
            top20 = sort_index[0:20]
            json.append({"img":"","similar":[]})
            img_index = str(idx)
            self.html+="<p>"+str(idx)+"</p>"
            for idy,image in enumerate(top20):

                if idy == 0:
                    json[idx]['img'] = self.im_list[image];
                    continue

                self.html += '<img src='+ self.im_list[image]+'>'
                img_source = self.im_list[image]
                #self.html += '<p>Score:'+ str(dist[image])+'</p>'
                json[idx]['similar'].append({"img":self.im_list[image],"pattern": str(dist[image]),"color":""})

            self.html += '<hr>'
            if idx == 1000:
                break
        self.html += '</body></html>'
        self.save_html()

    def save_html(self):
        f1 = open(self.path+'.html', 'wb')
        cPickle.dump(self.html,f1)
        f1.close()
        # jinja2
        #self.template.render(the='variables', go='here')



if __name__ == '__main__':
    ef = EvaluationFramework(path=sys.argv[1])
    ef.generate_html()