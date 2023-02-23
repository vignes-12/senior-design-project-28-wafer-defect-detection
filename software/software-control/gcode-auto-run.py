import serial
import time  

ser1 = serial.Serial('COM3', 115200)
time.sleep(1)

run = True;

#ser1.write(('G28 X Y\n').encode())
#time.sleep(10)

#ser1.write(('G0 X100 Y100\n').encode())
#time.sleep(1)

while(run):
    inp = input("Input your wafer size in cm (s x s): ")
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
                

while(run):
    command = input("serial command:")
    command += '\n'
    if ("end" in command):
        break
    ser1.write(command.encode())
    time.sleep(1)
    
ser1.close()