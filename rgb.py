#!/usr/bin/python
import serial
import shelve
from threading import Thread, Event
import random
import time

class RgbMode(Thread):
  def __init__(self, function, args, kwargs): 
    super(RgbMode, self).__init__()
    self._stop = Event()
    self.args = args
    self.kwargs = kwargs
    self.func = function
    Thread.__init__(self) 
  def run(self):
    res = None
    while not self.stopped():
     res = self.func(*self.args, **self.kwargs)
  def stop(self):
    self._stop.set()
  def stopped(self):
    return self._stop.isSet()


class ArduinoRgb(object):
  def __init__(self):
    self.fading_speed = '10'
    self.ard = self.arduino_connect()
    self.red, self.green, self.blue = self.get_colors()
    self.t = None
    self.active_mode = 'off'
    self.modes = {'random full': (self.random,),
                  'off': (self.off,),
                  'random low': (self.random_low,),
                  'brothel': (self.mode_brothel,),
                  'yellow': (self.set_light, (255,65,0), {'speed': '20'}),
                  'police': (self.mode_police,),
                  'amber': (self.mode_amber,) }
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
    return sorted(self.modes.keys())

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
    time.sleep(20)

  def random_low(self):
    self.set_light(random.randint(0, 90), random.randint(0, 90), random.randint(0, 90))
    time.sleep(20)

  def mode_police(self):
    self.set_light(200, 0, 0, speed='2')
    time.sleep(0.3)
    self.set_light(0, 0, 200, speed='2')
    time.sleep(0.3)

  def mode_amber(self):
    self._pulse_color(230,50,30)

  def mode_brothel(self):
    self._pulse_color(217,15,19)

  def _pulse_color(self, r, g, b):
    diff1, diff2, diff3  = random.randint(1, 25), random.randint(1, 25), random.randint(1, 25)
    self.set_light(r - diff1, g - diff2, b - diff3, speed='30')
    time.sleep(1.8)
    self.set_light(r, g, b, speed='40')

  def off(self):
    self.set_light(0,0,0)
    # return True if no loop is neccessary
    return True

  def set_mode(self, mode):
    if mode in self.modes.keys():
      if self.t:
        self.t.stop()
        self.t.join()
      if len(self.modes[mode]) == 1:
        self.t = RgbMode(self.modes[mode][0], (), {})
      elif len(self.modes[mode]) == 2:
        self.t = RgbMode(self.modes[mode][0], self.modes[mode][1])
      elif len(self.modes[mode]) == 3:
        self.t = RgbMode(self.modes[mode][0], self.modes[mode][1], self.modes[mode][2])
      self.t.start()
      self.active_mode = mode
    else:
      return {'status': 'unsupported mode'}
    return {'status': 'mode is set to %s' %(mode)}
