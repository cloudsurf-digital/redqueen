#!/usr/bin/python
class NoSerialArduinoFoundException(Exception):
  pass

class UnknownArduinoResponseException(Exception):
  pass

class SwitchNotFound(KeyError):
  pass
