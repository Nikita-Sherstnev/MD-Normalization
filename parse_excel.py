import os.path as osp

import pandas as pd
import numpy as np


class ExcelParser():
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def read_names_and_classes(self, filename):
        train_df = self.read_train_set(filename)

        names = train_df['Полное наименование'].tolist()
        names = [s.strip() for s in names]

        classes = train_df['Класс (Наименование)'].tolist()
        classes = [s.strip() for s in classes]

        names_classes = dict(zip(names, classes))

        return names, classes, names_classes

    def read_train_set(self, filename):
        '''
        Returns DataFrame with names and classes. 
        '''
        df = pd.read_excel(osp.join(self.root_dir, filename), index_col=0)
        df = df.loc[df['Пометка удаления/ Признак архивной записи'] == 'Нет']
        df = df.drop(df.columns[[0,1,2,4,5,6,7,8,10,11,12,13,14,15,16,17]], axis=1)
        return df.rename({x:y for x,y in zip(list(df.index.values), range(0, len(list(df.index.values))))})

    def read_patterns(self, filename):
        '''
        Returns dict of classes with pattern and example
        '''
        xls = pd.ExcelFile(osp.join(self.root_dir, filename))
        df = pd.read_excel(xls, None)

        patterns_dict = dict()
        for k, _ in df.items():
            _cls = df[k].iloc[0, 1]
            props_headers = df[k].iloc[5,:6].tolist()
            props = df[k].iloc[6:27,:6]
            pattern = df[k].iloc[28,0]

            props.columns = props_headers

            props = props.dropna(axis=0, thresh=4)
            # .loc[props['Наименование свойства'].notnull()]

            # props['Пример заполнения'] = props[props.columns[3:6]].apply(
            #     lambda x: ' '.join(x.dropna().astype(str)),
            #     axis=1
            # )

            names = props['Наименование свойства'].tolist()
            names = [s.strip() for s in names]

            examples = props['Пример заполнения'].tolist()
            examples = [str(s).strip() for s in examples]

            types = props['Тип значения'].tolist()
            types = [s.strip() for s in types]
            types = '+'.join(types)

            prefixes = props['Префикс'].tolist()
            prefixes = [str(s).strip() for s in prefixes]
            prefixes = '+'.join(prefixes)

            postfixes = props['Постфикс'].tolist()
            postfixes = [str(s).strip() for s in postfixes]
            postfixes = '+'.join(postfixes)

            props_dict = dict(zip(names, examples))

            ord_props = pattern.split('+')
            ord_props.remove('Класс')
            example = _cls
            for prop in ord_props:
                example += '+' + props_dict[prop]

            patterns_dict[_cls] = {
                'pattern': pattern,
                'props': example,
                'types': types,
                'prefixes': prefixes,
                'postfixes': postfixes
            }
            
        return patterns_dict