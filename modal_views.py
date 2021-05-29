from norm import Normalizer
from typing import Text
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from plyer import filechooser
from kivy.uix.popup import Popup
import threading

from fasttext import new_model, update_model, define_class
from ontology import Ontology


def to_rbga(rbga):
    return (rbga[0]/255.0, rbga[1]/255.0, rbga[2]/255.0, rbga[3])


class NewModelView(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(NewModelView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Обучение новой модели', pos=(0, 170), font_size=20))
        load_train_set_btn = Button(text='Открыть файл с выборкой', size_hint=(.25, .14), pos=(20, 280), background_color=to_rbga((100, 57, 43, 1)))
        load_train_set_btn.bind(on_press=self.show_load_train_set)
        load_patterns_btn = Button(text='Открыть шаблоны для обучения', size_hint=(.25, .14), pos=(20, 210), background_color=to_rbga((100, 57, 43, 1)))
        load_patterns_btn.bind(on_press=self.show_load_patterns)
        load_onto_btn = Button(text='Открыть онтологию', size_hint=(.25, .14), pos=(20, 140), background_color=to_rbga((100, 57, 43, 1)))
        load_onto_btn.bind(on_press=self.show_load_onto)
        save_model_btn = Button(text='Путь к новой модели', size_hint=(.25, .14), pos=(20, 70), background_color=to_rbga((100, 57, 43, 1)))
        save_model_btn.bind(on_press=self.show_save_model)

        start_train_btn = Button(text='Начать обучение', size_hint=(.25, .1), pos=(240, 20), background_color=to_rbga((60, 179, 113, 1)))
        start_train_btn.bind(on_press=self.train_new_model)

        self.add_widget(load_train_set_btn)
        self.add_widget(load_patterns_btn)
        self.add_widget(load_onto_btn)
        self.add_widget(save_model_btn)
        self.add_widget(start_train_btn)

        self.train_set_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 290))
        self.patterns_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 220))
        self.onto_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 150))
        self.model_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 80))

        self.add_widget(self.train_set_path)
        self.add_widget(self.patterns_path)
        self.add_widget(self.onto_path)
        self.add_widget(self.model_path)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def show_load_train_set(self, widget):
        train_set_path = filechooser.open_file(title="Выберите файл с обучающей выборкой", 
                                    filters=[("*.xlsx")])
        if train_set_path:
            self.train_set_path.text = train_set_path[0]

    def show_load_patterns(self, widget):
        patterns_path = filechooser.open_file(title="Выберите файл с шаблонами", 
                                    filters=[("*.xlsx")])

        if patterns_path:
            self.patterns_path.text = patterns_path[0]

    def show_load_onto(self, widget):
        onto_path = filechooser.open_file(title="Выберите файл онтологии", 
                                    filters=[("*.owl")])
        if onto_path:
            self.onto_path.text = onto_path[0]

    def show_save_model(self, widget):
        model_path = filechooser.save_file(title="Куда сохранить новую модель",
                                            filters=[("*.model")])

        if model_path:
            self.model_path.text = model_path[0]

    def train_new_model(self, widget):
        if self.onto_path.text and self.train_set_path.text and \
            self.model_path.text and self.patterns_path.text:
                popup_process = Popup(title='',
                        content=Label(text='Идет обучение...', font_size=25),
                        size_hint=(None, None), size=(300, 250), auto_dismiss=False)
                popup_process.open()
                
                threading.Thread(target=self.start_train, args=(popup_process,), daemon=True).start()
        else:
            popup = Popup(title='',
                content=Label(text='Заполните все поля!', font_size=25),
                size_hint=(None, None), size=(300, 250))
            popup.open()
            
    def start_train(self, popup_process):
        new_model(self.onto_path.text, self.train_set_path.text,
                    self.model_path.text, self.patterns_path.text)
        popup_process.dismiss()
        popup = Popup(title='',
            content=Label(text='Обучение прошло успешно!', font_size=25),
            size_hint=(None, None), size=(300, 250))
        popup.open()


