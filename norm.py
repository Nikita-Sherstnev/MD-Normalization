from collections import defaultdict

from gensim.models import FastText

from ontology import Ontology


class Normalizer():
    def __init__(self, _cls, onto_path):
        self.cls_name = _cls
        self.model = FastText.load(f'models/{_cls}.model')
        self.onto = Ontology(onto_path)

    def normalize_name(self, name):
        inst_props = name.split(' ')

        instans = self.onto.get_all_instances_of(self.cls_name)

        all_props_names = dict()
        for inst in instans:
            pattern, props = self.onto.get_pattern_and_props(inst)
            all_props_names.update(dict(zip(props.split('+'), pattern.split('+'))))

        inst_props_names = dict()
        topn = 1
        for prop in inst_props:
            prop = str(prop) 
            most_sim = self.model.wv.most_similar(prop, topn=topn)
            inst_props_names[all_props_names[most_sim[0][0]]] = prop

        props = pattern.split('+')
        props.remove('Класс')

        norm_name = self.cls_name
        for prop in props:
            norm_name += ' ' + inst_props_names[prop]

        return norm_name
