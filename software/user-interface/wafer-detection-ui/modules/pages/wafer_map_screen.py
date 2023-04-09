# Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
import threading

# Logger.setLevel(logging.TRACE)

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

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg, FigureCanvasKivy, NavigationToolbar2Kivy
import matplotlib.pyplot as plt

#from data import load_data

import matplotlib.pyplot as plt
import numpy as np
import csv

from modules.utils.wafer_map_generator import generate_wafer_map


Builder.load_string('''
<WaferMap>:
    orientation: 'vertical'
    spacing: "12dp"
    size_hint_x: .6
    size_hint_y: .6
    pos_hint: {"x": .2, "y": .2}
    adaptive_height: True

    # Button:
    #     text: "Re-Draw"
    #     on_press: root.re_draw()
    
''')


class WaferMap(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fig = generate_wafer_map()
        self.drawMap()
        

    def drawMap(self):
        print('wafermap')
     
        self.layout = GridLayout(rows=2, cols=2, spacing = 0, padding=(20))
        
        self.box = MDBoxLayout()
        
        canvas = FigureCanvasKivyAgg(self.fig)

        # bind callback events
        # fig.canvas.mpl_connect('button_press_event', self.press)
        # fig.canvas.mpl_connect('button_release_event', self.release)
        # fig.canvas.mpl_connect('key_press_event', self.keypress)
        # fig.canvas.mpl_connect('key_release_event', self.keyup)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        # fig.canvas.mpl_connect('resize_event', self.resize)
        # self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        # fig.canvas.mpl_connect('figure_enter_event', self.figure_enter)
        # fig.canvas.mpl_connect('figure_leave_event', self.figure_leave)
        # fig.canvas.mpl_connect('close_event', self.close)

        # toolbar = NavigationToolbar2Kivy(self.canvas)
        # Bind the callback function to the figure_leave event
       

        self.box.add_widget(canvas)       
        
        self.layout.add_widget(self.box)

        # Add a label to display the x, y coordinates
        self.label = Label(text='')
        self.layout.add_widget(self.label)
        # self.add_widget(toolbar.actionbar)
        self.add_widget(self.layout)
        
        

    def press(self, event):
        print('press released from test', event.x, event.y, event.button)
    def release(self, event):
        print('release released from test', event.x, event.y, event.button)
    def keypress(self, event):
        print('key down', event.key)
    def keyup(self, event):
        print('key up', event.key)
    def motionnotify(self, event):
        print('mouse move to ', event.x, event.y)
    def resize(self, event):
        print('resize from mpl ', event)
    def scroll(self, event):
        print('scroll event from mpl ', event.x, event.y, event.step)
    def figure_enter(self, event):
        print('figure enter mpl')
    def figure_leave(self, event):
        print('figure leaving mpl')
    def close(self, event):
        print('closing figure')

    def on_motion(self, event):
        # Get the x, y coordinates from the event
        x, y = event.x, event.y

        # Convert the x, y coordinates to data coordinates
        fig = plt.gcf()
        ax = fig.gca()
        x_data, y_data = ax.transData.inverted().transform((x, y))

        # Update the label text with the x, y coordinates
        self.label.text = f'x={x_data:.2f}, y={y_data:.2f}'

    def on_scroll(self, event):
        # Get the x, y coordinates from the event
        x, y = event.x, event.y

      
        fig = plt.gcf()
        ax = fig.gca()
        # Convert the x, y coordinates to data coordinates
        x_data, y_data = ax.transData.inverted().transform((x, y))

        # Get the current x and y limits
        x_lim = ax.get_xlim()
        y_lim = ax.get_ylim()

        # Get the scroll direction and scale factor
        direction = event.button
        if direction == 'up':
            scale_factor = 1/1.5
        elif direction == 'down':
            scale_factor = 1.5

        # Calculate the new x and y limits
        x_range = x_lim[1] - x_lim[0]
        y_range = y_lim[1] - y_lim[0]
        x_center = (x_data - x_lim[0]) / x_range
        y_center = (y_data - y_lim[0]) / y_range
        x_min = x_data - x_center * x_range * scale_factor
        x_max = x_data + (1 - x_center) * x_range * scale_factor
        y_min = y_data - y_center * y_range * scale_factor
        y_max = y_data + (1 - y_center) * y_range * scale_factor

        # Set the new x and y limits
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])

        # Redraw the plot
        self.fig.canvas.draw_idle()

    def on_run_scan(self):
        # self.drawMap()
        print()





