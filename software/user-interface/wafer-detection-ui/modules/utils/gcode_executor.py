import serial
import io
import time
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
        run = True;
        #while(run):
            #inp = input("Input your wafer size in cm (s x s): ")
        dimension = int(inp)
        
        w_move = dimension * 10
        l_move = dimension * 10
        
        print("performing homing procedure...verify starting coordinates:")
        
        x_start = 200 - w_move/2 - 25
        y_start = 200 + l_move/2 + 40
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
        command = "G0 X" + str(x_start) + " Y" + str(y_start)
        print(command)
        command += "\n"
        ser1.write(command.encode())
        time.sleep(8)

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
        for y in range(l_move):
            for x in range(w_move):
                picture += 1 
                save_image(picture)
                
                command = "G0 X"
                if(y%2 == 1):
                    command += "-1"
                else:
                    command += "1"
                print(command)
                command += "\n"
                ser1.write(command.encode())
                
                #time.sleep(0.3)
                
            command = "G0 Y-1\n"
            print(command)
            ser1.write(command.encode())
            time.sleep(0.3)