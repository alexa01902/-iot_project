

import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Conversions between binary data and various encodings
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
from machine import Pin, ADC      # Define pin
from lib import aio_configuration as aio
import dht 
import ntptime  
import utime

ldr = ADC(Pin(27))
redLed = Pin(7, Pin.OUT)
tempSensor = dht.DHT11(Pin(16))     # DHT11 Constructor 
yellowLed = Pin(11, Pin.OUT)
greenLed = Pin(15, Pin.OUT)

DATA_INTERVAL = 60*15 # seconds

def send_data(darkness, temperature, humidity):
    try:
        global DATA_INTERVAL
        
        print("Publishing: {0} to {1} ... ".format(temperature, aio.AIO_TEMP_FEED), end='')

        try:
            client.publish(topic=aio.AIO_TEMP_FEED, msg=str(temperature))
            print("DONE")
        except Exception as e:
            print("FAILED")

        print("Publishing: {0} to {1} ... ".format(humidity, aio.AIO_HUMIDITY_FEED), end='')
        try:
            client.publish(topic=aio.AIO_HUMIDITY_FEED, msg=str(humidity))
            print("DONE")
        except Exception as e:
            print("FAILED")

        print("Publishing: {0} to {1} ... ".format(darkness,aio.AIO_DARKNESS_FEED), end='')
        try:
            client.publish(topic=aio.AIO_DARKNESS_FEED, msg=str(darkness))
            print("DONE")
        except Exception as e:
            print("FAILED")

        finally:
            last_data_sent_ticks = time.ticks_ms()

    except Exception as error:
        print("Exception occurred", error)
    time.sleep(DATA_INTERVAL)

def boundary_check(darkness, temperature, humidity):
    time_zone_offset = +2 
    current_time = utime.time() + time_zone_offset * 3600
    current_time = utime.localtime(current_time)
    current_hour = current_time[3]
    if current_hour >= 22 or current_hour < 6:
        if temperature < 18 or temperature > 19:
            yellowLed.on()
        else:
            yellowLed.off()

        if humidity < 40 or humidity > 60:
            greenLed.on()
        else:
            greenLed.off()

        if darkness <= 90:
            redLed.on()
        else:
            redLed.off()
    else:
        redLed.off()
        yellowLed.off()
        greenLed.off()

def measure(ldr, tempSensor):
    light = ldr.read_u16()
    darkness = round(light / 65535 * 100, 2)
    tempSensor.measure()
    temperature = tempSensor.temperature()
    humidity = tempSensor.humidity()
    boundary_check(darkness, humidity, temperature)
    return [darkness, temperature, humidity]


# Use the MQTT protocol to connect tohelp() Adafruit IO
client = MQTTClient(aio.AIO_CLIENT_ID, aio.AIO_SERVER, aio.AIO_PORT, aio.AIO_USER, aio.AIO_KEY)


client.connect()
ntptime.settime()

try:                      # Code between try: and finally: may cause an error
                        # so ensure the client disconnects the server if
                        # that happens.
    while 1:              # Repeat this loop forever
        measurements = measure(ldr, tempSensor)
        client.check_msg()# Action a message if one is received. Non-blocking.
        boundary_check(measurements[0], measurements[1], measurements[2])
        send_data(measurements[0], measurements[1], measurements[2])     # Send a random number to Adafruit IO if it's time.
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    print("Disconnected from Adafruit IO.")
    time.sleep(20)
    machine.reset()
    