class UpdateModelView(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(UpdateModelView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Продолжить обучение модели', pos=(0, 170), font_size=20))
        load_train_set_btn = Button(text='Открыть файл с выборкой', size_hint=(.25, .14), pos=(20, 280), background_color=to_rbga((100, 57, 43, 1)))
        load_train_set_btn.bind(on_press=self.show_load_train_set)
        load_patterns_btn = Button(text='Открыть шаблоны для обучения', size_hint=(.25, .14), pos=(20, 210), background_color=to_rbga((100, 57, 43, 1)))
        load_patterns_btn.bind(on_press=self.show_load_patterns)
        load_onto_btn = Button(text='Открыть онтологию', size_hint=(.25, .14), pos=(20, 140), background_color=to_rbga((100, 57, 43, 1)))
        load_onto_btn.bind(on_press=self.show_load_onto)
        save_model_btn = Button(text='Загрузить модель', size_hint=(.25, .14), pos=(20, 70), background_color=to_rbga((100, 57, 43, 1)))
        save_model_btn.bind(on_press=self.show_save_model)

        start_train_btn = Button(text='Продолжить обучение', size_hint=(.25, .1), pos=(240, 20), background_color=to_rbga((60, 179, 113, 1)))
        start_train_btn.bind(on_press=self.update_model)

        self.add_widget(load_train_set_btn)
        self.add_widget(load_patterns_btn)
        self.add_widget(load_onto_btn)
        self.add_widget(save_model_btn)
        self.add_widget(start_train_btn)

        self.train_set_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 290))
        self.patterns_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 220))
        self.onto_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 150))
        self.model_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 80))

        self.add_widget(self.train_set_path)
        self.add_widget(self.patterns_path)
        self.add_widget(self.onto_path)
        self.add_widget(self.model_path)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def show_load_train_set(self, widget):
        train_set_path = filechooser.open_file(title="Выберите файл с обучающей выборкой", 
                                    filters=[("*.xlsx")])
        if train_set_path:
            self.train_set_path.text = train_set_path[0]

    def show_load_patterns(self, widget):
        patterns_path = filechooser.open_file(title="Выберите файл с шаблонами", 
                                    filters=[("*.xlsx")])

        if patterns_path:
            self.patterns_path.text = patterns_path[0]

    def show_load_onto(self, widget):
        onto_path = filechooser.open_file(title="Выберите файл онтологии", 
                                    filters=[("*.owl")])
        if onto_path:
            self.onto_path.text = onto_path[0]

    def show_save_model(self, widget):
        model_path = filechooser.open_file(title="Выберите файл модели",
                                            filters=[("*.model")])

        if model_path:
            self.model_path.text = model_path[0]

    def update_model(self, widget):
        if self.onto_path.text and self.train_set_path.text and \
            self.model_path.text and self.patterns_path.text:
                popup_process = Popup(title='',
                        content=Label(text='Идет обучение...', font_size=25),
                        size_hint=(None, None), size=(300, 250), auto_dismiss=False)
                popup_process.open()
                
                threading.Thread(target=self.start_train, args=(popup_process,), daemon=True).start()
        else:
            popup = Popup(title='',
                content=Label(text='Заполните все поля!', font_size=25),
                size_hint=(None, None), size=(300, 250))
            popup.open()
            
    def start_train(self, popup_process):
        update_model(self.onto_path.text, self.train_set_path.text,
                    self.model_path.text, self.patterns_path.text)
        popup_process.dismiss()
        popup = Popup(title='',
            content=Label(text='Обучение прошло успешно!', font_size=25),
            size_hint=(None, None), size=(300, 250))
        popup.open()


class ClassifyView(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(ClassifyView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Классифицировать новую позицию', pos=(0, 170), font_size=20))
        load_train_set_btn = Button(text='Открыть онтологию', size_hint=(.25, .14), pos=(20, 280), background_color=to_rbga((100, 57, 43, 1)))
        load_train_set_btn.bind(on_press=self.show_load_onto)
        load_patterns_btn = Button(text='Загрузить модель', size_hint=(.25, .14), pos=(20, 210), background_color=to_rbga((100, 57, 43, 1)))
        load_patterns_btn.bind(on_press=self.show_load_model)

        start_train_btn = Button(text='Определить класс', size_hint=(.25, .1), pos=(240, 20), background_color=to_rbga((60, 179, 113, 1)))
        start_train_btn.bind(on_press=self.define_class)

        self.add_widget(load_train_set_btn)
        self.add_widget(load_patterns_btn)
        self.add_widget(start_train_btn)
        
        self.onto_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 290))
        self.model_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 220))
        self.add_widget(Label(text='Введите новую позицию', pos=(0, -10), font_size=15))
        self.inst = TextInput(multiline=False, size_hint=(.7, .1), pos=(100, 130))

        self.add_widget(self.inst)
        self.add_widget(self.onto_path)
        self.add_widget(self.model_path)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def show_load_onto(self, widget):
        onto_path = filechooser.open_file(title="Выберите файл онтологии", 
                                    filters=[("*.owl")])
        if onto_path:
            self.onto_path.text = onto_path[0]

    def show_load_model(self, widget):
        model_path = filechooser.open_file(title="Выберите файл модели",
                                            filters=[("*.model")])

        if model_path:
            self.model_path.text = model_path[0]
    
    def define_class(self, widget):
        if self.onto_path.text and \
            self.model_path.text and self.inst.text:
            predictions = define_class(self.onto_path.text, self.inst.text, self.model_path.text)
            view = ClassifyResultView(auto_dismiss=False, preds=predictions, inst=self.inst.text, onto_path=self.onto_path.text)
            view.open()
        else:
            popup = Popup(title='',
                content=Label(text='Заполните все поля!', font_size=25),
                size_hint=(None, None), size=(300, 250))
            popup.open()


