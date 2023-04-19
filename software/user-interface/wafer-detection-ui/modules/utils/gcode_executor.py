import serial
import io
import time
import os
import csv
from math import ceil
from modules.utils.vignes_test import processor
# Camera Python script
from CameraCode import *
# Uncomment this line
# ser1 = serial.Serial('COM3', 115200)
# Comment this line during test
from modules.utils.popup import *


# global ser1


class GCodeExecutor(object):

    ser1 = serial.Serial
    #self.proc = processor()

    def connect_serial(self, port):
        #port = self.port_input
        baudrate = 115200

        try:
            global ser1
            ser1 = serial.Serial(port, baudrate)
            print(ser1)
            print(f"Connected to {port}")            
        except:
            display_error(2)
                       

    def gcode_write(self, command):
        print(f'Writing command {command}')
        
        print(ser1)
        ser1.write(command.encode())
        
        

                
    # def gcode_move(self, x, y):
    #     return 'G01 X{:.3f} Y{:.3f}\n'.format(x, y)

    # def gcode_execute(self,x, y):
    #     command = self.gcode_move(x, y)
    #     print(command)
    #     ser1.write(command.encode())

    def run_auto(self):

        self.directory += '\\'
        print(self.directory)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            print("creating directory")

        inp = self.input_wafer_size
        print(inp)
        run = True
        #while(run):
            #inp = input("Input your wafer size in in (s x s): ")
        dimension = int(inp) * 2.54
        x_fov = 12
        y_fov = 12*9/16
        
        w_move = dimension * 10
        l_move = dimension * 10
        
        print("performing homing procedure...verify starting coordinates:")
        
        x_start = int(165 - w_move/2)
        y_start = int(280 + l_move/2)
        print("x_start: ")
        print(x_start)
        print("y_start: ")
        print(y_start)
        
        ser1.write(('G28 X Y\n').encode())
        time.sleep(10)
################################################################################################################ You should be able to screenshot things 
## That is the function call 
## Please put it where it will stop or when you want to take a picture 
        # Picture += 1 
        # save_image()    
################################################################################################################
        
        command = "G90\n"
        ser1.write(command.encode())
        
        command = "G0 X170 Y280\n"
        ser1.write(command.encode())
        time.sleep(8)

        x_steps = ceil(w_move / x_fov)
        y_steps = ceil(l_move / y_fov)
        total_images = x_steps * y_steps

        with open(self.directory + 'auto_run.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x_start, y_start, x_steps, y_steps, total_images, x_fov, y_fov])

        file.close

        print(x_start)
        print(y_start)
        print(x_steps)
        print(y_steps)
        print(total_images)
        print(x_fov)
        print(y_fov)

        
    def continue_auto(self):
        
        self.directory += '\\'
        print(self.directory)    

        with open(self.directory + 'auto_run.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in reader:
                x_start = int(row[0])
                y_start = int(row[1])
                x_steps = int(row[2])
                y_steps = int(row[3])
                total_images = int(row[4])
                x_fov = (row[5])
                y_fov = row[6]

        print(x_start)
        print(y_start)
        print(x_steps)
        print(y_steps)
        print(total_images)
        print(x_fov)
        print(y_fov)
     
        command = "G90\n"
        ser1.write(command.encode())
        command = "G0 X" + str(x_start) + " Y" + str(y_start)
        print(command)
        command += "\n"
        ser1.write(command.encode())
        time.sleep(2)

        # command = "G90\n"
        # ser1.write(command.encode())
        # command = "G0 Z-150\n"
        # ser1.write(command.encode())
        
        ser1.write(('G91\n').encode())
        
        #print("focus and press continue to begin sequence, q to quit")
        #ser1.write(('G90\n').encode())
        #  if('q' in inp):
        #     exit()
        #break
        picture = 1 
        save_image(self.directory, picture)   
        for y in range(y_steps):
            for x in range(x_steps-1):
                command = "G0 X"
                if(y%2 == 1):
                    command += "-" + str(x_fov)
                else:
                    command += str(x_fov)
                print(command)
                command += "\n"
                ser1.write(command.encode())
                picture += 1 
                save_image(self.directory, picture)
                #time.sleep(0.3)
            command = "G0 Y-" + str(y_fov) +"\n"
            print(command)
            ser1.write(command.encode())
            if(y != y_steps-1):
                picture += 1 
                save_image(self.directory, picture)
            #time.sleep(0.3)

        self.proc = processor()
        self.proc.IMG_DIR = self.directory
        self.proc.process_data()
