## this has code related to functions for choosing and  accessing digipot

from RPi import GPIO
from time import sleep

import sys
sys.path.append('/home/group-11/Group-11/python_scripts/.')
import RPi.GPIO as GPIO
import rgb1602
import time
import control_digipot
import pigpio as pi

## intializing values
clk = 18
dt = 22
switch = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
lcd = rgb1602.RGB1602(16,2)
counter = 0
clkLastState = GPIO.input(18)

''' defines set of instructions for setting digitpot_one value of resistance'''
def digipot_one(switch) :
    lcd.setCursor(0,0)
    lcd.clear()
    lcd.printout("Turn Knob To")
    lcd.setCursor(0,1)
    lcd.printout("Select Pot Val")
    time.sleep(1.5)
    lcd.setCursor(0,0)
    lcd.clear()
    lcd.printout("Select Val P1: ")
    lcd.setCursor(0,1)
    lcd.printout("5000  Ohms")
    #time.sleep(1)
    turnDigiPot(18, 22, 1)
    
    print("returned")
    return
    
    ##implement return to main

''' defines set of instructions for setting digipot_zero value of resistance'''
def digipot_zero(switch) :
    lcd.setCursor(0,0)
    lcd.clear()
    lcd.printout("Turn Knob To")
    lcd.setCursor(0,1)
    lcd.printout("Select Pot Val")
    time.sleep(1.5)
    lcd.setCursor(0,0)
    lcd.clear()
    lcd.printout("Select Val P0: ")
    lcd.setCursor(0,1)
    lcd.printout("5000  Ohms")
    #time.sleep(1)
    turnDigiPot(18, 22, 0)
    
    print("returned")
    
    ##code for returning to main loop
   
    #code for setting up digipot  
def turnDigiPot(clk, dt, potNum):
    digiVal = 0
    #starts the time for to determine the speed of the rotary encoder's turning
    
    clkLastState = GPIO.input(18)
    counter = 0
    changeInValue = 5000
    oldValue = 5000
    newValue = 5000
    timeSinceLast = -1

    #gets the inputs of the clk and dt states

    while True:
        
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        
        #checks if there has been a change in state
        if (clkState != clkLastState and dtState == 1):
            
            startTimeTurnDigiPot = timeSinceLast
            timeSinceLast = time.time()
            
            #if so, calculates the speed of the turning
            timeTakenToSpin = (time.time() - startTimeTurnDigiPot)
            startTimeTurnDigiPot = time.time()
            #startTimeTurnDigiPlot = time.time() #resets the clock
                        
            #if the speed is fast, does below statement
            if (timeTakenToSpin < .1):
                if (dtState != clkState):
                    changeInValue += 100
                    if (changeInValue > 10000): #ensures that the value does not go above 10000
                        changeInValue = 10000     
                    print(changeInValue)
                else: #(dtState == clkState and clkState != 1):
                    changeInValue -= 100
                    if (changeInValue < 100): #ensures that the value does not go below 100
                        changeInValue = 100
                    print(changeInValue)
                newValue = changeInValue
        #if the speed is slow, does below statement
            else:
                if (dtState != clkState):
                    changeInValue += 10
                    if (changeInValue > 10000): #ensures that the value does not go above 10000
                        changeInValue = 10000
                    print(changeInValue)
                else:
                    changeInValue -= 10
                    if (changeInValue < 100): #ensures that the value does not go below 100
                        changeInValue = 100
                    print(changeInValue)
                newValue = changeInValue
                
        clkLastState = clkState # updates state for next loop

        time.sleep(.001)
        
        if (newValue != oldValue):
            lcd.setCursor(0,1)
            lcd.printout("      ")
            lcd.setCursor(0,1)
            lcd.printout(changeInValue)
            lcd.setCursor(6,1)
            lcd.printout("Ohms")
        
        oldValue = newValue
        
        #Checks if a button got pushed
        if (GPIO.input(27) == GPIO.LOW):
            if (holdButton(27) == True):
                #button held: return to main
                lcd.clear()
                lcd.printout("Returning to")
                lcd.setCursor(0,1)
                lcd.printout("Select Screen...")
                return #back to main
                
                ## release pigpio resources
                pi.stop()
            else:
                #button pressed: select value of digiPot
                print("Value Set")
                print(changeInValue)
                
                ## check which digipot was selected
                if (potNum == 1) :
                    ## invoke control digi
                    control_digipot.controlPot1(newValue)
                    
                elif (potNum == 0) :
                    ## invoke control digi
                    control_digipot.controlPot0(newValue)
                    
                ## sleep program to prevent immediately changing value after setting it   
                time.sleep(0.25)
                
def sendResisToDigiPot(counter):
    #Takes the number given by the user and transforms it into a number with the usuable steps of the digiPot
    
    #declares variables
    stepConstant = 38.91
    remainder = 0
    digiPotResistance = 0
    
    #finds the number of times that the 38.91 doesnt go into the given number
    remainder = counter % stepConstant
    digiPotResistance = counter // stepConstant # does floor division
    
    #either ceilings or floors the remainder
    if (remainder >= .5000001):
        digiPotResistance += 1

            
    if (digiPotResistance > 10000):
        return 9999.87
    elif (digiPotResistance < 100):
        return 116.73
    else:
        return digiPotResistance
            
def holdButton(switch):
       
    startTimeHoldButton = 0
    buttonHeld = 2 ## holds value of when button is held -->True, otherwise False
    
    # User presses in select button
    while GPIO.input(switch) == GPIO.LOW   :
        startTimeHoldButton = time.time()
        #print(start)

        #user continues holding select button
        while GPIO.input(switch) == GPIO.LOW   :
            endTimeHoldButton = time.time()
            

            #user lets go of select button
            if GPIO.input(switch) == GPIO.HIGH :

                #total time is ended and calculated
                total = endTimeHoldButton - startTimeHoldButton
                print(total)

                #if time is more than 3 seconds, backs out
                if total >= 3  :
                    print("Button Held")
                    return True ##True if button held for 3 seconds or more     
                else :
                    print("Button Pressed")
                    return False
                    
                
    return buttonHeld ##False for button not being held longer than 3 sec
