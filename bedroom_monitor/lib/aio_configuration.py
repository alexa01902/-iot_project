import machine
import ubinascii      

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "alexa222"
AIO_KEY =  "aio_FCqI29UFHAK5wngpQgcmJ5YZEBm6"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = "alexa222/feeds/lights"
AIO_TEMP_FEED = "alexa222/feeds/temperature"
AIO_HUMIDITY_FEED = "alexa222/feeds/humidity"
AIO_DARKNESS_FEED = "alexa222/feeds/light-intensity"