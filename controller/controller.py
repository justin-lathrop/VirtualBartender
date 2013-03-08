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

orderDir = 'Orders'
completedDir = 'OrdersCompleted'
recipeDir = '../server/drinks/'
serialDevice = '/dev/ttyACM0'
baudRate = '115200'

"""
" Holds all data needed for 
" each step for a specific 
" drink.
"""
class step:
	def __init__(self, code):
		self.codeNum = code

"""
" Holds all the steps needed 
" and commands for arduino to 
" process each step.
"""
class order:
	def __init__(self, drinkName):
		self.drinkName = drinkName
		self.steps = []

	def addStep():
		"""  """

"""
" Checks the 'Orders' directory
" and gets the next order within
" it.
"
" @param: String <order directory>
" 
" @return: order object if there is 
" another order in the queue else 
" return null.
"""
def getNextOrder():
	print os.listdir(orderDir)
	return

def main():
	print 'Initializing Controller'

	ser = serial.Serial(serialDevice, baudRate)
	time.sleep(5)
	ser.flush()
	ser.flushInput()
	ser.flushOutput()

	print 'Initialization Complete'
	print

	getNextOrder()

if __name__ == '__main__':
	main()
