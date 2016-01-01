#!/usr/bin/python
import serial
import re
import sys
import inspect
import random
import time
import logging
import shelve
from threading import Thread, Event

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class NoSerialArduinoFoundException(Exception):
  pass

class UnknownArduinoResponseException(Exception):
  pass

class RgbControl(object):
  def __init__(self):
    self.ard = self.arduino_connect()
    self.t = None

  def arduino_connect(self):
    for com in range(0,4):
      try:
        port = '/dev/ttyACM' + str(com)
        BAUD = 9600
        ard = serial.Serial(port, BAUD, timeout=40)
        break
      except:
        pass
    if ard:
      logging.debug('found serial device: %s' % (port))
      return ard
    else:
      raise NoSerialArduinoFoundException('Failed to found Arduino on serial ports /dev/ttyACMXX')

  def modes(self):
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
      if name.endswith('Mode'):
        yield name, obj

  def get_modes(self):
    modes = [ o.NAME for m,o in self.modes()]
    sorted(modes)
    modes.insert(0, "Off")
    return modes

  def get_mode(self):
    if self.t:
      return self.t.__str__()
    else:
      return "Off"

  def get_colors(self):
    if self.t:
      return self.t.current_color()
    else:
      return 0, 0, 0

  def shutdown(self):
    if self.t:
      self.t.stop()
      self.t.join()
      self.t = None

  def set_mode(self, mode, **kwargs):
    res = None
    logging.debug('try to set rgb mode to: ' + mode)
    if mode == "Off":
      self.shutdown()
      res = {'status': 'mode is set to Off'}
    else:
      for m,o in self.modes():
        if o.NAME == mode or m == mode:
          self.shutdown()
          self.t = o(self.ard, **kwargs)
          self.t.start()
          res = {'status': 'mode is set to %s' %(mode)}
    if not res:
      res = {'status': 'unsupported mode'}
    return res

class base_mode(Thread):
  SPEED   = 30
  TMPFILE = '/tmp/rgb.state'
  LOOP    = True
  NAME    = 'base'
  RGB     = (0,0,0)
  def __init__(self, serial_conn, *args, **kwargs):
    super(base_mode, self).__init__()
    self._pulse = False
    #self.fs_serializer = shelve.open(self.TMPFILE + self.NAME, writeback=True)
    self.red, self.green, self.blue = self.RGB[0], self.RGB[1], self.RGB[2]
    self.serial_conn = serial_conn
    self._stop = Event()
    self.loop = self.LOOP
    logging.debug('RgbMode: ' + self.NAME + ' initialzed')
    self.reconfig(self, *args, **kwargs)
    Thread.__init__(self)

  def reconfig(self, *args, **kwargs):
    '''for each unknown keyword argument make it available in self context'''
    self.red, self.green, self.blue = self.RGB[0], self.RGB[1], self.RGB[2]
    # reset colors
    for k in kwargs.keys():
      logging.debug('set: self.%s to %s' % (k, kwargs[k]))
      self.__setattr__(k, kwargs[k])

  def _run_mode(self):
    '''override in abstractin classes'''
    # does nothing
    time.sleep(5)

  def run(self):
    if self.loop:
      sleeper = 0.0
      while not self._stop.isSet():
        if sleeper <= 0:
          sleeper = float(self._run_mode())
        time.sleep(0.5)
        if sleeper <= 0:
          sleeper = 0
        else:
          sleeper -= 0.5
    else:
      self._run_mode()

  def stop(self):
    self._stop.set()
    self._set_light(0,0,0)

  def current_color(self):
    return self.red, self.green, self.blue

  def _pulse_color(self):
    def zero_or_pulse(c):
      i = random.randint(5, 30)
      return 0 if c < i else c - i
    if not self._pulse:
      self._pulse = not(self._pulse)
      pulse_red = zero_or_pulse(self.red)
      pulse_green = zero_or_pulse(self.green)
      pulse_blue = zero_or_pulse(self.blue)
      logging.debug('pulsing to: %i, %i, %i' % (pulse_red, pulse_green, pulse_blue))
      self._set_light(pulse_red, pulse_green, pulse_blue, speed=60)
    else:
      self._pulse = not(self._pulse)
      logging.debug('pulsing back to: %i, %i, %i' % (self.RGB[0], self.RGB[1], self.RGB[2]))
      self._set_light(self.RGB[0], self.RGB[1], self.RGB[2], speed=60)

  def _set_light(self, r, g, b, speed=None):
    if not speed:
      speed = self.SPEED
    logging.debug('change to: %i, %i, %i' % (r, g, b))
    self.serial_conn.write("%i,%i,%i,%i\n" % (speed,r,g,b))
    self.red = r
    self.green = g
    self.blue = b
    logging.debug('report from serial:')
    for line in self.serial_conn:
      line = line.rstrip()
      logging.debug(line)
      if line.startswith('finished'):
        break

  def __str__(self):
    return self.NAME


class RandomMode(base_mode):
  NAME = 'random full'
  def _run_mode(self):
    self._set_light(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return 30

class RandomLowMode(base_mode):
  NAME = 'random low'
  def _run_mode(self):
    self._set_light(random.randint(0, 90), random.randint(0, 90), random.randint(0, 90))
    return 30

class PoliceMode(base_mode):
  NAME = 'police'
  def _run_mode(self):
    if self.blue == 200:
      self._set_light(200, 0, 0, speed=0)
    else:
      logging.debug('blue is: %i' % self.blue)
      self._set_light(0, 0, 200, speed=0)
    return 0.5

class AmberMode(base_mode):
  NAME = 'amber'
  RGB  = (240,50,30)
  def _run_mode(self):
    self._pulse_color()
    return 0.5

class BrothelMode(base_mode):
  NAME = 'brothel'
  RGB  = (217,25,29)
  def _run_mode(self):
    self._pulse_color()
    return 0

class YellowMode(base_mode):
  NAME = 'yellow'
  LOOP = False
  def _run_mode(self):
    self._set_light(255,55,0)
    return 0

class CustomColorMode(base_mode):
  NAME = 'Custom color'
  LOOP = False
  def _run_mode(self):
    if self.pulse_mode:
      self._pulse_color()
    else:
      self._set_light(self.red, self.green, self.blue)
    return 0
