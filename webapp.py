from flask import Flask, render_template, request
import switch
import rgb
import json
app = Flask(__name__)
appname = "homecontrol"

leds = rgb.ArduinoRgb()

areas = ['leinwand', 'essbereich', 'couch']

@app.route('/')
def index():
  area_states = {}
  for area in areas:
    area_states[area] = switch.get_state(area)
  return render_template('index.html',
    area_states=area_states,
    rgbmodes=leds.get_modes(),
    active_rgbmode=leds.get_mode())

@app.route('/light')
def light():
  return render_template('light.html', areas=areas)

@app.route('/light/switch')
def light_area():
  res = {}
  off = set(areas).difference(request.args.keys())
  on = set(areas).intersection(request.args.keys())

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
  
if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=80)
  #app.run(host='0.0.0.0')
