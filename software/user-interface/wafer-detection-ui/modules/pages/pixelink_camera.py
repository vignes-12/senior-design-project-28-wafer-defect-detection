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
from functools import partial

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
        # ret = PxLApi.initialize(0)
        # print(ret[0])
        # hCamera = ret[1]
        
        #PxLApi.uninitialize(hCamera)
        # fig,ax = plt.subplots()
        # canvas = fig.canvas
        fig = plt.figure(figsize=(16, 15))
        ax = fig.add_subplot(111)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        self.livecam = FigureCanvasKivyAgg(plt.gcf())
        self.add_widget(self.livecam)
        # self.add_widget(fig)
        data = get_temp_image(PxLApi.ImageFormat.JPEG)

        file = open("test.jpeg", "wb")
        file.write(data)
        file.close()
        im = Image.open("test.jpeg")
        window = plt.imshow(im)
        plt.ion()
        #plt.show()
        try:
            Clock.schedule_interval(partial(self.update_continue, plt, window), 0.01)
        except:
            print("Camera is busy")


    def update_continue(self, plt, window, *largs):
        # print('Continuous frame grabbing started...')
        if(UPDATE_CAMERA):
            data = get_temp_image(PxLApi.ImageFormat.JPEG)
        #im = Image.frombuffer('L', cam.size, data)
        file = open("test.jpeg", "wb")
        file.write(data)
        file.close()
        im = Image.open("test.jpeg")
        window.set_data(im)
        plt.draw()
        plt.pause(0.001)
            
        