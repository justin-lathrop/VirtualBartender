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
import json

orderDir = './Orders'
completedDir = './OrdersCompleted'
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
		newFile.write(orderContents)
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
	orders = []
	while 1:
		orders = os.listdir(orderDir)
		if len(orders) > 0:
			orders.sort()
			break;
		else:
			time.sleep(5)
	return json.load(open(orderDir + '/' + orders[0]))


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
	print 'Filling order <' + order + '>'
	
	#ser.write('A');
	
	time.sleep(3)
	return True


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
		currentOrder = getNextOrder()
		if fillOrder(currentOrder, ser):
			markOrderComplete(currentOrder)
			print 'Order complete'
		else:
			print 'Failed to make order'
		time.sleep(2)
	print 'Controller exited'

if __name__ == '__main__':
	main()
