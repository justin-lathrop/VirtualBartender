"""
" @author: Justin Lathrop
"
" @param: Checks directory 'Orders' 
" for list of drinks to make. Steps 
" to make drink are included inside
" of drink order file in JSON format.
" If Admin folder contains any
" commands then they will be done
" first.
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
import json

orderDir = './Orders'
completedDir = './OrdersCompleted'
adminDir = './Admin'
serialDevice = '/dev/ttyACM0'
baudRate = '115200'

"""
" Marks current order as complete 
" by removing it from the orderDir 
" and appending it inside the 
" completedDir.
" 
" @return: True if success and 
" False if error.
"""
def markOrderComplete():
	orders = os.listdir(orderDir)
	if len(orders) > 0:
		# Save the current order
		orders.sort()
		orderName = orders[0]
		orderContents = json.load(open(orderDir + '/' + orders[0]))
		
		# Delete current order from order directory
		os.remove(orderDir + '/' + orderName)
		
		# Put current order into completed directory
		newFile = open(completedDir + '/' + orderName, 'w')
		newFile.write(json.dumps(orderContents))
		newFile.close()
		
		return True
	return False


"""
" Checks the 'Orders' directory
" and gets the next order within
" it.  If no orders are found 
" then it will wait until an 
" order is filled.  Will check 
" periodically (5 seconds) until 
" an order is placed.
"
" @param: String <order directory>
" 
" @return: order object if there is 
" another order in the queue else 
" return null.
"""
def getNextOrder():
	orders = os.listdir(orderDir)
	if len(orders) > 0:
                orders.sort()
                return json.load(open(orderDir + '/' + orders[0]))
        else:
                return False


"""
" Fills the order of a drink and 
" is in charge of sending commands 
" to Arduino to process.
" 
" @param: Order <order> which holds 
" all of the drinks information 
" needed to create it.
" 
" @return: True is successful and 
" False by default if unsuccessful.
"""
def fillOrder(order, ser):
	print 'Filling order <' + order['title'] + '>'
	
	ser.write('A')
	response = ser.read()
        print 'response ' + response
	
	time.sleep(3)
	return True


"""
" Checks to see if there are any
" admin commands to do.
"
" @return: True is folder is not
" empty else False if it is.
"""
def admin():
        commands = os.listdir(adminDir)
        if len(commands) > 0:
                return True
        else:
                return False

"""
" Speaks to arduino for admin
" simply printing out what
" the arduino responds with
" for testing purposes.
"""
def fillAdminReq(ser):
        commands = os.listdir(adminDir)
        
        for el in commands:
                print 'Processing command ' + el
                if el == 'Turn_Tray.command':
                        ser.write('T')
                        response = ser.read()
                        print 'Arduino responded with ' + response
                elif el == 'Mix_Drink.command':
                        ser.write('M')
                        response = ser.read()
                        print 'Arduino responded with ' + response
                elif el == 'Dispense_Drink_A.command':
                        ser.write('A')
                        response = ser.read()
                        print 'Arduino responded with ' + response
                elif el == 'Dispense_Drink_B.command':
                        ser.write('B')
                        response = ser.read()
                        print 'Arduino responded with ' + response
                else:
                        print 'Command Unknown'

                os.remove(adminDir + '/' + el)


def main():
	print 'Initializing Controller'
	ser = serial.Serial(serialDevice, baudRate)
	time.sleep(5)
	ser.flush()
	ser.flushInput()
	ser.flushOutput()
	print 'Initialization Complete'
	print

	# Loop forever filling orders
	while 1:
                if admin():
                        fillAdminReq(ser)
                else:
                        currentOrder = getNextOrder()
                        if currentOrder != False:
                                if fillOrder(currentOrder, ser):
                                        markOrderComplete()
                                        print 'Order complete'
                                else:
                                        print 'Failed to make order'
		time.sleep(2)
	print 'Controller exited'

if __name__ == '__main__':
	main()
