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

class PixelinkApp(App):
    def build(self):
        # Create a BoxLayout widget to contain the camera preview
        boxlayout = BoxLayout()

        # Create a Pixelink camera object
        cam = PixeLINK()

        # Set camera settings
        cam.streaming = True
        cam.shutter = 0.001
        # Uncomment to just test the camera
        # while cam.is_open():
        #     data = cam.grab()
        #     if data is not None:
        #         print('#: shape: %s, mean: %0.3f, std: %0.3f'
        #             % (repr(data.shape), data.mean(), data.std()))
        
        # data = cam.grab()
        # cam.binning = [2, 0]
        cam.roi = [0, 0, 1000, 1000]  # 0,0,2208,3000
        # cam.roi = [0, 0, 2208, 3000]  # 0,0,2208,3000

        # Create an Image widget to display the camera preview
        self.image = Image()

        # Initialize the texture with a dummy size
        self.image.texture = Texture.create(size=(1, 1))

        # Update the Image widget with the camera preview image
        # Update the Image widget with the camera preview image
        def update_image(dt):
            
            # th = threading.Thread(target=self.grab_continuous, args=[self, cam])
            th = threading.Thread(target=self.grab_continuous, args=[cam])
            th.start()
            time_0 = time.time()
            # cam.streaming = False
            t_dif = 0.0

        Clock.schedule_interval(update_image, 1.0/30.0)

        # Add the Image widget to the BoxLayout
        boxlayout.add_widget(self.image)

        return boxlayout
    
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
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.image.texture = texture

            except PxLerror as exc:
                print('ERROR: grab_continuous:', str(exc))
                continue
            t_dif = time.time() - time_0
            if data is not None:
                print('#: %d, %0.3f sec, shape: %s, mean: %0.3f, std: %0.3f'
                    % (frame_num, t_dif, repr(data.shape), data.mean(), data.std()))
            time.sleep(0.001)


if __name__ == '__main__':
    PixelinkApp().run()