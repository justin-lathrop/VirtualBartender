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
"       - 'P' => Parallel dispensing
"           <7 bytes -> array of servings>
"           <1 byte -> amount>
"       - 'R' => Reset tray
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
import operator

orderDir = './Orders'
completedDir = './OrdersCompleted'
adminDir = './Admin'
serialDevice = '/dev/ttyACM0'
baudRate = '115200'
drinks = {"Cherry": '0', "Orange": '1', "Grape": '2',
          "Lemonade": '3', "Strawberry": '4', "RaspberryLemonade": '5',
          "TropicalPunch": '6'}
drinkNames = ["Cherry", "Orange", "Grape", "Lemonade", "Strawberry",
              "RaspberryLemonade", "TropicalPunch"]
emergState = False


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


def listDone(List, val):
    """
    " Will check if all elements values in
    " the list are the same.
    "
    " @param: list, val
    "
    " @return: boolean
    """
    for x in List:
        if int(x['amount']) != val:
            return False
    return True


def smallestDrinkAmount(List):
    """
    " Given a list of drinks
    " find the smallest of the
    " amounts and return it.
    "
    " @param: List of drinks
    "
    " @return: int smallest amount
    """
    # 9 is the max amount for a drink
    # serving size
    amount = 9
    
    for d in List:
        if int(d['amount']) < amount:
            amount = int(d['amount'])
    return amount


def updateDrinkAmounts(List, amount):
    """
    " Will subtract the smallest
    " amount from each item in
    " the list unless the item's
    " amount is already equal to
    " zero or less.
    "
    " @param: List of drinkItems, and
    "   int of amount to subtract.
    "
    " @return: Updated List
    """
    for i in List:
        if int(i['amount']) > 0:
            print "Update Drink Amounts: "
            print "before " + i['amount']
            i['amount'] = str( int(i['amount']) - amount )
            print "after " + i['amount']
    return List


def getAmount(name, List):
    """
    " Finds the drink name in the List
    " and returns amount value.
    "
    " @param: string drink name,
    "   List of drinks
    "
    " @return: Int amount
    """
    for d in List:
        if d['drink'] == name:
            return int(d['amount'])
    return 0


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


    while not listDone(order['drinkList'], 0):
        count = 0
        msg = ''
        amount = 0
        strDrinks = str(order['drinkList'])

        for index, d in enumerate(drinks):
            if count >= 3:
                msg = msg + '0'
            else:
                if (drinkNames[index] in strDrinks) and (getAmount(drinkNames[index], order['drinkList']) > 0):
                    msg = msg + '1'
                    count = count + 1
                else:
                    msg = msg + '0'

        amount = smallestDrinkAmount(order['drinkList'])
        order['drinkList'] = updateDrinkAmounts(order['drinkList'], amount)
        msg = 'P' + msg + str(amount)
        ser.write(msg)
        
        print "Command Arduino to:"
        print "> Dispense Liquid in Parallel"
        print "> " + msg

        serIn = readSerial(ser)
        print "Arduino Reponse:"
        print "> " + serIn
        print
        print
        if emergState:
            print
            print "!!!! EMERGENCY BEGIN !!!!"
            print "Skipping current drink..."
            print "Will wait until Go button pressed..."
            print "!!!! EMERGENCY FINISH !!!!"
            print
            return False

    """# Loop through all drinks in list
    for d in order['drinkList']:
        if not emergState:
            ser.write('L')
            print 'L,'
            ser.write(drinks[ d['drink'] ])
            print drinks[ d['drink'] ] + ','
            ser.write(d['amount'])
            print d['amount']
            print
        
            print "Command Arduino to:"
            print "> Dispense Liquid " + d['drink']
            print "> Amount " + d['amount']

            serIn = readSerial(ser)
            print "Arduino Reponse:"
            print "> " + serIn
            print
            print
            if emergState:
                print
                print "!!!! EMERGENCY BEGIN !!!!"
                print "Skipping current drink..."
                print "Will wait until Go button pressed..."
                print "!!!! EMERGENCY FINISH !!!!"
                print
                return False
        else:
            return False"""

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
    if emergState:
        print
        print "!!!! EMERGENCY BEGIN !!!!"
        print "Skipping current drink..."
        print "Will wait until Go button pressed..."
        print "!!!! EMERGENCY FINISH !!!!"
        print
        return False

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
    serIn = ser.read()

    if serIn == '!':
        emergState = True
        return serIn
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
                    
                        numDrinks = numDrinks + 1
                        print '\n\nOrder complete\n\n'

                        """# Get confirmation to start next drink
                        ser.write('B')
                        while ser.read() != '!':
                            time.sleep(0.5)"""
                    else:
                        # Wait until user says to begin serving again
                        print "\nWaiting for user go button...\n"
                        while ser.read() != '!':
                            time.sleep(0.5)

                        # Reset environment since Emergency happened
                        numDrinks = 0
                        markOrderComplete()
                        print "Failed to make order"
                        print "Reseting Environment"
                        print
                        print "Command Arduino to:"
                        print "> Reset Tray"
                        ser.write('R')
                        serIn = serialRead()
                        print
                        print "Arduino Response:"
                        print "> " + serIn
                            
                        
                        
            if numDrinks >= 6:
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
                    print "\n\nError getting user button press\n\n"
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
