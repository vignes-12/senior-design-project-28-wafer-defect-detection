from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(name=kwargs.get('name'))
        
        self.layout_hint_with_bounds = BoxLayout(padding=10)
        button = Button(text="wow")
        self.layout_hint_with_bounds.add_widget(button)