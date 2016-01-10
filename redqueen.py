from flask import Flask, render_template, request
from core.controller import Controller
import json
app = Flask(__name__)
appname = "homecontrol"

ctrl = Controller()

@app.route('/')
def index():
  switches = ctrl.get_switches()
  r, g, b = ctrl.get_colors()
  return render_template('index.html',
    area_states=switches,
    r=r,
    g=g,
    b=b,
    rgbmodes=ctrl.get_rgb_modes(),
    active_rgbmode=ctrl.get_rgb_mode())


@app.route('/light/switch')
def light_area():
  off = set([ name for name, state in switches ]).difference(request.args.keys())
  on = set([ name for name, state in switches ]).intersection(request.args.keys())

  for area in off:
    ctrl.switch_off(area)
  for area in on:
    ctrl.switch_on(area)
  return "done"

@app.route('/rgb/setmode')
def set_rgb():
  mode = request.args['rgbmodes']
  ctrl.set_rgb_mode(mode)
  return "done"

@app.route('/rgb/setcolor')
def set_color():
  r, g, b = int(request.args['red']), int(request.args['green']), int(request.args['blue'])
  if request.args.has_key('pulse'):
    ctrl.set_rgb_mode('CustomColorMode', red=r, green=g, blue=b, pulse_mode=True)
  else:
    ctrl.set_rgb_mode('CustomColorMode', red=r, green=g, blue=b, pulse_mode=False)
  return "done"

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=80)
  #app.run(host='0.0.0.0')
