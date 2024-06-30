import machine
import ubinascii      

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "USERNAME"
AIO_KEY =  "MY_AIO_KEY"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_TEMP_FEED = "alexa222/feeds/temperature"
AIO_HUMIDITY_FEED = "alexa222/feeds/humidity"
AIO_DARKNESS_FEED = "alexa222/feeds/light-intensity"
