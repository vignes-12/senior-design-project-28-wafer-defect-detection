from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.graphics import Color, Line
from modules.utils.gcode_executor import GCodeExecutor
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.switch import Switch
from modules.utils.gcode_executor import GCodeExecutor
import serial
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivy.graphics import Color, Ellipse
from modules.utils.popup import *

from modules.utils.vignes_test import processor

import os




class InputControls(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super(InputControls, self).__init__(**kwargs)

        self.gcodeExecutor = GCodeExecutor()

        # create a box layout
        # self.orientation = 'vertical'
        self.orientation = 'horizontal'

        self.layout_connect = GridLayout(rows=3, cols=3, spacing = 0, row_force_default=True, row_default_height=40, padding=(20))
        self.label_port = Label(text='Serial Port')

        self.dropdown = DropDown()
        for index in range(10):
            btn = Button(text='COM%d' % index, size_hint_y=None, height=35)
            btn.bind(on_release=lambda btn: self.connect_serial(port=btn.text))
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.mainbutton = Button(text='COM PORT', size_hint_y=None, height=35)

        self.mainbutton.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        self.text_input_port = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        #self.button_port = Button(text='Connect', size_hint=(None, None), size=(100, 35))
        #self.button_port.bind(on_press=self.connect_serial)
        self.layout_connect.add_widget(self.label_port)
        self.layout_connect.add_widget(self.mainbutton)
        #self.layout.add_widget(self.button_port)

        # self.layout1 = GridLayout(cols=3, row_force_default=True, row_default_height=40, padding=(20))
        self.label2 = Label(text='')
        self.layout_connect.add_widget(self.label2)
        self.label = Label(text='Enter increment (mm):')
        self.text_input_incr = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(100, 35), multiline = False)
        self.layout_connect.add_widget(self.label)
        self.layout_connect.add_widget(self.text_input_incr)
        

        # # create label and slider widgets
        # self.label = Label(text='Select increment (mm):', size_hint_y=None, height='32dp')
        # self.slider = Slider(min=0, max=10, step=0.1, size_hint_y=None, height='32dp')
        # # add widgets to layout
        # self.layout.add_widget(self.label)
        # self.layout.add_widget(self.slider)
        # self.slider_value = Label(text=str(self.slider.value), size_hint_y=None, height='32dp')
        # # bind label to slider value
        # self.slider.bind(value=self.on_value_change)
        # self.layout.add_widget(self.slider_value)

#homing button

        self.button_home = Button(text='Home', size_hint=(None, None), size=(100, 35))
        self.button_home.bind(on_press=self.home_device)
        self.layout_connect.add_widget(self.button_home)

        self.button_display = Button(text='Open PixeLINK', size_hint=(None, None), size=(100, 35))
        self.button_display.bind(on_press=self.open_PL)
        self.layout_connect.add_widget(self.button_display)

        self.process_button = Button(text='PROCESS TEST', size_hint=(None, None), size=(100, 35))
        self.process_button.bind(on_press=self.process_test)
        self.layout_connect.add_widget(self.process_button)
   
        # Add input buttons
        self.absolute_position = GridLayout(rows=4, cols=3, row_force_default=True, row_default_height=40, padding=(20))

        # Add a label
        self.absolute_position.add_widget(Label(text='Movement Controls'))
        self.absolute_position.add_widget(Label(text=''))
        self.absolute_position.add_widget(Label(text=''))
        # Add a switch
        #self.switch_mode = Switch(active=False)
        #self.switch_mode.bind(active=self.on_switch_active)
        #self.layout2.add_widget(self.switch_mode)

    
        # Add X & Y positions
        self.label_x = Label(text='Enter X:')
        self.text_input_x = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.absolute_position.add_widget(self.label_x)
        self.absolute_position.add_widget(self.text_input_x)
        self.absolute_position.add_widget(Label(text=''))

        self.label_y = Label(text='Enter Y:')
        self.text_input_y = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.absolute_position.add_widget(self.label_y)
        self.absolute_position.add_widget(self.text_input_y)

        # Button to move to absolute position
        self.button_movs_abs = Button(text='Move to (X,Y)', size_hint=(None, None), size=(100, 35))
        self.absolute_position.add_widget(self.button_movs_abs)
        self.button_movs_abs.bind(on_press=self.move_abs)

        # Button to move for all movement positions

        # self.temp_grid_layout = GridLayout(rows=1, cols=2, row_force_default=True, row_default_height=40, padding=(20))

        self.layout_arrow = FloatLayout()

        # self.temp_layout = BoxLayout(orientation='vertical')
        
        #(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))
        # self.button_up = Button(text="^", size_hint=(None, None), size=(100, 35))
        # self.button_down = Button(text="v", size_hint=(None, None), size=(100, 35))
        # self.button_left = Button(text="<", size_hint=(None, None), size=(100, 35))
        # self.button_right = Button(text=">", size_hint=(None, None), size=(100, 35))

        self.button_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.5, 'top': 0.9})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout_arrow.add_widget(self.button_up)
        self.button_up.bind(on_press=self.move_up)

        self.button_right = MDIconButton(icon="arrow-right-bold", pos_hint={'right': 0.6, 'top': 0.7})
        # label2 = MDLabel(text="X+", halign="auto",font_size="10sp")
        # self.button_right.add_widget(label2)
        self.layout_arrow.add_widget(self.button_right)
        self.button_right.bind(on_press=self.move_right)

        self.button_left = MDIconButton(icon="arrow-left-bold", pos_hint={'x': 0.4, 'top': 0.7})
        # label3 = MDLabel(text="X-", halign="auto",font_size="10sp")
        # self.button_left.add_widget(label3)
        self.layout_arrow.add_widget(self.button_left)
        self.button_left.bind(on_press=self.move_left)
        
        self.button_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.5, 'top': 0.5})
        # label4 = MDLabel(text="Y-", halign="auto",font_size="10sp")
        # self.button_down.add_widget(label4)
        self.layout_arrow.add_widget(self.button_down)
        self.button_down.bind(on_press=self.move_down)

        self.button_z_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.3, 'top': 0.9})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout_arrow.add_widget(self.button_z_up)
        self.button_z_up.bind(on_press=self.move_z_up)

        self.button_z_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.3, 'top': 0.5})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout_arrow.add_widget(self.button_z_down)
        self.button_z_down.bind(on_press=self.move_z_down)

        # Add to temp grid layout
        # self.temp_grid_layout.add_widget(self.layout3)
        # self.temp_grid_layout.add_widget(self.temp_layout)
        # self.layout3.add_widget(self.temp_layout)

        
