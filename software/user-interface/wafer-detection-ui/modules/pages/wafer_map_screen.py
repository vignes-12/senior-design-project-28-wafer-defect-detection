Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
import threading

Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder 
from kivymd.toast import toast
from kivy.utils import platform
from kivy.uix.gridlayout import GridLayout

from wfmap import wafermap

from wfmap import defectmap

from kivy.uix.scrollview import ScrollView

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

from data import load_data


Builder.load_string('''
<WaferMap>:
    orientation: 'vertical'
    spacing: "12dp"
    size_hint_x: .6
    size_hint_y: .6
    pos_hint: {"x": .2, "y": .2}
    adaptive_height: True
   

    
    
''')


class WaferMap(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

       
        self.drawMap()
        
        

    def drawMap(self):
        print('wafermap')
        data=load_data()
        # fig=wafermap(data,'MR',wftype='UP3')
        # fig=defectmap(data,'DEFECT')

        self.layout = GridLayout(rows=2, cols=2, spacing = 0, padding=(20))
        
        box = MDBoxLayout()
        canvas = FigureCanvasKivyAgg(fig)
        box.add_widget(canvas)
       
        self.layout.add_widget(box)
        self.add_widget(self.layout)
        




