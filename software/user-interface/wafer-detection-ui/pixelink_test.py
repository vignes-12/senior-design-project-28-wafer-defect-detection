from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.core.image import Image as CoreImage
from pixelink import PixeLINK
from pixelink import PxLapi
from pixelink import PxLerror
from pixelink import *
import pixelink
from kivy.core.image import Image as CoreImage
from pixelinkWrapper import *
from io import BytesIO

from kivy.clock import Clock
import os
import threading
import struct
import time
from kivy.graphics.texture import Texture
import cv2
from CameraCode import *

class PixelinkApp(App):
    def build(self):
        # Create a BoxLayout widget to contain the camera preview
        boxlayout = BoxLayout()

        self.cam = PixeLINK()
        self.cam.open_first()
        self.cam.set_roi(1776, 1284, 1920, 1080)
        self.cam.set_exposure_time(0.043329)

        self.cam.resolution(1920, 1080)
        self.cam.start_stream()

        boxlayout.add_widget(self.cam)

        # Create a Pixelink camera object
        # cam = PixeLINK()
        # cam2 = PxLapi()

        # # Set camera settings
        # cam.streaming = True
        # cam.shutter = 0.07665
        # # Uncomment to just test the camera
        # # while cam.is_open():
        # #     data = cam.grab()
        # #     if data is not None:
        # #         print('#: shape: %s, mean: %0.3f, std: %0.3f'
        # #             % (repr(data.shape), data.mean(), data.std()))
        
        # # data = cam.grab()
        # # cam.binning = [2, 0]
        # cam.roi = [1776, 1284, 1920, 1080]  # 0,0,2208,3000
        # cam2.SetFeature(cam, 3, 4)
        # cam2.SetFeature(cam, 7, 4)
        # cam.white_shading = [2.29, 1, 1.5]
        #         #FEATURE_FLAG_AUTO



        # file = open("test.jpeg", "wb")
        # numBytesWritten = file.write(retVal)
        # file.close()

        # self.src = "test.jpeg"
        # self.image = Image(source="test.jpeg")


        #im = CoreImage(BytesIO(retVal), ext='png')
        
        # # Create an Image widget to display the camera preview
        



        # # Initialize the texture with a dummy size
        # self.image.texture = Texture.create(size=(1, 1))

        # # Update the Image widget with the camera preview image
        # # Update the Image widget with the camera preview image
        # th = threading.Thread(target=self.grab_continuous, args=[hCamera])
        # th.start()
        # def update_image(dt):
            
        #     # th = threading.Thread(target=self.grab_continuous, args=[self.cam])
            
        #     time_0 = time.time()
        #     # cam.streaming = False
        #     t_dif = 0.0

        # #Clock.schedule_interval(update_image, 5)

        # Add the Image widget to the BoxLayout
        # boxlayout.add_widget(self.image)

        return boxlayout
    
    def grab_continuous(self, cam):
        while(True):
            print("run")
            retVal = get_temp_image(cam, PxLApi.ImageFormat.JPEG)

            file = open("test.jpeg", "wb")
            file.write(retVal)
            file.close()

            self.image.reload()
        


        # frame_num = 0
        # while cam.is_open():
        #     time_0 = time.time()
        #     frame_num += 1
        #     try:
        #         data = cam.grab()
        #         # use opencv to convert img
        #         img = cv2.cvtColor(data, cv2.COLOR_BAYER_GR2RGB)
        #         buf1 = cv2.flip(img, 0)
        #         buf = buf1.tobytes()
        #         # add image to self.image.texture here
        #         texture = self.image.texture
        #         if texture is None:
        #             # texture = Texture.create(size=(cam.width, cam.height), colorfmt='rgb')
        #             height, width = data.shape
        #             channels = 1
        #             texture = Texture.create(size=(width, height), colorfmt='rgb')
        #             self.image.texture = texture
        #         texture.blit_buffer(
        #             buf, colorfmt='rgb', bufferfmt='ubyte')
        #         self.image.texture = texture
        #     except PxLerror as exc:
        #         print('ERROR: grab_continuous:', str(exc))
        #         continue
        #     t_dif = time.time() - time_0
        #     if data is not None:
        #         # print('#: %d, %0.3f sec, shape: %s, mean: %0.3f, std: %0.3f'
        #             # % (frame_num, t_dif, repr(data.shape), data.mean(), data.std()))
        #         time.sleep(0.001)



if __name__ == '__main__':
    PixelinkApp().run()