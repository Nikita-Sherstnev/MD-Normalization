import os

from gensim.models import FastText

from parse_excel import ExcelParser
from ontology import Ontology
from norm import Normalizer


class NamesCorpus:
    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename 

    def __iter__(self):
        parser = ExcelParser(self.dir)
        train_df = parser.read_train_set(self.filename)
        names = train_df['Полное наименование'].tolist()
        yield list(names)


class PropsCorpus:
    def __init__(self, dir, names):
        self.dir = dir
        self.names = names 

    def __iter__(self):
        yield list(self.names)


def train_new(corpus, corpus_len):
    model = FastText(vector_size=32, window=3, min_count=1, min_n=4)
    model.build_vocab(corpus_iterable=corpus)
    model.train(corpus_iterable=corpus, total_examples=corpus_len, epochs=10)
    return model


def train_update(model, corpus, corpus_len):
    model.build_vocab(corpus_iterable=corpus, update=True)
    model.train(corpus_iterable=corpus, total_examples=corpus_len, epochs=model.epochs)

    return model


def new_model(onto_path, path_to_excel, model_path, props_path):
    onto = Ontology(onto_path)

    path, filename = os.path.split(path_to_excel)
    parser = ExcelParser(path)
    names, classes, names_classes = parser.read_names_and_classes(filename)

    corpus = NamesCorpus(path, filename)
    model = train_new(corpus, len(names))
    model.save(model_path)

    onto.create_many_classes(list(set(classes)))
    
    train_patterns(onto, props_path)

    onto.create_many_instances(names_classes)


def names_normalization(classes, names_classes, onto_path):
    norm_names_classes = dict()
    for _cls in classes:
        normalizer = Normalizer(_cls, onto_path)
        for name, value in names_classes.items():
            if value == _cls:
                norm_name = normalizer.normalize_name(name)
                norm_names_classes[norm_name] = _cls

    return norm_names_classes


def train_patterns(onto, props_path):
    path, filename = os.path.split(props_path)
    parser = ExcelParser(path)
    props = parser.read_patterns(filename)
    
    for _cls in props:
        names = props[_cls]['props'].split('+')

        inst_name = ' '.join(names)
        cls_name = onto.get_class_by_name(_cls)
        if cls_name is not None:
            inst = onto.create_instance(onto.get_class_by_name(_cls), inst_name) 
            onto.set_pattern_and_props(inst, props[_cls]['pattern'], props[_cls]['props'])
            onto.set_prefixes_and_postfixes(inst, props[_cls]['prefixes'], props[_cls]['postfixes'])
            onto.set_types(inst, props[_cls]['types'])


def update_model(onto_path, path_to_excel, model_path, props_path):
    path, filename = os.path.split(path_to_excel)
    parser = ExcelParser(path)
    names, classes, names_classes = parser.read_names_and_classes(filename)
    corpus = NamesCorpus(path, filename)

    model = FastText.load(model_path)
    model = train_update(model, corpus, len(names))
    model.save(model_path)

    onto = Ontology(onto_path)

    train_patterns(onto, props_path)

    onto.create_many_classes(list(set(classes)))
    onto.create_many_instances(names_classes)


def define_class(onto_path, inst, model_path):
    onto = Ontology(onto_path)
    model = FastText.load(model_path)
    wv = model.wv
    topn = 5
    most_sim = wv.most_similar(inst, topn=topn)
    print(most_sim)
    sim_classes = list()
    for sim in most_sim:
        sim_classes.append(onto.get_class_of_instance(sim[0]))

    sim_classes = list(filter(None, sim_classes))
    set_sim_classes = set(sim_classes)

    classes_count = list()
    for cl in set_sim_classes:
        classes_count.append((cl, sim_classes.count(cl)))

    classes_count = sorted(classes_count, key=lambda x: x[1], reverse=True)
    print(classes_count)
    perc_count = []
    for cl in classes_count:
        perc_count.append((cl[0], int((cl[1]/len(sim_classes))*100)))

    inst_class = perc_count[0][0]
    print('Предполагаемый класс: ', inst_class)

    return perc_count
