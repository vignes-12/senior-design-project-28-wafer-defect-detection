import serial
import io
import time
import csv
# Camera Python script
from CameraCode import *
# Uncomment this line
# ser1 = serial.Serial('COM3', 115200)
# Comment this line during test
from modules.utils.popup import *


# global ser1


class GCodeExecutor(object):

    ser1 = serial.Serial

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
        inp = self.input_wafer_size
        print(inp)
        run = True
        #while(run):
            #inp = input("Input your wafer size in in (s x s): ")
        dimension = int(inp) * 2.54
        fov = 7
        
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

        x_steps = int(w_move / fov)
        y_steps = int(l_move / fov)
        total_images = x_steps * y_steps

        with open('auto_run.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([x_start, y_start, x_steps, y_steps, total_images, fov])

        file.close

        
    def continue_auto(self):
        with open('auto_run.csv', 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            for row in reader:
                x_start = int(row[0])
                y_start = int(row[1])
                x_steps = int(row[2])
                y_steps = int(row[3])
                total_images = int(row[4])
                fov = row[5]

        print(x_start)
        print(y_start)
        print(x_steps)
        print(y_steps)
        print(total_images)
        print(fov)
     
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
        
        print("focus and press continue to begin sequence, q to quit")
        #ser1.write(('G90\n').encode())
        #  if('q' in inp):
        #     exit()
        #break
        picture = 0    
        for y in range(y_steps):
            for x in range(x_steps):
                picture += 1 
                save_image(picture)
                
                command = "G0 X"
                if(y%2 == 1):
                    command += "-" + str(fov)
                else:
                    command += str(fov)
                print(command)
                command += "\n"
                ser1.write(command.encode())
                
                #time.sleep(0.3)
            
            picture += 1 
            save_image(picture)
            command = "G0 Y-" + str(fov) +"\n"
            print(command)
            ser1.write(command.encode())
            #time.sleep(0.3)
