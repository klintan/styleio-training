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
from jinja2 import Template, Environment, PackageLoader, FileSystemLoader
import logging
import yaml
import os

logging.basicConfig(level=logging.INFO)

class EvaluationFramework():
    def __init__(self):
        self.config = yaml.safe_load(open("../config.yml"))['html']
        self.path = self.config['path']
        self.histograms = None
        self.im_list = imtools.get_imlist(self.config['path'])
        self.all_scores=[]
        self.logger = logging.getLogger(__name__)
        self.html= None
        self.all_dist = []
        self.all_data = []
        #jinja 2
        template_dir = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(template_dir + "/templates"),trim_blocks=True)
        self.template = env.get_template('annotate.html')
        self.load_comparison()


    def load_comparison(self):
        self.logger.info('Loading comparison scores...')
        f = open(self.path+'_comparison.pickle', 'r')
        while 1:
            try:
                self.all_dist.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        self.logger.info('Succesfully loaded comparison scores')

    def generate_html(self):
        self.logger.info('Generate HTML...')
        json = []
        for idx,dist in enumerate(self.all_dist):
            sort_index = np.argsort(dist)
            top20 = sort_index[0:20]
            json.append({"img":"","similar":[]})
            img_index = str(idx)
            img_row = []
            for idy,image in enumerate(top20):
                if idy == 0:
                    json[idx]['img'] = self.im_list[image];
                    continue

                img_path = os.path.normpath(self.im_list[image])
                img_source = "/".join(img_path.split(os.sep)[-2:])
                img_row.append({"src":img_source, "score":str(dist[image])})

                #self.html += '<img src='+ self.im_list[image]+' width="'+str(100)+'" height="'+str(100)+'">'
                #img_source = self.im_list[image]
                #self.html += '<p>Score:'+ str(dist[image])+'</p>'
                #json[idx]['similar'].append({"img":self.im_list[image],"pattern": str(dist[image]),"color":""})

            self.all_data.append(img_row)
            if idx == 500:
                break

        self.render_html()

    def save_html(self):
        with open(self.path+'.html', 'wb') as f1:
            cPickle.dump(self.html, f1)

    def render_html(self):
        # jinja2
        with open(self.path+'_jinja.html', 'wb') as f2:
            cPickle.dump(self.template.render(all_images=self.all_data).encode( "utf-8" ) ,f2)

if __name__ == '__main__':
    ef = EvaluationFramework()
    ef.generate_html()