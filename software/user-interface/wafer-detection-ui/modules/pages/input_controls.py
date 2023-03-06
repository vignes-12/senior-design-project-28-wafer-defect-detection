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


class InputControls(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super(InputControls, self).__init__(**kwargs)

        self.gcodeExecutor = GCodeExecutor()

        # create a box layout
        # self.orientation = 'vertical'
        self.orientation = 'vertical'

        self.layout = GridLayout(rows=2, cols=3, spacing = 0, row_force_default=True, row_default_height=40, padding=(20))
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

        self.layout3 = GridLayout(rows=4, cols=2, row_force_default=True, row_default_height=40, padding=(20))
       

        self.button_up = Button(text='Up', size_hint=(None, None), size=(100, 35))
        self.button_down = Button(text='Down', size_hint=(None, None), size=(100, 35))
        self.button_left = Button(text='Left', size_hint=(None, None), size=(100, 35))
        self.button_right = Button(text='Right', size_hint=(None, None), size=(100, 35))

        self.layout3.add_widget(self.button_up)
        self.button_up.bind(on_press=self.move_up)

        self.layout3.add_widget(self.button_down)
        self.button_down.bind(on_press=self.move_down)

        self.layout3.add_widget(self.button_left)
        self.button_left.bind(on_press=self.move_left)

        self.layout3.add_widget(self.button_right)
        self.button_right.bind(on_press=self.move_right)

#auto button with input wafer size

        self.label_port_auto = Label(text='Wafer Size (cm)')
        self.text_input_port_auto = TextInput(size_hint_y=None,size_hint_x=None, height='32dp', size=(300, 35), multiline = False)
        self.button_port_auto = Button(text='Run Auto', size_hint=(None, None), size=(100, 35))
        self.button_port_auto.bind(on_press=self.run_auto)
        self.layout3.add_widget(self.label_port_auto)
        self.layout3.add_widget(self.text_input_port_auto)
        self.layout3.add_widget(self.button_port_auto)


        self.add_widget(self.layout)
        self.add_widget(self.layout2)
        self.add_widget(self.layout3)
    
        # self.layout.add_widget(Label(text="Serial Communication"))
        # self.layout2.add_widget(Label(text="Manual Control"))
        # self.layout3.add_widget(Label(text="Auto Mode"))




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
            # self.gcodeExecutor.gcode_write(command)
        else:
            print('Switching mode to Absolute position')
            self.text_input_x.disabled = False
            self.text_input_y.disabled = False
            command = f"G90\n"
            # self.gcodeExecutor.gcode_write(command)

    def connect_serial(self, instance):
        self.gcodeExecutor.port_input = self.text_input_port.text
        self.gcodeExecutor.connect_serial()


    def move_abs(self, instance):
        print(f'Moving to absolute position... ( {self.text_input_x.text},  {self.text_input_y.text})')
        increment_x = float(self.text_input_x.text)
        increment_y = float(self.text_input_y.text)
        command = f"G0 X{increment_x} Y{increment_y}\n"
        # self.gcodeExecutor.gcode_write(command)
        

    # Define a function to run when the up arrow button is clicked
    def move_up(self, instance):
        print(f'Moving up... {self.text_input_incr.text}')
        increment = float(self.text_input_incr.text)
        command = f"G0 Y{increment}\n"
        # self.gcodeExecutor.gcode_write(command)
        

    # Define a function to run when the down arrow button is clicked
    def move_down(self, instance):
        print(f'Moving down... {self.text_input_incr.text}')
        increment = float(self.text_input_incr.text)
        command = f"G0 Y-{increment}\n"
        # self.gcodeExecutor.gcode_write(command)
        

    # Define a function to run when the left arrow button is clicked
    def move_left(self, instance):
        print(f'Moving left... {self.text_input_incr.text}')
        increment = float(self.text_input_incr.text)
        command = f"G0 X-{increment}\n"
        # self.gcodeExecutor.gcode_write(command)
      

    # Define a function to run when the right arrow button is clicked
    def move_right(self, instance):
        print(f'Moving right... {self.text_input_incr.text}')
        increment = float(self.text_input_incr.text)
        command = f"G0 X{increment}\n"
        # self.gcodeExecutor.gcode_write(command)
       
    # Define a function to run when the auto button is clicked 
    def run_auto(self, instance):
        self.gcodeExecutor.input_wafer_size = self.text_input_port_auto.text
        self.gcodeExecutor.run_auto()
        