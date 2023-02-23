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
    command = input("serial command:")
    command += '\n'
    if ("end" in command):
        break
    ser1.write(command.encode())
    time.sleep(1)
    
ser1.close()