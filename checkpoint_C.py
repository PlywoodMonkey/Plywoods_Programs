
##last updated: Feb 8, 2023 

## this is the code that accomplishes all requirments of checkpoint c

## import statments for necesary libraries
import sys
sys.path.append('/home/group-11/Group-11/python_scripts/.')
import RPi.GPIO as GPIO
import rgb1602
import time
import digi_pot 
import control_digipot
import pigpio as pi

## allows us to use the BCM/GPIO naming convention
GPIO.setmode(GPIO.BCM)

## declares and intiializes constants
lcd = rgb1602.RGB1602(16,2) ## for lcd
digiPotChosen = False
backToMain = False
digiPot = 0

# Define and intialize keys
lcd_key = 0
key_in = 0

clk = 18 #clk for RE
dt = 22 #dt for RE
switch = 27 #switch for RE
counter = 0

#sets the state of the GPIO pins to either take IN a signal (GPIO.IN) or OUTPUT a signal (GPIO.OUT)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#returns the value being read from the rotary encoder
GPIO.input(switch)

'''callback function for switch press interrupt'''
def digipot_callback(channel) :
    global digiPotChosen
    global backToMain
    
    ## sets var to true which stops loop in main program
    digiPotChosen = True
    
def startProgram():
    
    lcd.clear()
        
    ## displays "select digipot:" on row one
    lcd.setCursor(0,0)
    lcd.printout("Mode Select:")
    lcd.setCursor(0,1)
    lcd.printout(" 1. Func Gen")
    time.sleep(1)
    
'''main program'''
def main():
    ## begins while loop
    global digiPotChosen
    digiPotChosen = False
    buttonPress = False ##need to define somewhere else
    digiPot = 0
    lcd.cursor_on()
    #lcd.blink()
    
    ## creates interrupt for detecting button press
    GPIO.add_event_detect(switch, GPIO.FALLING, callback = digipot_callback, bouncetime = 50)
    
    while True:
        lcd.clear()
        
        ## displays "select digipot:" on row one
        lcd.setCursor(0,0)
        lcd.printout("Select digitpot: ")

        ## displays digitpot options "P0   P1" to choose on row 2
        lcd.setCursor(0,1)
        lcd.printout("*P0       *P1")

        ## Set cursor on second row
        lcd.setCursor(0,1)
        
        ## loop runs until digipot is chosen
        while digiPotChosen == False :
             ##declaring and intializing constants and vars
            clkLastState = GPIO.input(clk)
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)       
                
            if clkState != clkLastState:
                
                '''turned clockwise'''
                if dtState != clkState:
                    ##move cursor to P1
                    digiPot = 1
                    lcd.setCursor(10,1)
                    print("clockwise")
                else:
                    '''turned counterclockwise'''
                    ## move cursor to P0
                    digiPot = 0
                    lcd.setCursor(0,1)
                    print("counterclockwise")
                    
            clkLastState = clkState
        
        ##checks which digipot was chosen and invokes corresponding method 
        if digiPot == 0:
            digi_pot.digipot_zero(switch)
            digiPot = 2
            time.sleep(1)
            break

        elif digiPot == 1:
            digi_pot.digipot_one(switch)
            digiPot = 2
            time.sleep(1)
            break
    
    GPIO.remove_event_detect(switch)
    
try:  
    ## initializing digiots to 5000 Ohms
    control_digipot.controlPot1(5000)
    control_digipot.controlPot0(5000)
    
    startProgram()
    
    while(True):
      main()
      
except KeyboardInterrupt:
    GPIO.cleanup()

    ## use a bunch of if statements here

  ## once digitpot is chosen, do the following -->
    ## display the following "Change value of" + "PO" or "P1"
      ## displays current value resistance value selected e.g. "100 Ohms"
