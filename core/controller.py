#!/usr/bin/python
import serial
import sys
import inspect
import logging
from .errors import NoSerialArduinoFoundException, UnknownArduinoResponseException, SwitchNotFound
from . import rgbmodes
from . import switch

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

class Controller(object):
  def __init__(self):
    self.ard = self.arduino_connect()
    self.switches = self._init_switches()
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

  def _init_switches(self):
    switches = {}
    for _, obj in self._gen_switches():
      switches[obj.NAME] = obj()
    return switches

  def _gen_switches(self):
    for name, obj in inspect.getmembers(switch, inspect.isclass):
      if not name.startswith('Switch'):
        yield name, obj


  def _gen_rgbmodes(self):
    for name, obj in inspect.getmembers(rgbmodes, inspect.isclass):
      if name.endswith('Mode'):
        yield name, obj

  def switch(self, switch_name):
    try:
      self.switches[switch_name].light_switch()
    except KeyError:
      raise SwitchNotFound

  def switch_on(self, switch_name):
    try:
      self.switches[switch_name].on()
    except KeyError:
      raise SwitchNotFound

  def switch_off(self, switch_name):
    try:
      self.switches[switch_name].off()
    except KeyError:
      raise SwitchNotFound

  def get_switches(self):
    switches = [ (i.name, i.get_state()) for i in self.switches.values() ]
    sorted(switches)
    return switches

  def get_rgb_modes(self):
    modes = [ o.NAME for m,o in self._gen_rgbmodes()]
    sorted(modes)
    modes.insert(0, "Off")
    return modes

  def get_rgb_mode(self):
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

  def set_rgb_mode(self, mode, **kwargs):
    res = None
    logging.debug('try to set rgb mode to: ' + mode)
    if mode == "Off":
      self.shutdown()
      res = {'status': 'mode is set to Off'}
    else:
      for m,o in self._gen_rgbmodes():
        if o.NAME == mode or m == mode:
          self.shutdown()
          self.t = o(self.ard, **kwargs)
          self.t.start()
          res = {'status': 'mode is set to %s' %(mode)}
    if not res:
      res = {'status': 'unsupported mode'}
    return res
