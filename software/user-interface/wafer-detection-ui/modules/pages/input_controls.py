from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.graphics import Color, Line
from modules.utils.gcode_executor import GCodeExecutor
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.switch import Switch
from modules.utils.gcode_executor import GCodeExecutor
from kivymd.uix.list import TwoLineListItem, IconLeftWidget, TwoLineIconListItem
import serial
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.filemanager import MDFileManager
from modules.utils.popup import *
from kivy.metrics import dp
from kivymd.toast import toast
from modules.utils.stitch_image_snake_func import stitch_images_snake 
import os
from modules.utils.vignes_test import processor
from data import wfdata
from pixelink import PxLapi
from CameraCode import *
from matplotlib import pyplot as plt
import threading
from PIL import Image
from functools import partial

from kivy.clock import Clock
import time


UPDATE_MAP = False


my_path = "/"    
# global directory = ""

class InputControls(BoxLayout):
    
    launched = False
    def __init__(self, **kwargs):
        super(InputControls, self).__init__(**kwargs)

        self.gcodeExecutor = GCodeExecutor()

        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
           # previous=True,
        )


        self.orientation = 'vertical'

        # create an MDCard
        card = MDCard(orientation='vertical')

        self.layout = GridLayout(rows=3, cols=2, spacing = 0, row_force_default=True, row_default_height=40, padding=(20))
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

        self.text_input_port = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(100, 35), multiline = False)
        self.layout.add_widget(self.label_port)
        self.layout.add_widget(self.mainbutton)
       
        self.label2 = Label(text='')
        self.label = Label(text='Enter increment (mm):')
        self.text_input_incr = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(100, 35), multiline = False)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text_input_incr)

        self.label_port_auto = Label(text='Wafer Size (inches)')
        self.text_input_port_auto = TextInput(size_hint_y=None,size_hint_x=None, height='32dp',  size=(100, 35), multiline = False)

        self.layout.add_widget(self.label_port_auto)
        self.layout.add_widget(self.text_input_port_auto)
        card.add_widget(self.layout)

        #-----------------------------------------------------------------------------------------------------------------------
        #new card
        #-----------------------------------------------------------------------------------------------------------------------

        
        card2 = MDCard(orientation='vertical')

        # Add input buttons
        self.layout2 = GridLayout(rows=3, cols=3, row_force_default=True, row_default_height=40, padding=(20))
        # self.layout2.width = max(self.layout2.minimum_width, dp(300))
    
        # Add a label
        self.layout2.add_widget(Label(text='Switch Mode (Relative)'))
        self.layout2.add_widget(Label(text=''))
        self.layout2.add_widget(Label(text=''))
            
        # Add X & Y positions
        self.label_x = Label(text='Enter X:')
        self.text_input_x = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.layout2.add_widget(self.label_x)
        self.layout2.add_widget(self.text_input_x)
        self.layout2.add_widget(Label(text=''))

        self.label_y = Label(text='Enter Y:')
        self.text_input_y = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.layout2.add_widget(self.label_y)
        self.layout2.add_widget(self.text_input_y)

        # Button to move to absolute position
        self.button_movs_abs = Button(text='Move to (X,Y)', size_hint=(None, None), size=(100, 35))
        self.layout2.add_widget(self.button_movs_abs)
        self.button_movs_abs.bind(on_press=self.move_abs)

        card2.add_widget(self.layout2)

        #-----------------------------------------------------------------------------------------------------------------------
        #new card
        #-----------------------------------------------------------------------------------------------------------------------

        card3 = MDCard()

        card3.add_widget(Label(text='Camera Controls'))

        # Button to move for all movement positions
        self.layout3 = FloatLayout()

        self.button_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.5, 'top': 0.9})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout3.add_widget(self.button_up)
        self.button_up.bind(on_press=self.move_up)

        self.button_right = MDIconButton(icon="arrow-right-bold", pos_hint={'right': 0.6, 'top': 0.7})
        self.layout3.add_widget(self.button_right)
        self.button_right.bind(on_press=self.move_right)

        self.button_left = MDIconButton(icon="arrow-left-bold", pos_hint={'x': 0.4, 'top': 0.7})
        self.layout3.add_widget(self.button_left)
        self.button_left.bind(on_press=self.move_left)
        
        self.button_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.5, 'top': 0.5})
        self.layout3.add_widget(self.button_down)
        self.button_down.bind(on_press=self.move_down)

        self.button_z_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.3, 'top': 0.9})
        self.layout3.add_widget(self.button_z_up)
        self.button_z_up.bind(on_press=self.move_z_up)

        self.button_z_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.3, 'top': 0.5})
        self.layout3.add_widget(self.button_z_down)
        self.button_z_down.bind(on_press=self.move_z_down)

        card3.add_widget(self.layout3)

        #-----------------------------------------------------------------------------------------------------------------------
        #new card
        #-----------------------------------------------------------------------------------------------------------------------


        card4 = MDCard(orientation='horizontal')
        self.layout5 = GridLayout(rows=3, cols=1, row_force_default=True, row_default_height=40, padding=(20))
       
        # Create TwoLineListItem
        self.two_line_list_item = TwoLineIconListItem(
                        IconLeftWidget(
                            icon="folder"
                        ),
                        text="Open the file",
                        on_release=lambda x: self.file_manager_open())

        # Add TwoLineListItem to Boxlayout
        self.layout5.add_widget(self.two_line_list_item)
     
        # Create the first MDTextField
        self.directory_field = MDTextField(
            id='directory_field',
            icon_left='file',
            mode='round',
            hint_text='Directory Path',
            height='42dp'
        )
        # Add the first MDTextField to the box layout
        self.layout5.add_widget(self.directory_field)
        
        # Create the second MDTextField
        self.folder_name_field = MDTextField(
            id='folder_name_field',
            icon_left='folder',
            mode='round',
            hint_text='Folder Name',
            height='42dp'
        )
        # Add the second MDTextField to the box layout
        self.layout5.add_widget(self.folder_name_field)
       
        card4.add_widget(self.layout5)


        #All control buttons go
        self.layout6 = BoxLayout(orientation='horizontal')

        #homing button

        self.button_home = Button(text='Home', pos_hint={'right': 0.4, 'top': 0.4},size_hint=(None, None), size=(100, 35))
        self.button_home.bind(on_press=self.home_device)
        self.layout6.add_widget(self.button_home)

        self.button_port_auto = Button(text='Run Auto',pos_hint={'right': 0.4, 'top': 0.4},size_hint=(None, None) , size=(100, 35))
        self.button_port_auto.bind(on_press=self.run_auto)
        
        self.layout6.add_widget(self.button_port_auto)       
       
        self.button_port_cont = Button(text='Continue Auto',pos_hint={'right': 0.4, 'top': 0.4},size_hint=(None, None), size=(100, 35))
        self.button_port_cont.bind(on_press=self.continue_auto)

        self.layout6.add_widget(self.button_port_cont)
        card4.add_widget(self.layout6) 


        self.add_widget(card)
        self.add_widget(BoxLayout(size_hint_y=None, height="10dp"))
        self.add_widget(card2)
        self.add_widget(BoxLayout(size_hint_y=None, height="10dp"))
        self.add_widget(card4)
        self.add_widget(BoxLayout(size_hint_y=None, height="10dp"))
        self.add_widget(card3)
        


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
        # ret = PxLApi.initialize(0)
        # print(ret[0])
        # self.hCamera = ret[1]
        
        #self.camera_view()
        try:
            if hasattr(self, 'file_path') and self.file_path:
                directory_path, file_name = os.path.split(self.file_path)
                print('Directory path:', directory_path)
                print('File name:', file_name)

                self.gcodeExecutor.directory = directory_path + '\\' + file_name + '\\' + self.folder_name_field.text
                self.directory = self.gcodeExecutor.directory
                print(self.gcodeExecutor.directory)
                self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
                self.gcodeExecutor.run_auto()
            else:
                print('File path is empty')
                if self.directory_field.text:
                    self.gcodeExecutor.directory = self.directory_field.text + '\\' + self.folder_name_field.text
                    self.directory = self.gcodeExecutor.directory
                    self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
                    print(self.gcodeExecutor.directory)
                    self.gcodeExecutor.run_auto()
                else:
                    display_error(5)

            with open('config.cfg', 'w+') as f:
                f.write(self.gcodeExecutor.directory)
        except:
            display_error(4)


    def continue_auto(self, instance):       
        #self.gcodeExecutor.continue_auto()
        #try:
        UPDATE_CAMERA = False
        try:
            if hasattr(self, 'file_path') and self.file_path:
                directory_path, file_name = os.path.split(self.file_path)
                print('Directory path:', directory_path)
                print('File name:', file_name)
                self.gcodeExecutor.directory = directory_path + '\\' + file_name + '\\' + self.folder_name_field.text
                self.directory = self.gcodeExecutor.directory
                # print(self.gcodeExecutor.directory)
                self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
            else:
                print('File path is empty')
                if self.directory_field.text:
                    self.gcodeExecutor.directory = self.directory_field.text + '\\' + self.folder_name_field.text
                    self.directory = self.gcodeExecutor.directory
                    self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
                    # print(self.gcodeExecutor.directory)
                else:
                    display_error(5)
            self.gcodeExecutor.continue_auto()
        except:
            display_error(4)
        
        UPDATE_MAP = True
        time.sleep(4)
        UPDATE_MAP = False


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

    def file_manager_open(self):
        self.file_manager.show_disks()  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        # dialog = MDDialog(
        #     title='Selected path',
        #     text=path,
        #     buttons=[
        #         MDFlatButton(
        #             text="OK",
        #             on_release=self.exit_manager
        #         )
        #     ]
        # )
        # dialog.open()
        self.file_path = path
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    
    # Update this method to take input from gcode function (x,y)
    def on_run_scan(self):
        print('Inside on_run_scale function...')
        print(self.ids.directory_field.text)
        print(self.ids.folder_name_field.text)
        # stitch_images_snake(self.ids.directory_field.text, 
        #                     self.ids.folder_name_field.text, 
        #                     self.ids.image_name_field.text,
        #                     self.ids.xval_field.text,
        #                     self.ids.yval_field.text,)

    