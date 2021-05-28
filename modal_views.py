from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from plyer import filechooser
from kivy.uix.popup import Popup

from fasttext import new_model


def to_rbga(rbga):
    return (rbga[0]/255.0, rbga[1]/255.0, rbga[2]/255.0, rbga[3])


class NewModelView(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(NewModelView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Обучение новой модели', pos=(0, 150)))
        load_train_set_btn = Button(text='Открыть файл с выборкой', size_hint=(.25, .15), pos=(20, 270), background_color=to_rbga((100, 57, 43, 1)))
        load_train_set_btn.bind(on_press=self.show_load_train_set)
        load_patterns_btn = Button(text='Открыть шаблоны для обучения', size_hint=(.25, .15), pos=(20, 200), background_color=to_rbga((100, 57, 43, 1)))
        load_patterns_btn.bind(on_press=self.show_load_patterns)
        load_onto_btn = Button(text='Открыть онтологию', size_hint=(.25, .15), pos=(20, 130), background_color=to_rbga((100, 57, 43, 1)))
        load_onto_btn.bind(on_press=self.show_load_onto)
        save_model_btn = Button(text='Путь к новой модели', size_hint=(.25, .15), pos=(20, 70), background_color=to_rbga((100, 57, 43, 1)))
        save_model_btn.bind(on_press=self.show_save_model)

        start_train_btn = Button(text='Начать обучение', size_hint=(.25, .15), pos=(200, 20), background_color=to_rbga((100, 57, 43, 1)))
        start_train_btn.bind(on_press=self.train_new_model)

        self.add_widget(load_train_set_btn)
        self.add_widget(load_patterns_btn)
        self.add_widget(load_onto_btn)
        self.add_widget(save_model_btn)
        self.add_widget(start_train_btn)

        self.train_set_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 280))
        self.patterns_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 210))
        self.onto_path = TextInput(multiline=False, size_hint=(.6, .1), pos=(200, 140))
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
                self.start_train()
        else:
            popup = Popup(title='',
                content=Label(text='Заполните все поля!', font_size=25),
                size_hint=(None, None), size=(300, 250))
            popup.open()
            
    def start_train(self):
        new_model(self.onto_path.text, self.train_set_path.text,
                    self.model_path.text, self.patterns_path.text)

        popup = Popup(title='',
            content=Label(text='Обучение прошло успешно!', font_size=25),
            size_hint=(None, None), size=(300, 250))
        popup.open()

class UpdateModelView():
    pass


class ClassifyView():
    pass


class TrainingProgress(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(TrainingProgress, self).__init__(**kwargs)
        self.size = (500, 300)
        label = Label(text='Обучение прошло успешно', font_size="20px", pos=(0, 150))
        self.add_widget(label)

        close_btn = Button(text='Назад', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)