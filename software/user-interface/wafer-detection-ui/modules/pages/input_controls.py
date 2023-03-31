from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
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



class InputControls(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super(InputControls, self).__init__(**kwargs)

        self.gcodeExecutor = GCodeExecutor()

        # create a box layout
        # self.orientation = 'vertical'
        self.orientation = 'vertical'

        self.layout = GridLayout(rows=3, cols=3, spacing = 0, row_force_default=True, row_default_height=40, padding=(20))
        self.label_port = Label(text='Serial Port')
        self.text_input_port = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        self.button_port = Button(text='Connect', size_hint=(None, None), size=(100, 35))
        self.button_port.bind(on_press=self.connect_serial)
        self.layout.add_widget(self.label_port)
        self.layout.add_widget(self.text_input_port)
        self.layout.add_widget(self.button_port)

        # self.layout1 = GridLayout(cols=3, row_force_default=True, row_default_height=40, padding=(20))

        self.label = Label(text='Enter increment (mm):')
        self.text_input_incr = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(100, 35), multiline = False)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.text_input_incr)
        

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
        self.layout.add_widget(self.button_home)
   
        # Add input buttons
        self.layout2 = GridLayout(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))

        # Add a label
        self.layout2.add_widget(Label(text='Switch Mode (Relative)'))

        # Add a switch
        self.switch_mode = Switch(active=False)
        self.switch_mode.bind(active=self.on_switch_active)
        self.layout2.add_widget(self.switch_mode)

    
        # Add X & Y positions
        self.label_x = Label(text='Enter X:')
        self.text_input_x = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.layout2.add_widget(self.label_x)
        self.layout2.add_widget(self.text_input_x)

        self.label_y = Label(text='Enter Y:')
        self.text_input_y = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(50, 35), multiline = False)
        self.layout2.add_widget(self.label_y)
        self.layout2.add_widget(self.text_input_y)

        # Button to move to absolute position
        self.button_movs_abs = Button(text='Move to (X,Y)', size_hint=(None, None), size=(100, 35))
        self.layout2.add_widget(self.button_movs_abs)
        self.button_movs_abs.bind(on_press=self.move_abs)

        # Button to move for all movement positions

        # self.temp_grid_layout = GridLayout(rows=1, cols=2, row_force_default=True, row_default_height=40, padding=(20))

        self.layout3 = FloatLayout()

        # self.temp_layout = BoxLayout(orientation='vertical')
        
        #(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))
        # self.button_up = Button(text="^", size_hint=(None, None), size=(100, 35))
        # self.button_down = Button(text="v", size_hint=(None, None), size=(100, 35))
        # self.button_left = Button(text="<", size_hint=(None, None), size=(100, 35))
        # self.button_right = Button(text=">", size_hint=(None, None), size=(100, 35))

        self.button_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.5, 'top': 0.9})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout3.add_widget(self.button_up)
        self.button_up.bind(on_press=self.move_up)

        self.button_right = MDIconButton(icon="arrow-right-bold", pos_hint={'right': 0.6, 'top': 0.7})
        # label2 = MDLabel(text="X+", halign="auto",font_size="10sp")
        # self.button_right.add_widget(label2)
        self.layout3.add_widget(self.button_right)
        self.button_right.bind(on_press=self.move_right)

        self.button_left = MDIconButton(icon="arrow-left-bold", pos_hint={'x': 0.4, 'top': 0.7})
        # label3 = MDLabel(text="X-", halign="auto",font_size="10sp")
        # self.button_left.add_widget(label3)
        self.layout3.add_widget(self.button_left)
        self.button_left.bind(on_press=self.move_left)
        
        self.button_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.5, 'top': 0.5})
        # label4 = MDLabel(text="Y-", halign="auto",font_size="10sp")
        # self.button_down.add_widget(label4)
        self.layout3.add_widget(self.button_down)
        self.button_down.bind(on_press=self.move_down)

        self.button_z_up = MDIconButton(icon="arrow-up-bold", pos_hint={'center_x': 0.3, 'top': 0.9})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout3.add_widget(self.button_z_up)
        self.button_z_up.bind(on_press=self.move_z_up)

        self.button_z_down = MDIconButton(icon="arrow-down-bold", pos_hint={'center_x': 0.3, 'top': 0.5})
        # label1 = Label(text="Y+", , size_hint_y=0.2)
        # self.button_up.add_widget(label1)
        self.layout3.add_widget(self.button_z_down)
        self.button_z_down.bind(on_press=self.move_z_down)

        # Add to temp grid layout
        # self.temp_grid_layout.add_widget(self.layout3)
        # self.temp_grid_layout.add_widget(self.temp_layout)
        # self.layout3.add_widget(self.temp_layout)

        
#auto button with input wafer size

        self.layout4 = GridLayout(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))


        self.label_port_auto = Label(text='Wafer Size (cm)')
        self.text_input_port_auto = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        self.button_port_auto = Button(text='Run Auto', size_hint=(None, None), size=(100, 35))
        self.button_port_auto.bind(on_press=self.run_auto)
        self.layout4.add_widget(self.label_port_auto)
        self.layout4.add_widget(self.text_input_port_auto)
        self.layout4.add_widget(self.button_port_auto)

        self.button_port_cont = Button(text='Continue Auto', size_hint=(None, None), size=(100, 35))
        self.button_port_cont.bind(on_press=self.continue_auto)
        self.layout4.add_widget(self.button_port_cont)


        self.add_widget(self.layout)
        self.add_widget(self.layout2)
        # self.add_widget(self.temp_grid_layout)
        self.add_widget(self.layout3)
        self.add_widget(self.layout4)



    #-------------------------------------------------------------------------------------
    # on-click functions
    #-------------------------------------------------------------------------------------

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

    def connect_serial(self, instance):
        self.gcodeExecutor.port_input = self.text_input_port.text
        self.gcodeExecutor.connect_serial()

    def move_z_down(self, instance):
        try:
            print(f'Moving down... {self.text_input_incr.text}')
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Z{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            print("MOVE FAILED")

    def move_z_up(self, instance):
        print(f'Moving up... {self.text_input_incr.text}')
        try:
            increment = float(self.text_input_incr.text)
            command = f"G91\n"
            self.gcodeExecutor.gcode_write(command)
            command = f"G0 Z-{increment}\n"
            self.gcodeExecutor.gcode_write(command)
        except:
            print("MOVE FAILED")
        

    def move_abs(self, instance):
        print(f'Moving to absolute position... ( {self.text_input_x.text},  {self.text_input_y.text})')
        increment_x = float(self.text_input_x.text)
        increment_y = float(self.text_input_y.text)
        command = f"G90\n"
        self.gcodeExecutor.gcode_write(command)
        command = f"G0 X{increment_x} Y{increment_y}\n"
        self.gcodeExecutor.gcode_write(command)
        

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
            print("MOVE FAILED")
        

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
            print("MOVE FAILED")
        

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
            print("MOVE FAILED")
      

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
            print("MOVE FAILED")
       
    # Define a function to run when the auto button is clicked 
    def run_auto(self, instance):
        self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
        self.gcodeExecutor.run_auto()

    def continue_auto(self, instance):
        self.gcodeExecutor.continue_auto()


    #Print values for the sliders
    def on_value_change(self, instance, value):
        self.slider_value.text = str(value)

    #Add Homing feature 
    def home_device(self, instance):
        print(f'Homing... {self.text_input_incr.text}')
        command = f"G28 X Y\n"
        self.gcodeExecutor.gcode_write(command)
