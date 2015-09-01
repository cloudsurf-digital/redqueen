#!/usr/bin/python
import serial
import shelve
from threading import Thread
import random
import time

class RgbMode(Thread):
  def __init__(self, function): 
    self.is_stop = False
    self.func = function
    Thread.__init__(self) 
  def run(self):
    res = None
    while not self.is_stop and not res:
     res = self.func()
  def stop(self):
    self.is_stop = True

class ArduinoRgb(object):
  def __init__(self):
    self.fading_speed = '10'
    self.ard = self.arduino_connect()
    self.red, self.green, self.blue = self.get_colors()
    self.t = None
    self.active_mode = 'off'
    self.modes = {'random full': self.random,
                  'off': self.off,
                  'random low': self.random_low,
                  'amber': self.mode_amber }
  def arduino_connect(self):
    for com in range(0,4):
      try:
        port = '/dev/ttyACM' + str(com)
        BAUD = 9600
        ard = serial.Serial(port, BAUD, timeout=1)
        break
      except:
        pass
    return ard

  def get_modes(self):
    return self.modes.keys()

  def get_mode(self):
    return self.active_mode

  def get_colors(self):
    states = self.load_cache()
    red = states.get('red', '0')
    green = states.get('green', '0')
    blue = states.get('blue', '0')
    states.close()
    return red, green, blue

  def load_cache(self):
    """Load cache"""
    myshelve = '/tmp/rgb.state'
    return shelve.open(myshelve, writeback=True)

  def set_light(self, r, g, b, speed='10'):
    self.ard.write("%s,%s,%s,%s\n" % (speed,r,g,b))
    self.ard.readline()
    self.ard.readline()
    self.ard.readline()
    self.ard.readline()
    self.ard.readline()

  def random(self):
    self.set_light(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    time.sleep(30)

  def random_low(self):
    self.set_light(random.randint(0, 90), random.randint(0, 90), random.randint(0, 90))
    time.sleep(30)

  def mode_amber(self):
    self._pulse_color(230,50,30)

  def _pulse_color(self, r, g, b):
    speed = str(random.randint(15, 40))
    diff1, diff2, diff3  = random.randint(5, 30), random.randint(5, 30), random.randint(5, 30)
    self.set_light(r - diff1, g - diff2, b - diff3, speed=speed)
    time.sleep(1.5)
    self.set_light(r, g, b, speed=40)

  def off(self):
    self.set_light(0,0,0)
    # return True if no loop is neccessary
    return True

  def set_mode(self, mode):
    if mode in self.modes.keys():
      if self.t:
        self.t.stop()
      self.t = RgbMode(self.modes[mode])
      self.t.start()
      self.active_mode = mode
    else:
      return {'status': 'unsupported mode'}
    return {'status': 'mode is set to %s' %(mode)}
