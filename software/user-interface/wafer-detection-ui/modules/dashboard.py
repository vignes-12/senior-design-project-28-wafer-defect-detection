from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from modules.pages.camera import CameraUI
from modules.pages.motor_controls import MotorControls
from modules.pages.input_controls import InputControls
from kivy.uix.camera import Camera
from modules.pages.main_screen import MainScreen

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
import time



Builder.load_string('''
<MainDashboard>:
    # cols: 2    
    # Camera:
    #     id: camera
    #     resolution: (640, 480)
    #     play: False     
    # # Create a BoxLayout to hold two buttons
    # BoxLayout:
    #     orientation: 'horizontal'
    #     Button:
    #         text: 'Button 1'
    #     Button:
    #         text: 'Button 2'

    
    orientation: 'horizontal'

    # Create a grid layout for the camera preview
    GridLayout:
        cols: 2
        size_hint_y: 0.9
        CameraUI:
            launched: True
        InputControls:
            launched: True
        # MainScreen:
       
            
''')


class MainDashboard(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)