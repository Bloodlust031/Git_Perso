

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

#from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
import os

GPIO.setwarnings(False)                                               # Mettre sur OFF les alertes (qui sont inutiles)
GPIO.setmode(GPIO.BOARD)                                                # BCM : Numero des GPIO (GPIO 18)
GPIO.setup(22, GPIO.OUT)                                              # Definition du port en sortie
GPIO.output(22, True)                                             # Mise a zero du GPIO 18 (GND)

DHTPin = 11     #define the pin of DHT11
buttonPin = 18	# define the buttonPin-GPIO24
buttonPinRed = 15	# define the buttonPin-GPIO24
TempCPU = 0.0
TempExt = 0.0
HumExt = 0.0
state_LCD = False
old_state_LCD = False
state_Red = 0
state_Red_counter = 0
mcp = 0
lcd = 0
LedOnCounter  = 0
dht = DHT.DHT(DHTPin)   #create a DHT class object

def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.1f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
	
def destroy_LCD():
    global lcd
    global mcp
    lcd.clear()	
    mcp.output(3,0)     # turn off LCD backlight

def buttonEvent(channel):
    global state_LCD 
    global state_Red
    global state_Red_counter
    #print('buttonEvent GPIO %d' %(channel))
    
    if (state_Red == 0):
	state_LCD = not state_LCD 
	if state_LCD : 
	    print('Turn on LCD Green... ')
	else : 
	    print('Turn off LCD Green... ') 
    elif(state_Red == 1):
	state_Red = 2
	state_Red_counter = 0
    elif(state_Red == 2):
	state_Red = 3
	state_Red_counter = 0
    
def buttonRedEvent(channel):
    global state_Red
    global state_Red_counter 
    global state_LCD

    if (state_Red == 0):
	state_Red = 1
	state_Red_counter = 0
	if state_LCD == False:
		allum_LCD()
        else:
                lcd.clear()
    elif(state_Red == 1):
	#annulation
	state_LCD = True
	state_Red = 0
	state_Red_counter = 0
        lcd.clear()
        state_LCD = True
        old_state_LCD = True
	LedOnCounter = 3540	#pour que l'ecran ne reste allume qu'une minute
    elif(state_Red == 2):
	state_Red = 4
	state_Red_counter = 0
    
def init_btn():
    global state_Red
    global state_Red_counter    
    state_Red = 0
    state_Red_counter = 0    
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set buttonPin's mode is input, and pull up to high
    GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback = buttonEvent,bouncetime=300)
    
    GPIO.setup(buttonPinRed, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set buttonPin's mode is input, and pull up to high
    GPIO.add_event_detect(buttonPinRed,GPIO.FALLING,callback = buttonRedEvent,bouncetime=300)

def init_DHT():
    dht = DHT.DHT(DHTPin)   #create a DHT class object

def loop_DHT():
    global TempExt
    global dht
    global chk
    global HumExt
    
    chk = dht.readDHT11() 
    if (chk is dht.DHTLIB_OK):  
	global TempExt
	TempExt = dht.temperature
	HumExt = dht.humidity
	#print"Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature)   	
		
def init_LCD():
    global lcd
    global mcp
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    try:
	mcp = PCF8574_GPIO(PCF8574_address)
    except:
	try:
	    mcp = PCF8574_GPIO(PCF8574A_address)
	except:
	    print('I2C Address Error !')
	    exit(1)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    
    
def allum_LCD():
    global lcd
    global mcp
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

def loop_LCD():
    global lcd
    global mcp
    global TempExt
    lcd.setCursor(0,0)  # set cursor position
    message =  get_cpu_temp() + ' - {:.1f}'.format( float(TempExt)) + ' C'
    lcd.message( message + '\n' )# display CPU temperature
    lcd.message( get_time_now() )   # display the time
    #print(TempExt)
    #print(message)

def loop():
    global state_LCD
    global old_state_LCD
    global LedOnCounter
    global state_Red
    global state_Red_counter        
    global lcd

    while(True):       
	if (state_Red_counter > 5):
	    state_Red = 0
	    state_Red_counter = 0
            lcd.clear()
            state_LCD = True
            old_state_LCD = True
	    LedOnCounter = 3540	#pour que l'ecran ne reste allume qu'une minute
	if (state_Red > 0):
	    state_Red_counter = state_Red_counter + 1
	    if state_Red ==1:
		lcd.setCursor(0,0)  # set cursor position
		lcd.message( "Confirm    Abort" + '\n' )# display CPU temperature
		message = "%s" % (6-state_Red_counter)
		lcd.message( message )		
	    elif state_Red ==2:
		lcd.setCursor(0,0)  # set cursor position
		lcd.message( "Reboot  shutdown" + '\n' )# display CPU temperature
		message = "%s" % (6-state_Red_counter)
		lcd.message( message )
	    elif state_Red ==3:
		print('Reboot')
		os.system('sudo reboot')
	    elif state_Red ==4:
		print('Shutdown')
		os.system('sudo shutdown -h now')
	else:
	    if (LedOnCounter > 3600):
		state_LCD = False
	    if (state_LCD == True) and (old_state_LCD == False):
		#Il faut initialiser
		allum_LCD()
	    if (state_LCD == True):
		loop_DHT()
		loop_LCD()
		LedOnCounter  = LedOnCounter  + 1
	    if ((state_LCD == False) and (old_state_LCD == True)):
		destroy_LCD()
	    if (state_LCD == False):
		LedOnCounter  = 0
	    old_state_LCD = state_LCD
	time.sleep(1)	

if __name__ == '__main__':
    init_LCD()
    init_DHT()
    init_btn()
    try:
	loop()
    except KeyboardInterrupt:
	destroy_LCD()
	GPIO.cleanup()
	exit()  	
	GPIO.output(25, False)
