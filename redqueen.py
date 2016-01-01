from flask import Flask, render_template, request
from core import switch, rgb
import json
app = Flask(__name__)
appname = "homecontrol"

leds = rgb.RgbControl()

@app.route('/')
def index():
  area_states = {}
  r, g, b = leds.get_colors()
  for area in switch.pin_map.keys():
    area_states[area] = switch.get_state(area)
  return render_template('index.html',
    area_states=area_states,
    r=r,
    g=g,
    b=b,
    rgbmodes=leds.get_modes(),
    active_rgbmode=leds.get_mode())

@app.route('/light')
def light():
  return render_template('light.html', areas=areas)

@app.route('/light/switch')
def light_area():
  res = {}
  off = set(switch.pin_map.keys()).difference(request.args.keys())
  on = set(switch.pin_map.keys()).intersection(request.args.keys())

  for area in off:
    switch.light(area, False)
  for area in on:
    switch.light(area, True)
  return "done"

@app.route('/rgb/setmode')
def set_rgb():
  mode = request.args['rgbmodes']
  leds.set_mode(mode)
  return "done"

@app.route('/rgb/setcolor')
def set_color():
  r, g, b = int(request.args['red']), int(request.args['green']), int(request.args['blue'])
  if request.args.has_key('pulse'):
    leds.set_mode('CustomColorMode', red=r, green=g, blue=b, pulse_mode=True)
  else:
    leds.set_mode('CustomColorMode', red=r, green=g, blue=b, pulse_mode=False)
  return "done"

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=80)
  #app.run(host='0.0.0.0')
