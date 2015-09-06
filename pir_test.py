import RPi.GPIO as GPIO
import time

SENSOR_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

def mein_callback(channel):
  # Hier kann alternativ eine Anwendung/Befehl etc. gestartet werden.
  print('Es gab eine Bewegung!')

try:
  GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=mein_callback)
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  print "Beende..."
GPIO.cleanup()
