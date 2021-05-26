import os

from gensim.models import FastText

from parse_excel import ExcelParser
from ontology import Ontology
from fasttext import NamesCorpus


def count_metrics(onto_path, path_to_excel, model_path):
    path, filename = os.path.split(path_to_excel)
    parser = ExcelParser(path)
    names, classes, names_classes = parser.read_names_and_classes(filename)
    corpus = NamesCorpus(path, filename)

    onto = Ontology(onto_path)
    model = FastText.load(model_path)
    wv = model.wv
    topn = 3

    all_names = len(names) - 9
    correct = 0

    for inst, _cls in names_classes.items():
        most_sim = wv.most_similar(inst, topn=topn)

        sim_classes = list()
        for sim in most_sim:
            sim_classes.append(onto.get_class_of_instance(sim[0]))

        set_sim_classes = set(sim_classes)

        classes_count = list()
        for cl in set_sim_classes:
            classes_count.append((cl, sim_classes.count(cl)))

        classes_count = sorted(classes_count, key=lambda x: x[1], reverse=True)

        perc_count = []
        for cl in classes_count:
            perc_count.append((cl[0], (cl[1]/topn)*100))
        
        inst_class = perc_count[0][0]
        
        if inst_class is not None:
            print()
            print(inst)
            print(inst_class.name)
            if inst_class.name == _cls:
                correct+=1

    print('accuracy = ', end='')
    print(correct/all_names)