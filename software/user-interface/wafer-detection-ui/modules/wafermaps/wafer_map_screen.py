# Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
import threading

# Logger.setLevel(logging.TRACE)
from kivy.clock import Clock
from kivy.uix.widget import Widget
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
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder 
from kivymd.toast import toast
from kivy.utils import platform
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from wfmap import wafermap

from wfmap import defectmap

from kivy.uix.scrollview import ScrollView

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, FigureCanvasKivy, NavigationToolbar2Kivy
import matplotlib.pyplot as plt

#from data import load_data

import matplotlib.pyplot as plt
import numpy as np
import csv

from modules.utils.wafer_map_generator import generate_wafer_map
from modules.wafermaps.graph_widget import MatplotFigure
from modules.wafermaps.hover_widget import add_hover,HoverVerticalText,InfoHover
from matplotlib.ticker import FormatStrFormatter
#from modules.pages.input_controls import *
from modules.pages.input_controls import UPDATE_MAP



Builder.load_string('''
<WaferMap>:
    figure_wgt:figure_wgt
    BoxLayout:
        orientation:'vertical'
        spacing: "12dp"
        size_hint_x: .6
        size_hint_y: .6
        pos_hint: {"x": .2, "y": .2}
        adaptive_height: True
         
        # BoxLayout:
        #     size_hint_y:0.2                    
        #     ToggleButton:
        #         group:'touch_mode'
        #         text:"pan_x" 
        #         on_press:
        #             root.set_touch_mode('pan_x')
        #             self.state='down'
        #     ToggleButton:
        #         group:'touch_mode'
        #         text:"pan_y" 
        #         on_press:
        #             root.set_touch_mode('pan_y')
        #             self.state='down'                    
        #     ToggleButton:
        #         group:'touch_mode'
        #         text:"adjust_x"  
        #         on_press:
        #             root.set_touch_mode('adjust_x')
        #             self.state='down'
        #     ToggleButton:
        #         group:'touch_mode'
        #         text:"adjust_y"  
        #         on_press:
        #             root.set_touch_mode('adjust_y')
        #             self.state='down' 

        #     ToggleButton:
        #         text:"zoom_x"  
        #         on_press:
        #             root.set_zoom_behavior('zoom_x',self.state)                     
        #     ToggleButton:
        #         text:"zoom_y"  
        #         on_press:
        #             root.set_zoom_behavior('zoom_y',self.state)                      
        MatplotFigure:
            id:figure_wgt
            #update axis during pan/zoom
            fast_draw:False
        # BoxLayout:
        #     # spacing: "12dp"
        #     size_hint_y:0.2
        #     # pos_hint: {"x": .2, "y": .2}
        #     Button:
        #         text:"home"
        #         on_release:root.calc_coords()
        #     Label:
        #             text: "placeholder"
        BoxLayout:
            # spacing: "12dp"
            size_hint_y:0.2
            # pos_hint: {"x": .2, "y": .2}
            Button:
                text:"home"
                on_release:root.home()
            Button:
                text:"back"
                on_release:root.back()  
            Button:
                text:"forward"
                on_release:root.forward()                
            ToggleButton:
                group:'touch_mode'
                state:'down'
                text:"pan" 
                on_press:
                    root.set_touch_mode('pan')
                    self.state='down'
            ToggleButton:
                group:'touch_mode'
                text:"zoom box"  
                on_release:
                    root.set_touch_mode('zoombox')
                    self.state='down' 
            ToggleButton:
                group:'touch_mode'
                text:"cursor"  
                on_release:
                    root.set_touch_mode('cursor')
                    self.state='down' 
    
''')


class WaferMap(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
        # Clock.schedule_once(self._finish_init)
        Clock.schedule_interval(self._finish_init, 3)

    def _finish_init(self, dt):

        if(UPDATE_MAP):
            try:
                self.figure_wgt.figure = generate_wafer_map()
            except:
                print("csv not found")

        # ax3=self.figure_wgt.figure.axes[0]
        # self.figure_wgt.register_lines(list(ax3.get_lines()))
        
        # #set x/y formatter for hover data
        # self.figure_wgt.cursor_xaxis_formatter = FormatStrFormatter('%.1f')
        # self.figure_wgt.cursor_yaxis_formatter = FormatStrFormatter('%.1f')  
            
        # #add custom hover widget "InfoHover" hover to the figure.
        # add_hover(self.figure_wgt,mode='desktop',hover_widget=InfoHover())

    def set_touch_mode(self,mode):
        self.figure_wgt.touch_mode=mode

    def set_zoom_behavior(self,mode,state):
        boolean_val=True
        if state=='down':
            boolean_val=False
        if mode=='zoom_x':
            self.figure_wgt.do_zoom_y=boolean_val
        elif mode=='zoom_y':
            self.figure_wgt.do_zoom_x=boolean_val        
    def home(self):
        self.figure_wgt.home()
    def back(self):
        self.figure_wgt.back()   
    def forward(self):
        self.figure_wgt.forward() 