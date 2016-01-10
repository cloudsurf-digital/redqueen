#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Switch(object):
  NAME = None
  PIN  = None
  def __init__(self):
    self.name = self.NAME
    self.pin  = self.PIN
    GPIO.setup(self.pin, GPIO.OUT)
    self.state = GPIO.input(self.pin)
    logging.debug('Switch: ' + self.name + ' initialzed')
    logging.debug('Switch: Current state is' + str(self.state))

  def get_state(self):
    return bool(self.state)

  def on(self):
    GPIO.output(self.pin, GPIO.HIGH)
    logging.debug('Switch: ' + self.name + ' on')
  def off(self):
    GPIO.output(self.pin, GPIO.LOW)
    logging.debug('Switch: ' + self.name + ' off')

  def light_switch(self):
    GPIO.output(self.pin, not(self.get_state()))


class LeinwandSwitch(Switch):
  NAME = 'Leinwand'
  PIN  = 2

class EssbereichSwitch(Switch):
  NAME = 'Essbereich'
  PIN  = 3

class CouchSwitch(Switch):
  NAME = 'Leinwand'
  PIN  = 4

class VitrineSwitch(Switch):
  NAME = 'Vitrine'
  PIN  = 5
