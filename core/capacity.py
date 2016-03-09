#!/usr/bin/python
import RPi.GPIO as GPIO
import logging
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class CButton(object):
  PIN    = None
  def __init__(self):
    self.pin  = self.PIN
    GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    logging.debug('Button: ' + self.name + ' initialized')
    while == True:
      self.ispressed()

  def ispressed(self):
    while GPIO.input(self.pin) == GPIO.LOW:
      time.sleep(0.10)
    print 'Button pressed'


class Light(CButton):
  PIN  = 2


if __name__ == '__main__':
  l = Light()
