#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
from purdue_print_func import purdue_print 

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Pin Definition
pin = 26

# Set up GPIO 26 as an input with an internal pull-down resistor
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

purdue_print()

print("Boeing Wind Tunnel Monitoring Program has been initiated.\n \
Purdue University, School of Aeronautics and Astronautics.\n \
All rights reserved. \n \
Designed in Summer 2025 \n \
Waiting for power signal on GPIO",pin)
print("... (Press CTRL+C to exit)")
starttime = datetime.now()

print("Program start time:",starttime)

i = 0;

try:
    past_state = GPIO.input(pin)
    while True:
        current_state = GPIO.input(pin)
        
        if current_state == GPIO.HIGH and past_state == GPIO.LOW:
            print("Power detected! Running emailer script to send emails to point of contacts...")
            print("The tunnel is currently ON")
            subprocess.run(["python3","/home/aslbwtpi/Desktop/rpi_wt/email_invoke.py"])
            past_state = current_state
            starttime = datetime.now()
            i = 0
            
        elif current_state == GPIO.LOW:
            past_state = GPIO.LOW
            now = datetime.now()
            delta = now - starttime
            total_seconds = int(delta.total_seconds())
            days, remainder = divmod(total_seconds,86400)
            hours, remainder = divmod(remainder,3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"The tunnel is turned off, waiting for power signal since, {days} day(s), {hours} hour(s), {minutes} min(s), {seconds} second(s)")
            i = i + 1;
            time.sleep(1)
            if i%10 == 0:
                purdue_print()  
            

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    GPIO.cleanup()  # Reset GPIO settings
