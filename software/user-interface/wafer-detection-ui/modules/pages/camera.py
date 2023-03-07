'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# import threading

# Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
import time



Builder.load_string('''
<CameraUI>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
        allow_stretch: True
        #on_error: root.handle_camera_error(*args)
               
    ToggleButton:
        text: 'Start/Stop'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraUI(BoxLayout):
    launched = False

    def toggleCamera(self):
        camera = self.ids['camera']
        
        if camera.play:
            camera.stop()
        else:
            camera.play = True

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''

        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
       
        print("Captured")
    
    # def handle_camera_error(self, instance, value):
    #     self.ids.status_label.text = 'Failed to start camera: ' + str(value)
    #     self.ids.camera.play = False