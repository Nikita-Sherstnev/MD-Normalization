from collections import defaultdict

from gensim.models import FastText
import nltk

from ontology import Ontology


class Normalizer():
    def __init__(self, _cls, onto_path):
        self.cls_name = _cls
        self.model = FastText.load(f'models/{_cls}.model')
        self.onto = Ontology(onto_path)

    def normalize_name(self, name):
        print('name:')
        print(name)
        inst_props = nltk.word_tokenize(name, language="russian")
        print(inst_props)

        instans = self.onto.get_all_instances_of(self.cls_name)

        all_props_names = dict()
        for inst in instans:
            pattern, props = self.onto.get_pattern_and_props(inst)
            all_props_names.update(dict(zip(props.split('+'), pattern.split('+'))))

        inst_props_names = defaultdict(lambda: '&None')
        topn = 1
        for prop in inst_props:
            prop = str(prop) 
            most_sim = self.model.wv.most_similar(prop, topn=topn)
            inst_props_names[all_props_names[most_sim[0][0]]] = prop

        props = pattern.split('+')
        props.remove('Класс')
        print('props names:')
        print(inst_props_names)

        norm_name = self.cls_name
        for prop in props:
            norm_name += ' ' + inst_props_names[prop]
        
        print('norm_name')
        print(norm_name)

        return norm_name
