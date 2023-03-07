from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
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

from modules.utils.stitch_image_snake_func import stitch_images_snake 

Builder.load_string('''
<MainControls>:
    
    orientation: "vertical"
    spacing: "12dp"
    size_hint_x: .6
    pos_hint: {"center_x": .5, "center_y": .3}
    adaptive_height: True

    MDBoxLayout:
        orientation: 'vertical'
        TwoLineListItem:
            text: "open the file"
            icon_left: "folder"
            md_bg_color: "white"
            on_release: root.file_manager_open() 

    MDTextField:
        id: directory_field
        icon_left: "file"
        mode: "round"
        hint_text: "Directory Path"
        normal_color: .8, .8, .8, 1
        color_active: .9, .9, .9, 1
        -height: "42dp"
    
    MDTextField:
        id: folder_name_field
        icon_left: "folder"
        mode: "round"
        hint_text: "Folder Name"
        normal_color: .8, .8, .8, 1
        color_active: .9, .9, .9, 1
        -height: "42dp"

    MDTextField:
        id: image_name_field
        icon_left: "image"
        mode: "round"
        hint_text: "Image Name"
        normal_color: .8, .8, .8, 1
        color_active: .9, .9, .9, 1
        -height: "42dp"

    MDTextField:
        id: xval_field
        icon_left: "location"
        mode: "round"
        hint_text: "X Value"
        normal_color: .8, .8, .8, 1
        color_active: .9, .9, .9, 1
        -height: "42dp"
    
    MDTextField:
        id: yval_field
        icon_left: "location"
        mode: "round"
        hint_text: "Y Value"
        normal_color: .8, .8, .8, 1
        color_active: .9, .9, .9, 1
        -height: "42dp"

    MDGridLayout:
        id: box
        cols: 2
        spacing: "12dp"
        padding: "12dp"
        adaptive_height: True

        MDFillRoundFlatButton:
            text: "RUN AUTO"
            size_hint: None, None
            pos_hint: {"center_x": .5}
            on_press: root.on_run_auto()
        
        MDFillRoundFlatButton:
            text: "RUN SCAN"
            size_hint: None, None
            pos_hint: {"center_x": .5}
            on_press: root.on_run_scan()
       
            
''')

my_path = "/"               

class MainControls(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MainControls, self).__init__(**kwargs)
        
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
           # previous=True,
        )

    def file_manager_open(self):
        self.file_manager.show(my_path)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
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
    
    def on_run_auto(self, *args):
        print('Inside on_run_auto function...')
        

    
    def on_run_scan(self):
        print('Inside on_run_scale function...')
        print(self.ids.directory_field.text)
        print(self.ids.folder_name_field.text)
        stitch_images_snake(self.ids.directory_field.text, 
                            self.ids.folder_name_field.text, 
                            self.ids.image_name_field.text,
                            self.ids.xval_field.text,
                            self.ids.yval_field.text,)


        