#auto button with input wafer size

        self.layout_auto = GridLayout(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))
        
        self.label_port_auto = Label(text='Wafer Size (inches)')
        self.text_input_port_auto = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        self.button_port_auto = Button(text='Run Auto', size_hint=(None, None), size=(100, 35))
        self.button_port_auto.bind(on_press=self.run_auto)
        self.layout_auto.add_widget(self.label_port_auto)
        self.layout_auto.add_widget(self.text_input_port_auto)
        self.layout_auto.add_widget(self.button_port_auto)

        self.button_port_cont = Button(text='Continue Auto', size_hint=(None, None), size=(100, 35))
        self.button_port_cont.bind(on_press=self.continue_auto)
        self.layout_auto.add_widget(self.button_port_cont)

        self.label_dir = Label(text='Directory to Use')
        self.text_input_dir = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        self.layout_auto.add_widget(self.label_dir)
        self.layout_auto.add_widget(self.text_input_dir)

        self.layout_right = GridLayout(rows=4, cols=1, row_force_default=False, row_default_height=40, padding=(20))
        #self.layout_right.orientation = 'vertical'
        self.layout_left = GridLayout(rows=4, cols=1, row_force_default=True, row_default_height=40, padding=(20))
        self.layout_right.add_widget(self.layout_connect)


        self.layout_right.add_widget(self.absolute_position)
        # self.add_widget(self.temp_grid_layout)
        self.layout_right.add_widget(self.layout_arrow)
        self.layout_right.add_widget(self.layout_auto)

        
        #self.add_widget(self.layout_left)
        self.add_widget(self.layout_right)



    #-------------------------------------------------------------------------------------
    # on-click functions
    #-------------------------------------------------------------------------------------

    def process_test(self, instance):
        proc = processor()
        proc.IMG_DIR = self.text_input_dir.text
        proc.process_data()



    def open_PL(self, instance):
        os.startfile("C:\\Program Files (x86)\\PixeLINK\\Pixelink Capture\\PixelinkCapture.exe")

    def on_switch_active(self, switch, value):
        if value:
            print('Switching mode to Relative position')
            # disable X & Y text inputs
            self.text_input_x.disabled = True
            self.text_input_y.disabled = True
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
        else:
            print('Switching mode to Absolute position')
            self.text_input_x.disabled = False
            self.text_input_y.disabled = False
            command = f"G90\n"
            self.gcodeExecutor.gcode_write(command)

    def connect_serial(self, port):
        #self.gcodeExecutor.port_input = self.text_input_port.text
        self.gcodeExecutor.connect_serial(port)

    def move_z_down(self, instance):
        try:
            print(f'Moving down... {self.text_input_incr.text}')
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Z{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)

    def move_z_up(self, instance):
        print(f'Moving up... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Z-{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
        

    def move_abs(self, instance):
        print(f'Moving to absolute position... ( {self.text_input_x.text},  {self.text_input_y.text})')
        try:
            increment_x = float(self.text_input_x.text)
            increment_y = float(self.text_input_y.text)
            command = f"G90\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 X{increment_x} Y{increment_y}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
        

    # Define a function to run when the up arrow button is clicked
    def move_up(self, instance):
        print(f'Moving back... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Y{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
        

    # Define a function to run when the down arrow button is clicked
    def move_down(self, instance):
        print(f'Moving forward... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Y-{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
        

    # Define a function to run when the left arrow button is clicked
    def move_left(self, instance):
        print(f'Moving left... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 X-{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
      

    # Define a function to run when the right arrow button is clicked
    def move_right(self, instance):
        print(f'Moving right... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 X{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(1)
       
    # Define a function to run when the auto button is clicked 
    def run_auto(self, instance):
        try:
            self.gcodeExecutor.directory = self.text_input_dir.text
            self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
            self.gcodeExecutor.run_auto()
        except:
            display_error(4)

    def continue_auto(self, instance):       
        #self.gcodeExecutor.continue_auto()
        try:
            self.gcodeExecutor.directory = self.text_input_dir.text
            self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
            self.gcodeExecutor.continue_auto()            
        except:
            display_error(4)
     

        proc = processor()
        proc.IMG_DIR = self.text_input_dir.text
        proc.process_data()


    #Print values for the sliders
    def on_value_change(self, instance, value):
        self.slider_value.text = str(value)

    #Add Homing feature 
    def home_device(self, instance):
        try:
            print(f'Homing... {self.text_input_incr.text}')
            command = f"G28 X Y\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            display_error(3)