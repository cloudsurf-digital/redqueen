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

  def get_state(self):
    if self.invert:
      return bool(not GPIO.input(self.pin))
    return bool(GPIO.input(self.pin))

  def on(self):
    if not self.get_state():
      self.light_switch()
      logging.debug('Switch: ' + self.name + ' on')
    else:
      logging.debug('Switch: ' + self.name + ' already on')
  def off(self):
    if self.get_state():
      self.light_switch()
      logging.debug('Switch: ' + self.name + ' off')
    else:
      logging.debug('Switch: ' + self.name + ' already off')

  def light_switch(self):
    GPIO.output(self.pin, not(GPIO.input(self.pin)))


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
