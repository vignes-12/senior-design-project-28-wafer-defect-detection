import gc

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button

from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import ObjectProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from modules.dashboard import MainDashboard

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar

from kivy.uix.spinner import Spinner
from kivy.clock import Clock



gc.disable()

KV = '''
<ContentNavigationDrawer>:

    ScrollView:

        MDList:

            OneLineListItem:
                text: "Controls UI"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "controls"

            OneLineListItem:
                text: "Wafer Map"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "wafer_map"
            
            OneLineListItem:
                text: "Others"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "others"


Screen:

    MDTopAppBar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Dashboard"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            Screen:
                name: "controls"

                MainDashboard:
                    launched: True
            
            Screen:
                name: "wafer_map"

                MDLabel:
                    text: "Screen 2"
                    halign: "center"
            
            Screen:
                name: "others"

                MDLabel:
                    text: "Screen 3"
                    halign: "center"
            

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def __init__(self, **kwargs):
        super(ContentNavigationDrawer, self).__init__(**kwargs)

        # Create the spinner and hide it initially
        self.spinner = Spinner(size_hint=(None, None), size=(50, 50))
        self.spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.spinner.active = False
        self.add_widget(self.spinner)

        # Schedule a function to simulate loading content after 2 seconds
        Clock.schedule_once(self.load_content, 2)
    
    def load_content(self, *args):
        # Show the spinner and start loading content
        self.spinner.active = True
        
        # Load content here
        
        # Hide the spinner when loading is complete
        self.spinner.active = False

class MainApp(MDApp):


    def build(self):
        #change App colors here
        self.title = 'Wafer Detection GUI'
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '300'
        self.theme_cls.accent_palette = 'Gray'
        self.theme_cls.accent_hue = '800'
        self.theme_cls.theme_style = 'Dark'
        self.accent_color = [255/255, 64/255, 129/255, 1]

        return Builder.load_string(KV)
    
  

if __name__ == "__main__":
    MainApp().run()