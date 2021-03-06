'''
Convenient interface for interacting with ontology.
'''
from owlready2 import World, Thing, DataProperty, FunctionalProperty


class Ontology():
    def __init__(self, path):
        world = World()
        self.path = path
        self.onto = world.get_ontology(path).load()

        with self.onto:
            class pattern(DataProperty, FunctionalProperty):
                domain = [Thing]
                range = [str]

            class props(DataProperty, FunctionalProperty): 
                domain = [Thing]
                range = [str]

            class types(DataProperty, FunctionalProperty):
                domain = [Thing]
                range = [str]

            class prefixes(DataProperty, FunctionalProperty):
                domain = [Thing]
                range = [str]

            class postfixes(DataProperty, FunctionalProperty):
                domain = [Thing]
                range = [str]
    
    def reload(self):
        world = World()
        self.onto = world.get_ontology(self.path).load()

    def get_all_class_names(self):
        return [str(cl).split('.')[1] for cl in self.onto.classes()]

    def get_class_name(self, cl):
        return str(cl).split('.')[1]

    def get_all_classes(self):
        return [cl for cl in self.onto.classes()]

    def get_all_instances_of(self, _cls):
        return self.onto.get_instances_of(self.get_class_by_name(_cls))

    def get_class_by_name(self, name):
        name = name.replace(' ', '_')
        return eval(f'self.onto.{name}')

    def get_inst_by_name(self, inst_name):
        classes = self.get_all_classes()
        for onto_class in classes:
            instans = self.get_all_instances_of(onto_class.name)
            inst_name = inst_name.replace(' ', '_')
            inst_name = inst_name.replace('"', "'")
            for name in instans:
                if inst_name == name.name:
                    return name

    def get_class_of_instance(self, inst_name):
        classes = self.get_all_classes()
        for onto_class in classes:
            instans = self.get_all_instances_of(onto_class.name)
            instans = [inst.name for inst in instans]
            inst_name = inst_name.replace(' ', '_')
            inst_name = inst_name.replace('"', "'")
            if inst_name in instans:
                return onto_class

        return None

    def create_class(self, name, superclass=None):
        name = name.replace(' ', '_')
        with self.onto:
            if superclass is not None:
                new_class = type(name, (superclass,), {})
            else:
                new_class = type(name, (Thing,), {})

            self.onto.save(file=self.path)

    def create_instance(self, onto_class, inst):
        inst = inst.replace(' ', '_')
        inst = inst.replace('"', "'")
        if str(onto_class).find('.') == -1:
            inst = eval("self.onto." + onto_class + "(inst)")
        else:
            inst = eval("self.onto." + str(onto_class).split(".")[1] + "(inst)")
        self.onto.save(file=self.path)
        return inst

    def create_many_classes(self, names: list, superclass=None):
        with self.onto:
            for name in names:
                name = name.replace(' ', '_')
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

    def create_property(self, prop, _cls, _type):
        with self.onto:
            exec(f'class {prop}(self.onto.{_cls.name} >> {_type}): pass')

        self.onto.save(file=self.path)

    def set_property(self, inst, prop, value):
        setattr(inst, prop, [value])

        self.onto.save(file=self.path)

    def set_pattern_and_props(self, inst, pattern, props):
        inst.pattern = pattern
        inst.props = props

        self.onto.save(file=self.path)
    
    def set_prefixes_and_postfixes(self, inst, prefixes, postfixes):
        inst.prefixes = prefixes
        inst.postfixes = postfixes

        self.onto.save(file=self.path)
    
    def set_types(self, inst, types):
        inst.types = types

        self.onto.save(file=self.path)

    def get_pattern_and_props(self, inst):
        return inst.pattern, inst.props

    def get_prefixes_and_postfixes(self, inst):
        return inst.prefixes, inst.postfixes

    def get_types(self, inst):
        return inst.types
