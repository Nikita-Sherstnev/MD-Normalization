'''
Convenient interface for interacting with ontology.
'''
import types

from owlready2 import World, Thing


class Ontology():
    def __init__(self, path):
        world = World()
        self.path = path
        self.onto = world.get_ontology(path).load()

    def get_all_class_names(self):
        return [str(cl).split('.')[1] for cl in self.onto.classes()]

    def get_class_name(self, cl):
        return str(cl).split('.')[1]

    def get_all_classes(self):
        return [cl for cl in self.onto.classes()]

    def get_all_instances_of(self, _cls):
        return self.onto.get_instances_of(self.get_class_by_name(_cls))

    def get_class_by_name(self, name):
        return eval(f'self.onto.{name}')

    def get_class_of_instance(self, inst_name):
        classes = self.get_all_classes()
        for onto_class in classes:
            instans = self.get_all_instances_of(onto_class.name)
            instans = [inst.name for inst in instans]
            inst_name = inst_name.replace(' ', '_')
            if inst_name in instans:
                return onto_class

        return None

    def create_class(self, name, superclass=None):
        with self.onto:
            if superclass is not None:
                new_class = type(name, (superclass,), {})
            else:
                new_class = type(name, (Thing,), {})

            self.onto.save(file=self.path)

    def create_instance(self, onto_class, inst):
        inst = inst.replace(' ', '_')
        inst = inst.replace('"', "'")
        eval("self.onto." + str(onto_class).split(".")[1] + "(inst)")
        self.onto.save(file=self.path)

    def create_many_classes(self, names: list, superclass=None):
        with self.onto:
            for name in names:
                if superclass is not None:
                    new_class = type(name.strip(), (superclass,), {})
                else:
                    new_class = type(name.strip(), (Thing,), {})

            self.onto.save(file=self.path)

    def create_many_instances(self, names_classes: dict):
        with self.onto:
            for inst, onto_class in names_classes.items():
                inst = inst.replace(' ', '_')
                inst = inst.replace('"', "'")
                onto_class = self.get_class_by_name(onto_class)
                onto_class(inst)

        self.onto.save(file=self.path)

    