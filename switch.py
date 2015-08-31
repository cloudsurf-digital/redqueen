#!/usr/bin/python
import RPi.GPIO as GPIO
import shelve

pin_map = {'leinwand'  : '2',
           'essbereich': '3',
           'couch'     : '4' }

def load_cache():
  """Load cache"""
  myshelve = '/tmp/gpio.state'
  return shelve.open(myshelve, writeback=True)

def get_state(area):
  states = load_cache()
  light = pin_map[area]
  if states.has_key(light):
    if states[light]:
      res = False
    else:
      res = True
  else:
    res = False
  states.close()
  return res


def light(area, state):
  if get_state(area) == state:
    return
  else:
    light_switch(area)

def light_switch(area):
  light = pin_map[area]
  i_li = int(light)
  GPIO.setup(i_li, GPIO.OUT)
  states = load_cache()
  if states.has_key(light):
    GPIO.output(i_li, not(states[light]))
    states[light] = not(states[light])
  else:
    GPIO.output(i_li, True)
    states[light] = True
  res = states[light]
  states.close()
  return not res

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
