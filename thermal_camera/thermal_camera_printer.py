try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
from time import sleep
import serial
from math import fabs
import numpy as np
import os
camera = serial.Serial('/dev/ttyUSB2',115200,timeout=None)
printer = serial.Serial('/dev/ttyUSB0',250000,timeout=None)

pixel_size = 10
size_x = 10
size_y = 4

max_size_y = 300

printer_x_home = 70
printer_y_home = 80
printer_x = printer_x_home
printer_y = printer_y_home
printer_x_step = 12.5
printer_y_step = 5.24
printer_x_travel = 100

printer_y_travel = 100
x_offset = 0

total_buffer = []

initclass=Tk()
Writeclass=Canvas(initclass)
Writeclass.place(x=0,y=0,height=(max_size_y*pixel_size+1500),width=(size_x*pixel_size+1500))
initclass.geometry(str(size_x*pixel_size+1500) + 'x' + str(max_size_y*pixel_size+1500))
# print('Homing Printer')
# printer.write(b"G28\n")
# printer.readline()
# print('Raising Printer')
# printer.write(b"G00 X0 Y0 Z30\n")
# printer.readline()
input_buffer = []
printer.write(b"G00 X" + str(printer_x) +" Y"+str(printer_y)+'\n')
sleep(5)
while(printer_x < printer_x_travel+printer_x_home):
    #os.system('clear')
    print((printer_x/(printer_x_travel+printer_x_home))*100)
    print("Percent complete.")
    camera.reset_input_buffer()
    input_buffer = []
    while(not input_buffer or len(input_buffer) < 52):
        try:
            input_string = camera.readline().split(',')[:-1]
            input_buffer = [float(str(i)) for i in input_string]
            print(len(input_buffer))
        except:
            pass
    formatted_buffer = [input_buffer[i:i+4] for i in range(0, len(input_buffer), 4)]

    for idx,val in enumerate(formatted_buffer):
        if(idx+x_offset > len(total_buffer)-1):
            total_buffer.append(val)
        else:
            total_buffer[idx+x_offset] += val
    # size_y += 4
    # if(size_y > max_size_y):
    #     size_y = 4
    #     total_buffer = []
    # sleep(1)
    printer_y += printer_y_step
    size_y+=4
    if(printer_y > printer_y_home+printer_y_travel):
        printer_y = printer_y_home
        printer_x += printer_x_step
        size_x += 10
        x_offset += 10
        printer.write(b"G00 X" + str(printer_x) +" Y"+str(printer_y)+'\n')
        sleep(5)
    printer.reset_input_buffer()
    printer.write(b"G00 X" + str(printer_x) +" Y"+str(printer_y)+'\n')
    sleep(0.3)
print("Processing...")
while(True):
    Writeclass.delete("all")
    for x in range(0,size_x):
        os.system('clear')
        print("Processing...")
        print((x/size_y)*100)
        print("Percent complete.")
        for y in range(0,size_y):
            max_val = max([item for sublist in total_buffer for item in sublist])
            min_val = min([item for sublist in total_buffer for item in sublist])
            try:
                current_temp = (((total_buffer[x][y])-min_val)/(max_val-min_val))
                Writeclass.create_rectangle(x*pixel_size, y*pixel_size, x*pixel_size+pixel_size, y*pixel_size+pixel_size, fill=("#%02x%02x%02x" % ((current_temp*255), 0, abs(255-(current_temp*255)))))
            except:
                pass
    Writeclass.update()
    sleep(10000000)
mainloop()
