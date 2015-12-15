#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from redqueen import app

if __name__ == '__main__':
  WSGIServer(app, bindAddress='/var/run/redqueen-fcgi.sock').run()
