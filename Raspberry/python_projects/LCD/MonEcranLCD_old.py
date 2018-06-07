

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

#from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
DHTPin = 11     #define the pin of DHT11
TempCPU = 0.0
TempExt = 0.0
HumExt = 0.0
state_LCD = False
old_state_LCD = False
dht = DHT.DHT(DHTPin)   #create a DHT class object

def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.1f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
	
def destroy_LCD():
	lcd.clear()
	mcp.output(3,0)     # turn on LCD backlight

def init_DHT():
	dht = DHT.DHT(DHTPin)   #create a DHT class object

def loop_DHT():
	chk = dht.readDHT11() 
	if (chk is dht.DHTLIB_OK):  
		global TempExt
		TempExt = dht.temperature
		HumExt = dht.humidity
		#print"Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature)   	
		
def init_LCD():
	mcp.output(3,1)     # turn on LCD backlight
	lcd.begin(16,2)     # set number of LCD lines and columns

def loop_LCD():
	global TempExt
	lcd.setCursor(0,0)  # set cursor position
	message =  get_cpu_temp() + ' - {:.1f}'.format( float(TempExt)) + ' C'
	lcd.message( message + '\n' )# display CPU temperature
	lcd.message( get_time_now() )   # display the time
	#print(TempExt)
	#print(message)

def loop():
    state_LCD = True
    old_state_LCD = False
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    while(True):         
		if (state_LCD == True) and (old_state_LCD == False):
			#Il faut initialiser
			init_LCD()
		if (state_LCD == True):
			loop_DHT()
			loop_LCD()
		if ((state_LCD == False) and (old_state_LCD == True)):
			destroy_LCD()
		old_state_LCD = state_LCD
		time.sleep(1)	

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print 'I2C Address Error !'
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
	print 'Program is starting ... '
	state_LCD = False
	old_state_LCD = False
	init_DHT()
    	try:
		state_LCD = True
		old_state_LCD = False
        	loop()
	except KeyboardInterrupt:
		destroy_LCD()
        	GPIO.cleanup()
        	exit()  	
