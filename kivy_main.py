from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

from modal_views import NewModelView, UpdateModelView, ClassifyView


Window.size = (600, 400)


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Классификатор номенклатуры', color=(0,0,0,1), pos=(0,150)))

        self.new_model_btn = Button(text='Обучить новую модель', size_hint=(.25, .25), pos=(20, 180))
        self.update_model_btn = Button(text='Продолжить обучение модели', size_hint=(.25, .25), pos=(220, 180))
        self.classify_btn = Button(text='Классифицировать данные', size_hint=(.25, .25), pos=(420, 180))

        self.new_model_btn.bind(on_press=open_new_model_view)
        self.update_model_btn.bind(on_press=open_update_model_view)
        self.classify_btn.bind(on_press=open_classify_view)

        self.add_widget(self.new_model_btn)
        self.add_widget(self.update_model_btn)
        self.add_widget(self.classify_btn)


def open_new_model_view(instance):
    view = NewModelView(auto_dismiss=False)
    view.open()


def open_update_model_view(instance):
    view = UpdateModelView(auto_dismiss=False)
    view.open()


def open_classify_view(instance):
    view = ClassifyView(auto_dismiss=False)
    view.open()



class OntoClass(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    OntoClass().run()