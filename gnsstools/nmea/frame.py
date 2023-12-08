from .exceptions import NmeaParseError


class Frame:
  def __init__(self, msg: bytes):
    try:
      self.source = msg[:2].decode('ascii')
      self.header = msg[2:5].decode('ascii')
      self.values = msg[6:].decode('utf-8').split(',')  # skip the first comma
    except IndexError:
      raise NmeaParseError('Nmea message is very short')


# ---

def test_load_from_msg():
  msg = b'GPGSV,4,2,14,05,,,27,06,,,28,07,,,34,08,,,29'

  frame = Frame(msg)

  assert frame.source == 'GP', 'Source decode error'
  assert frame.header == 'GSV', 'Header decode error'
  assert frame.values[0] == 4, 'Value in pos 0 incorrected'


def test_short_msg():
  msg = b''

  try:
    Frame(msg)
  except NmeaParseError:
    pass
  else:
    raise AssertionError('expected NmeaParseError exception')
