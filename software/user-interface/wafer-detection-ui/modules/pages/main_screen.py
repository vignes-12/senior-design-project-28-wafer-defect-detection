from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial

Builder.load_string('''
<MainScreen>:
    MDFloatingActionButtonSpeedDial:
        data: app.buttons
        rotation_root_button: True
        rotation: True
        hint_animation: True
        hint_animation_scale: True
        hint_text_color: 1, 1, 1, 1
        root_button_anim_delay: 0
        root_button_anim_duration: 0.15
        label_text_color: 1, 1, 1, 1
        color_icon_root_button: 1, 1, 1, 1
        color_icon_stack_button: 1, 1, 1, 1
        bg_hint_color: 0, 0, 0, 1
        tooltip_text_color: 1, 1, 1, 1
''')

class MainScreen(Screen):
    buttons = [
        {
            "icon": "arrow-left-bold",
            "text": "Left",
            "tooltip": "Go left",
        },
        {
            "icon": "arrow-right-bold",
            "text": "Right",
            "tooltip": "Go right",
        },
        {
            "icon": "arrow-up-bold",
            "text": "Up",
            "tooltip": "Go up",
        },
        {
            "icon": "arrow-down-bold",
            "text": "Down",
            "tooltip": "Go down",
        },
    ]
