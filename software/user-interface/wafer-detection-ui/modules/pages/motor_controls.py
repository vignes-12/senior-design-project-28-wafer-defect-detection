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


class MotorControls(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super(MotorControls, self).__init__(**kwargs)


        # create a box layout
        self.orientation = 'vertical'
        self.spacing = 10

        self.box2 = BoxLayout(orientation='vertical')
            
        # Set the grid layout properties
        # Create the grid layout widget
        self.grid_layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)

        # Add Input button inside a grid layout
        self.label = Label(text='Enter increment movement (mm):')
        self.text_input_incr = TextInput(size_hint=(None, None), size=(400, 50))
        self.grid_layout.add_widget(self.label)
        self.grid_layout.add_widget(self.text_input_incr)

        self.box2.add_widget(self.grid_layout)


        # self.cols = 2
        # self.row_force_default = True
        # self.row_default_height = 40

        # Create the X-axis slider
        # self.x_slider = Slider(min=-100, max=100, value=0, orientation='horizontal')
        # self.x_slider.bind(value=self.on_value_change)
        
        # self.grid_layout.add_widget(Label(text='X-Axis'))
        # self.grid_layout.add_widget(self.x_slider)
        
        # Create the Y-axis slider
        # self.y_slider = Slider(min=-100, max=100, value=0, orientation='horizontal')
        # self.y_slider.bind(value=self.on_value_change)
        
        # self.grid_layout.add_widget(Label(text='Y-Axis'))
        # self.grid_layout.add_widget(self.y_slider)

        # self.grid_layout_2 = GridLayout(cols=1, row_force_default=True)
        # self.reset = Button(text='Reset', size_hint=(None, None), size=(100, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # self.reset.bind(on_press=self.on_reset)

        # self.grid_layout.add_widget(self.reset)

        # self.add_widget(self.grid_layout)
        # self.add_widget(self.grid_layout_2)

        # Draw a horizontal line
        # with self.canvas:
        #     Color(1, 0, 0, 1)
        #     Line(points=[self.x, self.y, self.width, self.y], width=1)

        # self.box2 = BoxLayout(orientation='vertical')
        # self.box2.add_widget(self.reset)

        # self.add_widget(self.box2)



        self.box3 = BoxLayout(orientation='vertical')

        # Add input buttons
        self.layout_directions_buttons = GridLayout(cols=4, row_force_default=True, row_default_height=40)

        self.button_up = Button(text='Up', size_hint=(None, None), size=(100, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.button_down = Button(text='Down', size_hint=(None, None), size=(100, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.button_left = Button(text='Left', size_hint=(None, None), size=(100, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.button_right = Button(text='Right', size_hint=(None, None), size=(100, 50),pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.layout_directions_buttons.add_widget(self.button_up)
        self.layout_directions_buttons.add_widget(self.button_down)
        self.layout_directions_buttons.add_widget(self.button_left)
        self.layout_directions_buttons.add_widget(self.button_right)
        
        self.box3.add_widget(self.layout_directions_buttons)


        self.add_widget(self.box2)
        self.add_widget(self.box3)
        

    def on_value_change(self, instance, value):
        # Update the CNC machine based on the slider values
        print(f'X-Axis value: {self.x_slider.value}, Y-Axis value: {self.y_slider.value}')
        # gcodeExecutor = GCodeExecutor()
        # gcodeExecutor.gcode_execute(self.x_slider.value, self.y_slider.value)

    def on_reset(self, instance):
        # Update the CNC machine based on the slider values
        self.x_slider.value=0
        self.y_slider.value=0
        print(f'X-Axis value: {self.x_slider.value}, Y-Axis value: {self.y_slider.value}')

    # Define a function to run when the up arrow button is clicked
    def move_up(self, instance):
        print("Moving up...")
        increment = float(increment_input.text())
        command = f"G0 Y{increment}\n"
        ser.write(command.encode())

    # Define a function to run when the down arrow button is clicked
    def move_down(self, instance):
        print("Moving down...")
        increment = float(increment_input.text())
        command = f"G0 Y{-increment}\n"
        ser.write(command.encode())

    # Define a function to run when the left arrow button is clicked
    def move_left(self, instance):
        print("Moving left...")
        increment = float(increment_input.text())
        command = f"G0 X{-increment}\n"
        ser.write(command.encode())

    # Define a function to run when the right arrow button is clicked
    def move_right(self, instance):
        print("Moving right...")
        increment = float(increment_input.text())
        command = f"G0 X{increment}\n"
        ser.write(command.encode())


        #  # Create a box layout
        # self.orientation='vertical'

        # # Create the CNC control buttons
        # up_button = Button(text='UP', font_size='30sp')
        # down_button = Button(text='DOWN', font_size='30sp')
        # left_button = Button(text='LEFT', font_size='30sp')
        # right_button = Button(text='RIGHT', font_size='30sp')

        # # Create a text input field for the COM port
        # com_port_input = TextInput(hint_text='COM port', size_hint=(None, None),
        #                            size=(200, 50), font_size='20sp')

        # # Add the buttons and text input field to the layout
        # self.add_widget(up_button)
        # self.add_widget(BoxLayout(size_hint_y=None, height=10))
        # self.add_widget(BoxLayout(orientation='horizontal', size_hint_y=None, height=50,
        #                              padding=10, spacing=10, 
        #                              children=[left_button, down_button, right_button]))
        # self.add_widget(BoxLayout(size_hint_y=None, height=10))
        # self.add_widget(com_port_input)

        # # Set GridLayout properties
        # self.cols = 3
        # self.rows = 3

        # # Add up button
        # self.add_widget(Label())
        # self.add_widget(Button(text='UP', font_size=25, size_hint_y=0.5))
        # self.add_widget(Label())

        # # Add left and right buttons
        # self.add_widget(Button(text='LEFT', font_size=25,size_hint_y=0.5))
        # self.add_widget(Label())
        # self.add_widget(Button(text='RIGHT', font_size=25,size_hint_y=0.5))

        # # Add down button
        # self.add_widget(Label())
        # self.add_widget(Button(text='DOWN', font_size=25,size_hint_y=0.5))
        # self.add_widget(Label())
