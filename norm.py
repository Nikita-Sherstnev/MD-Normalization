from ontology import Ontology


class Normalizer():
    def __init__(self, _cls, onto_path):
        self.cls_name = _cls
        self.onto = Ontology(onto_path)

    def normalize_name(self, name):
        instans = self.onto.get_all_instances_of(self.cls_name)
        inst = instans[0]

        for inst in instans:
            pattern, props = self.onto.get_pattern_and_props(inst)
            prefixes, postfixes = self.onto.get_prefixes_and_postfixes(inst)
            types = self.onto.get_types(inst)

            if pattern and props and prefixes and postfixes and types:
                break

        pattern = pattern.split('+')
        pattern.remove('Класс')

        props = props.split('+')
        props.remove(self.cls_name)

        all_props_data = dict()
        all_props_data = dict(zip(pattern, zip(props, prefixes.split('+'), postfixes.split('+'), types.split('+'))))

        inst_props_names = dict()

        # remove class from name
        _cls = name.split(' ')[0]
        if self.cls_name == _cls:
            name = name[len(_cls):].strip()

        for prop_name, props in all_props_data.items():
            if props[1] != 'nan':
                pos = name.find(props[1])
                prop = name[pos+len(props[1])+1:].split(' ')[0]
                name = name[:pos] + name[pos+len(props[1])+len(prop)+1:].strip()
                
                inst_props_names[prop_name] = prop
            
            if props[2] != 'nan':
                pos = name.find(props[2])
                cur_pos = pos-1
                prop = ''
                while name[cur_pos].isdigit():
                    prop += name[cur_pos]
                    cur_pos-=1

                prop = prop[::-1]
                if pos+2 < len(name):
                    if name[pos+2] == ',' or name[pos+2] == ' ':
                        name = name[:cur_pos] + name[pos+2:]
                    else:
                        name = name[:cur_pos] + name[pos+1:]
                else:
                    name = name[:cur_pos] + name[pos+1:]
                inst_props_names[prop_name] = prop

            pos = name.find('А')
            if  pos != -1:
                prop = name[pos:pos+2]
                name = name[:pos] + name[pos+2:]
                inst_props_names['Формат'] = prop

        inst_props_names['Название'] = name.split(',')[0].strip()

        norm_name = self.cls_name
        for prop in pattern:
            prefix = all_props_data[prop][1]
            postfix = all_props_data[prop][2]
            prefix = '' if prefix == 'nan' else prefix + ' '
            postfix = '' if postfix == 'nan' else postfix
            norm_name += ' ' + prefix + inst_props_names[prop] + postfix

        return norm_name
