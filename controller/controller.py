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
" Serial:
"   Responses:
"       - '0' => Error
"       - '1' => Success
"       - '2' => Unknown command
"       - '!' => Confirm/Emergency
"   Commands:
"       - 'L' => Dispense Liquid
"           <liquid number> <servings>
"       - 'T' => Move Tray
"           <number of spots to move>
"       - 'D' => Move down mixer
"       - 'U' => Move up mixer
"       - 'B' => Wait for start button
" When order is completed the drink
" item will be erased from 'Orders'
" directory and put into the 'Finished'
" directory, then controller will wait
" until arduino start button is pressed.
" 
" @return:
"   - errors => stdout
"   - other => stdout
"   - logging => logs.log (current dir)
"""

import serial
import time
import os
import json
import traceback
import sys

orderDir = './Orders'
completedDir = './OrdersCompleted'
adminDir = './Admin'
serialDevice = '/dev/ttyACM0'
baudRate = '115200'
drinks = {"A": '0', "B": '1', "C": '2',
          "D": '3', "E": '4', "F": '5',
          "G": '6'}


def markOrderComplete():
    """
    " Marks current order as complete 
    " by removing it from the orderDir 
    " and appending it inside the 
    " completedDir.
    " 
    " @return: True if success and 
    " False if error.
    """
    orders = os.listdir(orderDir)
    if len(orders) > 0:
        # Save the current order
        orders.sort()
        orderName = orders[0]
        orderContents = json.load(open(orderDir + '/' + orders[0]))

	# Delete current order from order directory
        os.remove(orderDir + '/' + orderName)

	# Put current order into completed directory
        newFile = open(completedDir + '/' + str(time.time()) + '_' + orderName, 'w')
        newFile.write(json.dumps(orderContents))
        newFile.close()

        return True
    return False


def getNextOrder():
    """
    " Checks the 'Orders' directory
    " and gets the next order within
    " it.
    "
    " @return: order object if there is 
    " another order in the queue else 
    " return False.
    """
    orders = os.listdir(orderDir)
    if len(orders) > 0:
        orders.sort()
        return json.load(open(orderDir + '/' + orders[0]))
    else:
        return False


def fillOrder(order, ser):
    """
    " Fills the order of a drink and 
    " is in charge of sending commands 
    " to Arduino to process.
    " 
    " @param: Order <order> which holds 
    " all of the drinks information 
    " needed to create it. Serial
    " reference in order to commuincate
    " to the Arduino.
    " 
    " @return: True is successful and 
    " False if unsuccessful.
    """
    print 'Filling order <' + order['title'] + '>'

    # Loop through all drinks in list
    for d in order['drinkList']:
        ser.write('L')
        print 'L,'
        ser.write(drinks[ d['name'] ])
        print drinks[ d['name'] ] + ','
        ser.write(d['amount'])
        print d['amount']
        print
        
        print "Command Arduino to:"
        print "> Dispense Liquid " + d['name']
        print "> Amount " + d['amount']

        serIn = ser.read()

        print "Arduino Response:"
        print "> " + serIn
        print
        print

    # Wait for liquid to clear tubes
    time.sleep(5)

    # Turn tray to next position
    print "Command Arduino to:"
    print "> Move tray 1 position"

    ser.write('T')
    ser.write('1')
    serIn = ser.read()

    print "Arduino Response:"
    print "> " + serIn
    print
    print

    return True


def admin():
    """
    " Checks to see if there are any
    " admin commands to do.
    "
    " @return: True is folder is not
    " empty else False if it is.
    """
    commands = os.listdir(adminDir)
    if len(commands) > 0:
        return True
    else:
        return False


def fillAdminReq(ser):
    """
    " Speaks to arduino for admin
    " simply printing out what
    " the arduino responds with
    " for testing purposes.
    """
    commands = os.listdir(adminDir)
        
    for el in commands:
        print 'Processing command ' + el
        if el == 'Turn_Tray.command':
            ser.write('T')
            ser.write('1')
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


def readSerial(ser):
    """
    " Reads serial input
    " from the Arduino and then
    " checks the input for errors
    " or an emergency state.  If
    " emergency state occurs then
    " abort current drink and wait
    " for emergency state to end.
    "
    " @param: configured Serial obj
    "
    " @return: input char
    """
    while 1:
        serIn = ser.read()

        if serIn == '!':
           time.sleep(2)
        else:
            return serIn

def main():
    try:
        print 'Initializing Controller'
        numDrinks = 0
        ser = serial.Serial(serialDevice, baudRate)
        time.sleep(2)
        ser.flush()
        ser.flushInput()
        ser.flushOutput()

        # Wait until start button is pressed
        while ser.read() != '!':
            time.sleep(0.5)
    
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
                    
                        #numDrinks = numDrinks + 1
                        print '\n\nOrder complete\n\n'

                        # Get confirmation to start next drink
                        ser.write('B')
                        while ser.read() != '!':
                            time.sleep(0.5)
                    else:
                        print '\n\nFailed to make order\n\n'
            """if numDrinks >= 6:
                print "Six drinks have been made"
                print "Command Arduino to:"
                print "> Get start button press"
                ser.write('B')
                serIn = ser.read()
                if serIn == '1':
                    print "Arduino Response:"
                    print "> " + serIn
                    numDrinks = 0
                    print "\nDrink count zeroed out\n"
                else:
                    print "\n\nError getting user button press\n\n"""
            time.sleep(2)
        print '\n\nController exited\n\n'
    except KeyboardInterrupt:
        print
        print 'Closing Serial Port'
        ser.close()
        print
        print 'Exiting...'
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)



if __name__ == '__main__':
    main()
