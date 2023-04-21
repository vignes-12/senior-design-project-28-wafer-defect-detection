from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from pixelink import PixeLINK
from pixelink import PxLapi
from pixelink import PxLerror
from pixelink import *
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

from matplotlib import pyplot as plt
from PIL import Image
from matplotlib import pyplot as plt
  
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg



class PixelinkCamera(BoxLayout):
    launched = False
    def __init__(self, **kwargs):
        super(PixelinkCamera, self).__init__(**kwargs)
        # Create a BoxLayout widget to contain the camera preview
        self.orientation = 'vertical'

    def update_continue():
        ret = PxLApi.initialize(0)
        print(ret[0])
        hCamera = ret[1]
        data = get_temp_image(hCamera, PxLApi.ImageFormat.JPEG)
        #im = Image.frombuffer('L', cam.size, data)
        file = open("test.jpeg", "wb")
        file.write(data)
        file.close()
        fig,ax = plt.subplots()
        canvas = fig.canvas
        im = Image.open("test.jpeg")
        window = ax.imshow(im)
        print('Continuous frame grabbing started...')
        plt.ion()
        self.add_widget(canvas)
        plt.show()
        # th = threading.Thread(target=grab_frames, args=[hCamera, plt, window])
        # th.start()
        
        # adding plot to kivy boxlayout
        while True:
            #time.sleep(1.0)
            data = get_temp_image(hCamera, PxLApi.ImageFormat.JPEG)
            #print(data)
            file = open("test.jpeg", "wb")
            file.write(data)
            file.close()
            im = Image.open("test.jpeg")
            window.set_data(im)
            plt.draw()
            plt.pause(0.001)
            