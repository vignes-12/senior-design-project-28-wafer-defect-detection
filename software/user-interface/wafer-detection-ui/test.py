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

from pixelink import PixeLINK, PxLerror


data = []
im = Image
torun = True

def grab_frames(cam, plt, window):
    frame_num = 0
    time_start = time.time()
    
    while torun:
        frame_num += 1
        try:
            data = get_temp_image(cam, PxLApi.ImageFormat.JPEG)
            #print(data)
            file = open("test.jpeg", "wb")
            file.write(data)
            file.close()
            im = Image.open("test.jpeg")
            window.set_data(im)
            plt.draw()
            # TODO: do something with the data...
        except PxLerror as exc:
            print('ERROR: grab_frames:', str(exc))
            continue
        t_total = time.time() - time_start
        if frame_num % 10 == 0:
            frame_rate = float(frame_num) / t_total
            print('#%04d FPS: %0.3f frames/sec' % (frame_num, frame_rate))


def main():
    ret = PxLApi.initialize(0)
    print(ret[0])
    hCamera = ret[1]
    #retVal = get_temp_image(hCamera, PxLApi.ImageFormat.JPEG)
    #cam = PixeLINK()
    #cam.shutter = 0.043329  # exposure time in seconds
    #cam.roi = [1776, 1284, 1920, 1080]  # 0,0,2208,3000
    #cam.white_shading = [2.29, 1, 1.5]
    #cam.resolution 
    data = get_temp_image(hCamera, PxLApi.ImageFormat.JPEG)
    #im = Image.frombuffer('L', cam.size, data)
    file = open("test.jpeg", "wb")
    file.write(data)
    file.close()
    im = Image.open("test.jpeg")
    window = plt.imshow(im)
    print('Continuous frame grabbing started...')
    plt.ion()
    plt.show()
    # th = threading.Thread(target=grab_frames, args=[hCamera, plt, window])
    # th.start()
    
    
    try:
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
            
    except KeyboardInterrupt:
        print('Caught CTRL+C')
    finally:
        print('Closing camera...')
        torun = False
        print('Waiting for thread...')
        #th.join()
        print('Done.')

if __name__ == '__main__':
    main()