#!/usr/bin/python
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Switch(object):
  INVERT = True
  NAME   = None
  PIN    = None
  def __init__(self):
    self.name = self.NAME
    self.invert = self.INVERT
    self.pin  = self.PIN
    GPIO.setup(self.pin, GPIO.OUT)
    self.state = self.get_state()
    logging.debug('Switch: ' + self.name + ' initialized')
    logging.debug('Switch: Current state is ' + str(self.state))

  def get_state(self):
    if self.invert:
      return bool(not GPIO.input(self.pin))
    return bool(GPIO.input(self.pin))

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
  NAME = 'Couch'
  PIN  = 4

class VitrineSwitch(Switch):
  NAME = 'Vitrine'
  PIN  = 5
