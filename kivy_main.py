from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooser

from kivy.core.window import Window
Window.size = (600, 400)


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Классификатор номенклатуры', color=(0,0,0,1), pos=(0,150)))
        self.new_model_btn = Button(text='Обучить новую модель', size_hint=(.25, .25), pos=(20, 180))
        self.update_model_btn = Button(text='Дообучить существующую модель', size_hint=(.25, .25), pos=(220, 180))
        self.new_model_btn.bind(on_press=new_model_view)
        self.add_widget(self.new_model_btn)
        self.add_widget(self.update_model_btn)
        self.classify_btn = Button(text='Классифицировать данные', size_hint=(.25, .25), pos=(420, 180))
        self.add_widget(self.classify_btn)


class NewModelView(FloatLayout, ModalView):
    def __init__(self, **kwargs):
        super(NewModelView, self).__init__(**kwargs)
        self.size = (600, 400)
        self.add_widget(Label(text='Обучение новой модели', pos=(0, 150)))

        load_train_set_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(load_train_set_btn)
        close_btn = Button(text='Отмена', size_hint=(.25, .1), pos=(20, 20), background_color=to_rbga((192, 57, 43, 1)))
        self.add_widget(close_btn)
        close_btn.bind(on_press=self.dismiss)

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)




def new_model_view(instance):
    view = NewModelView(auto_dismiss=False)
    view.open()
    
def to_rbga(rbga):
    return (rbga[0]/255.0, rbga[1]/255.0, rbga[2]/255.0, rbga[3])

class OntoClass(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    OntoClass().run()