import serial
import io
import time

# Uncomment this line
# ser1 = serial.Serial('COM3', 115200)
# Comment this line during test
global ser1


class GCodeExecutor(object):

    def connect_serial(self):
        port = self.port_input
        baudrate = 115200

        try:
            ser1 = serial.Serial(port, baudrate)
            print(f"Connected to {port}")
            
        except:
            print("Connection failed")
                       

    def gcode_write(self, command):
        print(f'Writing command {command}')
        ser1.write(b"{command}")

                
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
        while(run):
            #inp = input("Input your wafer size in cm (s x s): ")
            if ("end" in inp):
                break
            dimension = int(inp)
            
            w_move = dimension * 10
            l_move = dimension * 10
            
            print("performing homing procedure...verify starting coordinates:")
            
            x_start = 200 - w_move/2
            y_start = 200 + l_move/2
            print("x_start: ")
            print(x_start)
            print("y_start: ")
            print(y_start)
            
            ser1.write(('G90\n').encode())
            ser1.write(('G28 X Y\n').encode())
            time.sleep(5)
            
            command = "G0 X" + str(x_start) + " Y" + str(y_start)
            print(command)
            command += "\n"
            ser1.write(command.encode())
            time.sleep(5)
            
            ser1.write(('G91\n').encode())
            
            inp = input("press any key to begin sequence, q to quit")
            if('q' in inp):
                exit()
            
            for y in range(l_move):
                for x in range(w_move):
                    command = "G0 X"
                    if(y%2 == 1):
                        command += "-1"
                    else:
                        command += "1"
                    print(command)
                    command += "\n"
                    ser1.write(command.encode())
                    time.sleep(0.3)
                command = "G0 Y-1\n"
                print(command)
                ser1.write(command.encode())
                time.sleep(0.3)