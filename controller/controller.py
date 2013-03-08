"""
" @author: Justin Lathrop
"
" @param: Checks directory 'Orders' 
" for list of drinks to make. Steps 
" to make drink are in 'Recipes'
" directory ('\n' delimmited).
" Commnunicates to Arduino through
" Serial and gets responses:
"   Responses:
"       - '0' => error
"       - '1' => success
"       - '2' => unknown command
"   Commands:
"       - 'A' => Rotate Tray
"       - 'B' => Dispense Liquid <number>
"       - 'C' => Dispense Liquid <number>
"       - ...
" When order is completed the drink
" item will be erased from 'Orders'
" directory and put into the 'Finished'
" directory.
" 
" @return:
"   - errors => stdout
"   - other => stdout
"""

import serial
import time
import os

"""
" Checks the 'Orders' directory
" and gets the next order within
" it.
"
" @param: String <order directory>
" 
" @return: String <filename> on
" success and String 'No Orders'
" when no orders left and 'Error'
" when error accurs.
"""
def getNextOrder(dir):
    os.listdir(dir)
    return

def main():
    print 'Initializing Controller'

    orderDir = 'Orders'
    completedDir = 'OrdersCompleted'
    serialDevice = '/dev/ttyACM0'
    baudRate = '115200'
    ser = serial.Serial(serialDevice, baudRate)
    time.sleep(5)
    ser.flush()
    ser.flushInput()
    ser.flushOutput()

    print 'Initialization Complete'
    print
    
    

if __name__ == '__main__':
    main()