class ClassifyResultView(FloatLayout, ModalView):
    def __init__(self, preds, inst, onto_path, **kwargs):
        super(ClassifyResultView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.pred = preds[0]
        self.inst = inst
        self.onto = Ontology(onto_path)

        self.add_widget(Label(text='Определение класса', pos=(0, 170), font_size=20))
        self.add_widget(Label(text='Предполагаемый класс:', pos=(-160, 100), font_size=18))
        self.add_widget(Label(text=str(self.pred[0]).split('.')[1] + ": " + str(self.pred[1]) + "%", pos=(-160, 70), font_size=18))

        write_btn = Button(text='Записать позицию', size_hint=(.3, .15), pos=(300, 250), background_color=to_rbga((60, 179, 113, 1)))
        self.add_widget(write_btn)
        write_btn.bind(on_press=self.write_inst)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def write_inst(self, widget):
        self.onto.create_instance(self.pred[0], self.inst)
        self.dismiss()
        popup = Popup(title='',
            content=Label(text='Успешно записано!', font_size=25),
            size_hint=(None, None), size=(300, 250))
        popup.open()


class NormView(FloatLayout, ModalView):
    CLASS = 'Бумага'

    def __init__(self, **kwargs):
        super(NormView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Нормализация позиции', pos=(0, 170), font_size=20))

        load_onto_btn = Button(text='Открыть онтологию', size_hint=(.25, .14), pos=(20, 280), background_color=to_rbga((100, 57, 43, 1)))
        load_onto_btn.bind(on_press=self.show_load_onto)
        self.onto_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 290))

        self.add_widget(Label(text='Введите позицию для нормализации', pos=(0, -10), font_size=15))
        self.inst = TextInput(multiline=False, size_hint=(.7, .1), pos=(100, 130))

        norm_btn = Button(text='Нормализовать', size_hint=(.25, .1), pos=(240, 20), background_color=to_rbga((60, 179, 113, 1)))
        norm_btn.bind(on_press=self.normalize)

        self.add_widget(self.onto_path)
        self.add_widget(self.inst)
        self.add_widget(norm_btn)
        self.add_widget(load_onto_btn)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def show_load_onto(self, widget):
        onto_path = filechooser.open_file(title="Выберите файл онтологии", 
                                    filters=[("*.owl")])
        if onto_path:
            self.onto_path.text = onto_path[0]

    def normalize(self, widget):
        if self.onto_path.text and self.inst.text:
            norm = Normalizer(self.CLASS, self.onto_path.text)
            norm_name = norm.normalize_name(self.inst.text)

            view = NormResultView(auto_dismiss=False, norm_name=norm_name, onto_path=self.onto_path.text, _cls=self.CLASS)
            view.open()
        else:
            popup = Popup(title='',
                content=Label(text='Заполните все поля!', font_size=25),
                size_hint=(None, None), size=(300, 250))
            popup.open()


class NormResultView(FloatLayout, ModalView):
    def __init__(self, norm_name, onto_path, _cls, **kwargs):
        super(NormResultView, self).__init__(**kwargs)
        self.size = (600, 400)
        self._cls = _cls
        self.norm_name = norm_name
        self.onto = Ontology(onto_path)

        self.add_widget(Label(text='Нормализация', pos=(0, 170), font_size=20))
        self.add_widget(Label(text='Нормализованная позиция:', pos=(0, 100), font_size=18))
        self.add_widget(Label(text=self.norm_name, pos=(0, 70), font_size=18))

        write_btn = Button(text='Записать позицию', size_hint=(.3, .15), pos=(200, 150), background_color=to_rbga((60, 179, 113, 1)))
        self.add_widget(write_btn)
        write_btn.bind(on_press=self.write_inst)

        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def write_inst(self, widget):
        self.onto.create_instance(self._cls, self.norm_name)
        self.dismiss()
        popup = Popup(title='',
            content=Label(text='Успешно записано!', font_size=25),
            size_hint=(None, None), size=(300, 250))
        popup.open()