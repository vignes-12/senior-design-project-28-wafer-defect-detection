from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pixelink import PixeLINK
from pixelink import PxLapi
from pixelink import PxLerror
from kivy.clock import Clock
import os
import threading
import struct
import time
from kivy.graphics.texture import Texture
import cv2


class PixelinkCamera(BoxLayout):
     launched = False
     def __init__(self, **kwargs):
        super(PixelinkCamera, self).__init__(**kwargs)
        # Create a BoxLayout widget to contain the camera preview
        self.orientation = 'vertical';

        # Create a Pixelink camera object
        self.cam = PixeLINK()

        # Set camera settings
        self.cam.streaming = True
        self.cam.shutter = 0.001
        self.cam.roi = [0, 0, 1000, 1000]  # 0,0,2208,3000

        # Create an Image widget to display the camera preview
        self.image = Image(allow_stretch=True)

        # Add the Image widget to the BoxLayout
        self.add_widget(self.image)

        Clock.schedule_interval(self.update_image, 1.0 / 30.0)
        

        def update_image(self, dt):
            th = threading.Thread(target=self.grab_continuous, args=[self.cam])
            # th = threading.Thread(target=self.grab_continuous, args=[cam])
            th.start()

        def grab_continuous(self, cam):
            frame_num = 0
            while cam.is_open():
                time_0 = time.time()
                frame_num += 1
                try:
                    data = cam.grab()
                    # use opencv to convert img
                    img = cv2.cvtColor(data, cv2.COLOR_BAYER_GR2RGB)
                    buf1 = cv2.flip(img, 0)
                    buf = buf1.tobytes()
                    # add image to self.image.texture here
                    texture = self.image.texture
                    texture.blit_buffer(
                        buf, colorfmt='rgb', bufferfmt='ubyte')
                    self.image.texture = texture
                except PxLerror as exc:
                    print('ERROR: grab_continuous:', str(exc))
                    continue
                t_dif = time.time() - time_0
                if data is not None:
                    print('#: %d, %0.3f sec, shape: %s, mean: %0.3f, std: %0.3f'
                        % (frame_num, t_dif, repr(data.shape), data.mean(), data.std()))
                time.sleep(0.001)

