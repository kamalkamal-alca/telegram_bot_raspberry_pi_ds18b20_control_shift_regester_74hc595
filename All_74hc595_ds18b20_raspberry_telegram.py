
import datetime 
import telepot  
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO
from time import sleep      
from w1thermsensor import W1ThermSensor
import subprocess

sensor = W1ThermSensor()

# EXACTLY the same setup as your working Flask code
GPIO.setmode(GPIO.BCM)
dataPin  = 24  # Pin for Data (GPIO 24)
latchPin = 23  # Pin for Latch (GPIO 23)
clockPin = 18  # Pin for Clock (GPIO 18)

GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)

# Variables - EXACTLY the same as Flask code
shift_data = 0b00000000  # Initial state of the shift register (all LEDs off)
previous_shift_data = 0b00000000

# Function to update shift register - EXACTLY the same as Flask code
def update_shift_register():
    global shift_data, previous_shift_data
    if shift_data != previous_shift_data:
        previous_shift_data = shift_data
        GPIO.output(latchPin, GPIO.LOW)
        shift_out(shift_data)
        GPIO.output(latchPin, GPIO.HIGH)

# Shift out data - EXACTLY the same as your working Flask code
def shift_out(data):
    for i in range(8):
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.output(dataPin, (data >> (7 - i)) & 0x01)
        GPIO.output(clockPin, GPIO.HIGH)

def handle(msg):
    global shift_data
    
    chat_id = msg['chat']['id']
    command = msg['text']
    print('Received command:', command)

    # Get current time for time/date commands
    now = datetime.datetime.now()

    # Temperature reading (keep it simple)
    temp_c = sensor.get_temperature()
    temp_C = str(round(temp_c))
    temp_F = str(round(float(temp_c)*1.8+32, 1))

    # Command handling - SIMPLIFIED to match Flask approach
    if command == '/help':
        bot.sendMessage(chat_id, "LED commands:\n/ledon1, /ledoff1\n/ledon2, /ledoff2\n/ledon3, /ledoff3\n/ledon4, /ledoff4\n\nOther commands:\n/hi, /time, /date, /temp, /humi")
    
    elif command == '/hi':
        bot.sendMessage(chat_id, "HELLO KAMAL.., bot is online")
    
    elif command == '/time':
        bot.sendMessage(chat_id, f"Time: {now.hour}:{now.minute}:{now.second}")
    
    elif command == '/date':
        bot.sendMessage(chat_id, f"Date: {now.day}/{now.month}/{now.year}")

    # LED CONTROL - EXACTLY the same logic as your Flask routes
    elif command == '/ledon1':
        shift_data |= 0b00000001  # Turn LED1 on - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 1 ON")
        print(f"LED1 ON - Shift data: {bin(shift_data)}")
    
    elif command == '/ledoff1':
        shift_data &= 0b11111110  # Turn LED1 off - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 1 OFF")
        print(f"LED1 OFF - Shift data: {bin(shift_data)}")
    
    elif command == '/ledon2':
        shift_data |= 0b00000010  # Turn LED2 on - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 2 ON")
        print(f"LED2 ON - Shift data: {bin(shift_data)}")
    
    elif command == '/ledoff2':
        shift_data &= 0b11111101  # Turn LED2 off - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 2 OFF")
        print(f"LED2 OFF - Shift data: {bin(shift_data)}")
    
    elif command == '/ledon3':
        shift_data |= 0b00000100  # Turn LED3 on - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 3 ON")
        print(f"LED3 ON - Shift data: {bin(shift_data)}")
    
    elif command == '/ledoff3':
        shift_data &= 0b11111011  # Turn LED3 off - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 3 OFF")
        print(f"LED3 OFF - Shift data: {bin(shift_data)}")
    
    elif command == '/ledon4':
        shift_data |= 0b00001000  # Turn LED4 on - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 4 ON")
        print(f"LED4 ON - Shift data: {bin(shift_data)}")
    
    elif command == '/ledoff4':
        shift_data &= 0b11110111  # Turn LED4 off - SAME as Flask
        update_shift_register()
        bot.sendMessage(chat_id, "LED 4 OFF")
        print(f"LED4 OFF - Shift data: {bin(shift_data)}")

    # Other simple commands
    elif command == '/temp':  
        bot.sendMessage(chat_id, f"Temperature: {temp_C}*C")
    
    elif command == '/humi':  
        bot.sendMessage(chat_id, f"Temperature: {temp_F}*F")
    
    elif command == '/usb':
        try:
            p = subprocess.Popen("lsusb", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            bot.sendMessage(chat_id, str(p.decode('utf-8')))
        except Exception as e:
            bot.sendMessage(chat_id, f"Error: {e}")
    
    else:
        bot.sendMessage(chat_id, "Unknown command. Type /help for available commands.")

# Initialize the shift register to known state
update_shift_register()

# Bot setup
bot = telepot.Bot('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
print(bot.getMe())

MessageLoop(bot, handle).run_as_thread()
print('GPIO-TEL 2.00 at your service...')

# Main loop - SIMPLE like Flask
try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
